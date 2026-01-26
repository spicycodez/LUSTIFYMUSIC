from pyrogram import filters, enums
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatPermissions
)
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    BadRequest
)
import random
from logging import getLogger
from LustifyMusic import LOGGER
from config import LOGGER_ID as LOG_GROUP_ID
from LustifyMusic.misc import SUDOERS
from LustifyMusic import app
from LustifyMusic.helper.admin_check import admin_filter
from config import OWNER_ID
from pyrogram.enums import ChatMemberStatus

LOGGER = getLogger(__name__)

kickpic = [
    "https://files.catbox.moe/30qlzm.jpg",
    "https://files.catbox.moe/6ed6rh.jpg",
    "https://files.catbox.moe/i5o42l.jpg",
]

button = [
    [
        InlineKeyboardButton(
            text="Ɗᴇᴠ𝘴", url="https://t.me/SheOwnsMaxim"
        )
    ]
]

def mention(user, name, mention=True):
    if mention:
        return f"[{name}](tg://openmessage?user_id={user})"
    else:
        return f"[{name}](https://t.me/{user})"

async def get_userid_from_username(username):
    try:
        user = await app.get_users(username)
    except Exception:
        return None
    return [user.id, user.first_name]

async def bans_user(user_id, first_name, admin_id, admin_name, chat_id, message):
    try:
        await app.ban_chat_member(chat_id, user_id)
        await app.unban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "I need ban rights to perform this action.", False
    except UserAdminInvalid:
        return "I can't ban another admin!", False
    except Exception as e:
        if user_id == OWNER_ID:
            return "Why should I ban myself? I'm not that silly!", False
        return f"An error occurred: {e}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    try:
        await app.send_message(
            LOG_GROUP_ID,
            f"{user_mention} was banned by {admin_mention} in {message.chat.title}"
        )
    except Exception:
        pass

    ban_message = await message.reply_photo(
        photo=random.choice(kickpic),
        caption=f"{user_mention} was banned by {admin_mention}."
    )
    return ban_message, True


# ==========================
# BAN COMMAND (FULL SAFE)
# ==========================
@app.on_message(filters.command("ban") & admin_filter)
async def ban_user_with_unban_button(client, message: Message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name

    # Check admin status
    try:
        member = await chat.get_member(admin_id)
    except Exception:
        return await message.reply_text("Failed to fetch your admin status.")

    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text("You don't have permission to ban someone.")

    if not member.privileges or not member.privileges.can_restrict_members:
        return await message.reply_text("You don't have permission to ban someone.")

    user_id = None
    first_name = "User"

    # Case 1: /ban <user_id or username>
    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
        except ValueError:
            user_obj = await get_userid_from_username(message.command[1])
            if user_obj is None:
                return await message.reply_text("User not found.")
            user_id = user_obj[0]
            first_name = user_obj[1]

    # Case 2: Reply ban
    elif message.reply_to_message:
        if not message.reply_to_message.from_user:
            return await message.reply_text("Can't ban this user (no user info found).")
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name

    # Case 3: No target
    else:
        return await message.reply_text("Reply to a user or use: /ban <user_id/username>")

    # Safety checks
    if user_id == OWNER_ID:
        return await message.reply_text("You cannot ban the bot owner.")

    if user_id == admin_id:
        return await message.reply_text("You cannot ban yourself.")

    # Perform ban
    msg_text, result = await bans_user(
        user_id,
        first_name,
        admin_id,
        admin_name,
        chat_id,
        message
    )

    if not result:
        return await message.reply_text(msg_text)

    # Unban button
    unban_button = [
        [InlineKeyboardButton("ƲɴʙᴀƝ ƲsᴇƦ", callback_data=f"unban_{user_id}")]
    ]

    await message.reply_text(
        f"Click below to unban {first_name}.",
        reply_markup=InlineKeyboardMarkup(unban_button),
    )


# ==========================
# UNBAN COMMAND (SAFE)
# ==========================
@app.on_message(filters.command("unban") & admin_filter)
async def unban_user(client, message: Message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name

    # Check admin status
    try:
        member = await chat.get_member(admin_id)
    except Exception:
        return await message.reply_text("Failed to fetch your admin status.")

    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text("You don't have permission to unban someone.")

    if not member.privileges or not member.privileges.can_restrict_members:
        return await message.reply_text("You don't have permission to unban someone.")

    if len(message.command) <= 1:
        return await message.reply_text("Use: /unban <user_id/username>")

    try:
        user_id = int(message.command[1])
        first_name = "User"
    except ValueError:
        user_obj = await get_userid_from_username(message.command[1])
        if user_obj is None:
            return await message.reply_text("User not found.")
        user_id = user_obj[0]
        first_name = user_obj[1]

    try:
        await app.unban_chat_member(chat_id, user_id)

        user_mention = mention(user_id, first_name)
        admin_mention = mention(admin_id, admin_name)

        await message.reply_photo(
            photo=random.choice(kickpic),
            caption=f"{user_mention} was unbanned by {admin_mention}.",
            reply_markup=InlineKeyboardMarkup(button),
        )

        try:
            await app.send_message(
                LOG_GROUP_ID,
                f"{user_mention} was unbanned by {admin_mention} in {message.chat.title}"
            )
        except Exception:
            pass

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")


# ==========================
# UNBAN CALLBACK BUTTON
# ==========================
@app.on_callback_query(filters.regex(r"unban_(\d+)"))
async def unban_button_callback(client, callback_query):
    user_id = int(callback_query.matches[0].group(1))
    chat_id = callback_query.message.chat.id

    try:
        await app.unban_chat_member(chat_id, user_id)
        await callback_query.answer("User has been unbanned!")
        await callback_query.message.edit_text("The user has been successfully unbanned.")
    except Exception as e:
        await callback_query.answer(f"An error occurred: {e}")


# ==========================
# KICKME COMMAND (SAFE)
# ==========================
@app.on_message(filters.command("kickme") & filters.group)
async def kickme_command(client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    try:
        await app.ban_chat_member(chat_id, user_id)
        await message.reply_photo(
            photo=random.choice(kickpic),
            caption=f"{user_name} has kicked themselves out of the group!",
            reply_markup=InlineKeyboardMarkup(button),
        )

        try:
            await app.send_message(
                LOG_GROUP_ID,
                f"{user_name} used the kickme command in {message.chat.title}"
            )
        except Exception:
            pass

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
