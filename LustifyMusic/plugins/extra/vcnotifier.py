from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated
import logging
from LustifyMusic import app

logging.basicConfig(level=logging.INFO)

# ----------------------- VC STARTED -----------------------
@app.on_message(filters.video_chat_started)
async def video_chat_started(client, message: Message):
    chat = message.chat
    await message.reply(
        f"<b>🎥 ᴠᴏɪᴄᴇ ᴄʜᴧᴛ sᴛᴧʀᴛ ʜᴏ ɢʏᴧ ʜᴧ {chat.title} ᴍᴇᴍ~ 💕</b>\n\n"
        f"<b>ʙᴧʙʏʏʏ ᴊᴏɪɴ ᴋᴀʀ ʟᴏ ɴᴀ... ᴍᴀɴᴅ ʙʜᴧʟᴧ ᴅᴏᴏɴɢɪ 😉</b>"
    )

# ----------------------- VC ENDED -------------------------
@app.on_message(filters.video_chat_ended)
async def video_chat_ended(client, message: Message):
    chat = message.chat
    await message.reply(
        f"<b>🚫 ᴠᴏɪᴄᴇ ᴄʜᴧᴛ ᴋʜᴧᴛᴧᴍ ʜᴏ ɢʏᴧ {chat.title} ᴍᴇᴍ…</b>\n\n"
        f"<b>ᴛʜᴧɴᴋ ʏᴏᴜ ꜰᴏʀ ᴊᴏɪɴɪɴɢ ʙᴧʙʏʏʏ... ᴍɪss ᴋᴀʀᴜɴɢɪ 😘👋</b>"
    )

# ----------------------- USER INVITED TO VC -----------------------
@app.on_message(filters.video_chat_members_invited)
async def vc_invited(client, message: Message):
    chat = message.chat
    inviter = message.from_user
    invited_users = message.video_chat_members_invited.users

    text = f"💞 <b>{inviter.mention}</b> ʙᴧʙʏʏʏ ɴᴇ ᴋɪssɪ ᴋᴏ ᴠᴄ ᴍᴇ ʙᴜʟᴧʏᴧ ʜᴧ…!\n\n"
    text += "👥 <b>ɪɴᴠɪᴛᴇᴅ ᴜsᴇʀs:</b>\n"

    for user in invited_users:
        text += f"• {user.mention}\n"

    await message.reply(text)

# ----------------------- USER JOIN / LEAVE VC -----------------------
@app.on_chat_member_updated()
async def member_update(client, update: ChatMemberUpdated):
    chat = update.chat
    old = update.old_chat_member
    new = update.new_chat_member

    # ----- USER JOINS VC -----
    try:
        if not old.is_speaking and new.is_speaking:
            if not new.user.is_bot:
                msg = await app.send_message(
                    chat.id,
                    f"💗 <b>{new.user.mention}</b> ʙᴧʙʏʏʏ ᴠᴄ ᴍᴇ ᴧ ɢʏᴧᴀᴀ… "
                    f"ᴍᴜᴊʜᴇ ʙʜɪ ʙᴜʟᴧ ʟᴏᴏ ɴᴀ 😉💞"
                )
                await msg.delete(delay=300)  # auto delete after 5 minutes
    except:
        pass

    # ----- USER LEAVES VC -----
    try:
        if old.is_speaking and not new.is_speaking:
            msg = await app.send_message(
                chat.id,
                f"💔 <b>{new.user.mention}</b> ᴠᴄ sᴇ ᴄʜᴧʟᴧ ɢʏᴧ ʙᴧʙʏ… "
                f"ᴍɪss ᴋᴀʀᴜɴɢɪ 😢"
            )
            await msg.delete(delay=300)  # auto delete after 5 minutes
    except:
        pass
