# ------------------------------
# IMPORTS
# ------------------------------
import random
import string
import traceback

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from LustifyMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from LustifyMusic.core.call import Lustify
from LustifyMusic.utils import seconds_to_min, time_to_seconds
from LustifyMusic.utils.channelplay import get_channeplayCB
from LustifyMusic.utils.decorators.language import languageCB
from LustifyMusic.utils.decorators.play import PlayWrapper
from LustifyMusic.utils.formatters import formats
from LustifyMusic.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from LustifyMusic.utils.logger import play_logs
from LustifyMusic.utils.stream.stream import stream
from config import BANNED_USERS, lyrical


# ------------------------------
# EMOJIS
# ------------------------------
EMOJII = [
    "ʙᴀʙʏ ɪ ᴄᴀɴ ꜰᴇᴇʟ ᴛʜᴇ ʙᴇᴀᴛ ᴡɪᴛʜ ᴜ ✨🥀",
    "ᴏᴏʜ ʙᴀʙʏ, ʟᴇᴛ'ꜱ ɢᴇᴛ ʟᴏꜱᴛ ɪɴ ᴛʜɪꜱ ᴠɪʙᴇ 🦋✨",
    "ʙᴀʙʏ, ᴛᴜʀɴ ɪᴛ ᴜᴘ… ꜰᴇᴇʟ ᴍᴇ? 🥀🦋",
    "ʜᴏʟᴅ ᴍᴇ ᴄʟᴏꜱᴇ ʙᴀʙʏ, ʟᴇᴛ'ꜱ ꜱᴡᴀʏ ✨💫",
    "ʙᴀʙʏ, ᴛʜᴇ ʀʜʏᴛʜᴍ ɪꜱ ᴍᴀᴋɪɴɢ ᴍᴇ ᴄʀᴀᴢʏ 🥀✨",
]

# ------------------------------
# PLAY COMMAND
# ------------------------------
@app.on_message(
    filters.command(
        [
            "play",
            "vplay",
            "cplay",
            "cvplay",
            "playforce",
            "vplayforce",
            "cplayforce",
            "cvplayforce",
        ]
    )
    & filters.group
    & ~BANNED_USERS
)
@PlayWrapper
async def play_commnd(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    Emoji = random.choice(EMOJII)
    mystic = await message.reply_text(
        _["play_2"].format(channel) if channel else Emoji
    )

    plist_id = None
    slider = None
    plist_type = None
    spotify = None

    user_id = message.from_user.id
    user_name = message.from_user.mention

    # ==========================
    # TEXT QUERY PART (MAIN BUG AREA)
    # ==========================
    if not url:
        if len(message.command) < 2:
            buttons = botplaylist_markup(_)
            return await mystic.edit_text(
                _["play_18"],
                reply_markup=InlineKeyboardMarkup(buttons),
            )

        slider = True
        query = message.text.split(None, 1)[1]
        if "-v" in query:
            query = query.replace("-v", "")

        try:
            details, track_id = await YouTube.track(query)
        except Exception as e:
            traceback.print_exc()
            print("YOUTUBE TRACK ERROR (TEXT QUERY):", e)
            return await mystic.edit_text(f"FAILED TO PROCESS QUERY: {e}")

        streamtype = "youtube"

    # ==========================
    # URL PART
    # ==========================
    else:
        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(
                        url,
                        config.PLAYLIST_FETCH_LIMIT,
                        message.from_user.id,
                    )
                except Exception as e:
                    traceback.print_exc()
                    print("YOUTUBE PLAYLIST ERROR:", e)
                    return await mystic.edit_text(f"FAILED TO PROCESS QUERY: {e}")

                streamtype = "playlist"
                plist_type = "yt"
                if "&" in url:
                    plist_id = (url.split("=")[1]).split("&")[0]
                else:
                    plist_id = url.split("=")[1]

                img = config.PLAYLIST_IMG_URL
                cap = _["play_9"]

            else:
                try:
                    details, track_id = await YouTube.track(url)
                except Exception as e:
                    traceback.print_exc()
                    print("YOUTUBE URL TRACK ERROR:", e)
                    return await mystic.edit_text(f"FAILED TO PROCESS QUERY: {e}")

                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_10"].format(
                    details["title"],
                    details["duration_min"],
                )

        else:
            # Not YouTube URL — fallback stream
            try:
                await Lustify.stream_call(url)
            except NoActiveGroupCall:
                await mystic.edit_text(_["black_9"])
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=_["play_17"],
                )
            except Exception as e:
                return await mystic.edit_text(_["general_2"].format(type(e).__name__))

            await mystic.edit_text(_["str_2"])
            try:
                await stream(
                    _,
                    mystic,
                    message.from_user.id,
                    url,
                    chat_id,
                    message.from_user.first_name,
                    message.chat.id,
                    video=video,
                    streamtype="index",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
                return await mystic.edit_text(err)

            return await play_logs(message, streamtype="M3u8 or Index Link")

    # ==========================
    # DIRECT PLAY MODE
    # ==========================
    if str(playmode) == "Direct":
        if not plist_type:
            if details.get("duration_min"):
                duration_sec = time_to_seconds(details["duration_min"])
                if duration_sec > config.DURATION_LIMIT:
                    return await mystic.edit_text(
                        _["play_6"].format(config.DURATION_LIMIT_MIN, app.mention)
                    )
            else:
                buttons = livestream_markup(
                    _,
                    track_id,
                    user_id,
                    "v" if video else "a",
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                return await mystic.edit_text(
                    _["play_13"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                video=video,
                streamtype=streamtype,
                spotify=spotify,
                forceplay=fplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
            return await mystic.edit_text(err)

        await mystic.delete()
        return await play_logs(message, streamtype=streamtype)

    # ==========================
    # INLINE / SLIDER MODE
    # ==========================
    else:
        if plist_type:
            ran_hash = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )
            lyrical[ran_hash] = plist_id

            buttons = playlist_markup(
                _,
                ran_hash,
                message.from_user.id,
                plist_type,
                "c" if channel else "g",
                "f" if fplay else "d",
            )

            await mystic.delete()
            await message.reply_photo(
                photo=img,
                caption=cap,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return await play_logs(message, streamtype=f"Playlist : {plist_type}")

        else:
            if slider:
                buttons = slider_markup(
                    _,
                    track_id,
                    message.from_user.id,
                    query,
                    0,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_photo(
                    photo=details["thumb"],
                    caption=_["play_10"].format(
                        details["title"].title(),
                        details["duration_min"],
                    ),
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, streamtype="Searched on Youtube")

            else:
                buttons = track_markup(
                    _,
                    track_id,
                    message.from_user.id,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_photo(
                    photo=img,
                    caption=cap,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, streamtype="URL Searched Inline")
