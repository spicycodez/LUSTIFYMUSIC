from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from LustifyMusic import app

logging.basicConfig(level=logging.INFO)

# ----------------------- VC STARTED -----------------------
@app.on_message(filters.video_chat_started)
async def video_chat_started(client, message: Message):
    chat = message.chat
    await message.reply(
        f"<b>🎥 ᴠᴏɪᴄᴇ ᴄʜᴧᴛ sᴛᴧʀᴛ ʜᴏ ɢʏᴧ ʜᴧ {chat.title} 💕</b>\n\n"
        f"<b>ʙᴧʙʏʏʏ ᴊᴏɪɴ ᴋᴀʀ ʟᴏ ɴᴀ... ᴍᴀɴᴅ ʙʜᴧʟᴧ ᴅᴏᴏɴɢɪ 😉</b>"
    )

# ----------------------- VC ENDED -------------------------
@app.on_message(filters.video_chat_ended)
async def video_chat_ended(client, message: Message):
    chat = message.chat
    await message.reply(
        f"<b>🚫 ᴠᴏɪᴄᴇ ᴄʜᴧᴛ ᴋʜᴧᴛᴧᴍ ʜᴏ ɢʏᴧ {chat.title} </b>\n\n"
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
