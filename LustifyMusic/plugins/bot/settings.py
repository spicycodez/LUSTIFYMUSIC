import random
import config
from time import time
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified

from LustifyMusic import app
from LustifyMusic.utils.database import (
    add_nonadmin_chat, get_authuser, get_authuser_names,
    get_playmode, get_playtype, get_upvote_count,
    is_nonadmin_chat, is_skipmode,
    remove_nonadmin_chat, set_playmode, set_playtype,
    set_upvotes, skip_off, skip_on,
)
from LustifyMusic.utils.decorators.admins import ActualAdminCB
from LustifyMusic.utils.decorators.language import language, languageCB
from LustifyMusic.utils.inline.settings import (
    auth_users_markup, playmode_users_markup,
    setting_markup, vote_mode_markup,
)
from LustifyMusic.utils.inline.start import private_panel
from config import BANNED_USERS, OWNER_ID


# ✅ Unique images
LUSTIFY_PIC = [
    "https://files.catbox.moe/7kbojt.jpg",
    "https://files.catbox.moe/y8xei6.jpg",
    "https://files.catbox.moe/taeu8f.jpg",
    "https://files.catbox.moe/p3rdn3.jpg",
    "https://files.catbox.moe/30qlzm.jpg",
    "https://files.catbox.moe/6ed6rh.jpg",
    "https://files.catbox.moe/i5o42l.jpg",
    "https://files.catbox.moe/2b9dlp.jpg",
    "https://files.catbox.moe/5hb0yi.jpg",
    "https://files.catbox.moe/9i4zek.jpg",
    "https://files.catbox.moe/p5k77y.jpg",
    "https://files.catbox.moe/zlds64.jpg"
]


# =========================
# 🔧 Utility Helpers
# =========================

def back_close_buttons():
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data="settingsback_helper"),
            InlineKeyboardButton("⌯ ᴄʟᴏsᴇ ⌯", callback_data="close"),
        ]]
    )


# =========================
# ⚙️ Settings
# =========================

@app.on_message(filters.command(["settings", "setting"]) & filters.group & ~BANNED_USERS)
@language
async def settings_mar(client, message: Message, _):
    await message.reply_text(
        _["setting_1"].format(app.mention, message.chat.id, message.chat.title),
        reply_markup=InlineKeyboardMarkup(setting_markup(_)),
    )


@app.on_callback_query(filters.regex("settings_helper") & ~BANNED_USERS)
@languageCB
async def settings_cb(client, query: CallbackQuery, _):
    await query.answer(_["set_cb_5"])
    await query.edit_message_text(
        _["setting_1"].format(app.mention, query.message.chat.id, query.message.chat.title),
        reply_markup=InlineKeyboardMarkup(setting_markup(_)),
    )


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_markup(client, query: CallbackQuery, _):
    await query.answer()
    if query.message.chat.type == ChatType.PRIVATE:
        return await query.edit_message_media(
            InputMediaPhoto(
                media=random.choice(LUSTIFY_PIC),
                caption=_["start_2"].format(query.from_user.mention, app.mention),
                has_spoiler=True
            ),
            reply_markup=InlineKeyboardMarkup(private_panel(_)),
            
        )
    return await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(setting_markup(_)))


# =========================
# 📂 Gib Source
# =========================

@app.on_callback_query(filters.regex("gib_source"))
async def gib_repo_callback(client, query: CallbackQuery):
    await query.edit_message_media(
        InputMediaPhoto(
            media="https://files.catbox.moe/h4higm.jpg",
            caption="ᴄʜᴧʟᴀ ᴊᴧ ʙʜᴏsᴅɪᴋᴇ",
            has_spoiler=True,
        ),
        reply_markup=back_close_buttons(),
    )


# =========================
# 📊 Bot Info
# =========================

@app.on_callback_query(filters.regex("^bot_info_data$"))
async def show_bot_info(client, query: CallbackQuery):
    start = time()
    temp = await client.send_message(query.message.chat.id, "ᴘɪɴɢ ᴘᴏɴɢ 💕..")
    delta_ping = time() - start
    await temp.delete()

    txt = f"""💌 ᴘɪɴɢ ᴘᴏɴɢ ʙᴧʙʏ...

• ᴅᴧᴛᴧʙᴧsᴇ: ᴏɴʟɪɴᴇ
• ʏᴏᴜᴛᴜʙᴇ ᴧᴘɪ: ʀᴇsᴘᴏɴsɪᴠᴇ
• ʙᴏᴛ sᴇʀᴠᴇʀ: ʀᴜɴɴɪɴɢ sᴍᴏᴏᴛʜʟʏ
• ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ: ᴏᴘᴛɪᴍᴧʟ
• ᴧᴘɪ ᴘɪɴɢ: {delta_ping * 1000:.3f} ms   

• ᴇᴠᴇʀʏᴛʜɪɴɢ ʟᴏᴏᴋs ɢᴏᴏᴅ!
"""
    await query.answer(txt, show_alert=True)


# =========================
# 💌 Support Links
# =========================

@app.on_callback_query(filters.regex("shiv_lustify") & ~BANNED_USERS)
@languageCB
async def support(client, query: CallbackQuery, _):
    await query.edit_message_text(
        text="💌 ʜᴇʀᴇ ᴀʀᴇ ꜱᴏᴍᴇ ɪᴍᴘᴏʀᴛᴀɴᴛ ʟɪɴᴋꜱ ᴊᴏɪɴ ᴘʟᴇᴀsᴇ...💞",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⌯ sᴜᴘᴘᴏʀᴛ ⌯", url=config.SUPPORT_CHAT),
                    InlineKeyboardButton("⌯ ᴄʜᴧɴɴᴇʟ ⌯", url=config.SUPPORT_CHANNEL),
                ],
                [
                    InlineKeyboardButton("⌯ ᴏᴡɴᴇʀ ⌯", user_id=config.OWNER_ID),
                    InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data="settingsback_helper"),
                ],
            ]
        ),
    )


# =========================
# ❌ Without Admin Rights
# =========================

@app.on_callback_query(
    filters.regex(r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|ANSWERVOMODE|VOTEANSWER|PM|AU|VM)$") 
    & ~BANNED_USERS
)
@languageCB
async def without_admin_rights(client, query: CallbackQuery, _):
    cmd = query.matches[0].group(1)

    if cmd == "SEARCHANSWER":
        return await query.answer(_["setting_2"], show_alert=True)
    if cmd == "PLAYMODEANSWER":
        return await query.answer(_["setting_5"], show_alert=True)
    if cmd == "PLAYTYPEANSWER":
        return await query.answer(_["setting_6"], show_alert=True)
    if cmd == "AUTHANSWER":
        return await query.answer(_["setting_3"], show_alert=True)
    if cmd == "VOTEANSWER":
        return await query.answer(_["setting_8"], show_alert=True)
    if cmd == "ANSWERVOMODE":
        current = await get_upvote_count(query.message.chat.id)
        return await query.answer(_["setting_9"].format(current), show_alert=True)

    # Playmode, Auth, Vote
    buttons = None
    if cmd == "PM":
        await query.answer(_["set_cb_2"], show_alert=True)
        playmode = await get_playmode(query.message.chat.id)
        Direct = playmode == "Direct"
        Group = not await is_nonadmin_chat(query.message.chat.id)
        Playtype = not (await get_playtype(query.message.chat.id) == "Everyone")
        buttons = playmode_users_markup(_, Direct, Group, Playtype)

    if cmd == "AU":
        await query.answer(_["set_cb_1"], show_alert=True)
        is_non_admin = await is_nonadmin_chat(query.message.chat.id)
        buttons = auth_users_markup(_, not is_non_admin)

    if cmd == "VM":
        mode = await is_skipmode(query.message.chat.id)
        current = await get_upvote_count(query.message.chat.id)
        buttons = vote_mode_markup(_, current, mode)

    if buttons:
        try:
            return await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
        except MessageNotModified:
            return


# =========================
# ➕ Vote Addition
# =========================

@app.on_callback_query(filters.regex("FERRARIUDTI") & ~BANNED_USERS)
@ActualAdminCB
async def addition(client, query: CallbackQuery, _):
    mode = query.data.strip().split(None, 1)[1]
    if not await is_skipmode(query.message.chat.id):
        return await query.answer(_["setting_10"], show_alert=True)

    current = await get_upvote_count(query.message.chat.id)
    final = current - 2 if mode == "M" else current + 2

    if final <= 2:
        final = 2
    if final >= 15:
        final = 15

    await set_upvotes(query.message.chat.id, final)
    try:
        return await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(vote_mode_markup(_, final, True)))
    except MessageNotModified:
        return


# =========================
# 🎮 Playmode Change
# =========================

@app.on_callback_query(filters.regex(r"^(MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$") & ~BANNED_USERS)
@ActualAdminCB
async def playmode_ans(client, query: CallbackQuery, _):
    cmd = query.matches[0].group(1)

    if cmd == "CHANNELMODECHANGE":
        if not await is_nonadmin_chat(query.message.chat.id):
            await add_nonadmin_chat(query.message.chat.id)
            Group = None
        else:
            await remove_nonadmin_chat(query.message.chat.id)
            Group = True
        Direct = await get_playmode(query.message.chat.id) == "Direct"
        Playtype = not (await get_playtype(query.message.chat.id) == "Everyone")

    elif cmd == "MODECHANGE":
        await query.answer(_["set_cb_3"], show_alert=True)
        playmode = await get_playmode(query.message.chat.id)
        if playmode == "Direct":
            await set_playmode(query.message.chat.id, "Inline")
            Direct = None
        else:
            await set_playmode(query.message.chat.id, "Direct")
            Direct = True
        Group = not await is_nonadmin_chat(query.message.chat.id)
        Playtype = not (await get_playtype(query.message.chat.id) == "Everyone")

    else:  # PLAYTYPECHANGE
        await query.answer(_["set_cb_3"], show_alert=True)
        playty = await get_playtype(query.message.chat.id)
        if playty == "Everyone":
            await set_playtype(query.message.chat.id, "Admin")
            Playtype = False
        else:
            await set_playtype(query.message.chat.id, "Everyone")
            Playtype = True
        Direct = await get_playmode(query.message.chat.id) == "Direct"
        Group = not await is_nonadmin_chat(query.message.chat.id)

    buttons = playmode_users_markup(_, Direct, Group, Playtype)
    try:
        return await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        return


# =========================
# 👥 Auth Users
# =========================

@app.on_callback_query(filters.regex(r"^(AUTH|AUTHLIST)$") & ~BANNED_USERS)
@ActualAdminCB
async def authusers_mar(client, query: CallbackQuery, _):
    cmd = query.matches[0].group(1)

    if cmd == "AUTHLIST":
        _authusers = await get_authuser_names(query.message.chat.id)
        if not _authusers:
            return await query.answer(_["setting_4"], show_alert=True)

        msg = _["auth_7"].format(query.message.chat.title)
        for idx, note in enumerate(_authusers, 1):
            _note = await get_authuser(query.message.chat.id, note)
            try:
                user = (await app.get_users(_note["auth_user_id"])).first_name
            except:
                continue
            msg += f"{idx}➤ {user}[<code>{_note['auth_user_id']}</code>]\n"
            msg += f"   {_['auth_8']} {_note['admin_name']}[<code>{_note['admin_id']}</code>]\n\n"

        upl = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(_["BACK_BUTTON"], callback_data="AU"),
                InlineKeyboardButton(_["CLOSE_BUTTON"], callback_data="close"),
            ]]
        )
        try:
            return await query.edit_message_text(msg, reply_markup=upl)
        except MessageNotModified:
            return

    # AUTH toggle
    await query.answer(_["set_cb_3"], show_alert=True)
    if not await is_nonadmin_chat(query.message.chat.id):
        await add_nonadmin_chat(query.message.chat.id)
        buttons = auth_users_markup(_)
    else:
        await remove_nonadmin_chat(query.message.chat.id)
        buttons = auth_users_markup(_, True)

    try:
        return await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        return


# =========================
# 🗳️ Vote Change
# =========================

@app.on_callback_query(filters.regex("VOMODECHANGE") & ~BANNED_USERS)
@ActualAdminCB
async def vote_change(client, query: CallbackQuery, _):
    await query.answer(_["set_cb_3"], show_alert=True)
    if await is_skipmode(query.message.chat.id):
        await skip_off(query.message.chat.id)
        mod = None
    else:
        await skip_on(query.message.chat.id)
        mod = True

    current = await get_upvote_count(query.message.chat.id)
    try:
        return await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(vote_mode_markup(_, current, mod)))
    except MessageNotModified:
        return
