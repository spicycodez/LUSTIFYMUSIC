from pyrogram import Client, filters
from pyrogram.types import Message, ChatMember
import logging
from LustifyMusic import app

logging.basicConfig(level=logging.INFO)

@app.on_message(filters.video_chat_started)
async def video_chat_started(client, message: Message):
    chat = message.chat
    await message.reply(
        f"<b>🎥 Vᴏɪᴄᴇ Cʜᴧᴛ ʜᴧs Sᴛᴧʀᴛᴇᴅ ɪɴ {chat.title}!</b>\n\n<b>ᴊᴏɪɴ ᴜs ɴᴏᴡ ꜰᴏʀ ᴧ ꜰᴜɴ ᴛɪᴍᴇ ᴛᴏɢᴇᴛʜᴇʀ..! 😉</b>"
    )

@app.on_message(filters.video_chat_ended)
async def video_chat_ended(client, message: Message):
    chat = message.chat
    await message.reply(
        f"<b>🚫 Vᴏɪᴄᴇ Cʜᴧᴛ ʜᴧs Eɴᴅᴇᴅ ɪɴ {chat.title}.</b>\n\n<b>ᴛʜᴧɴᴋs ʏᴏᴜ ꜰᴏʀ ᴊᴏɪɴɪɴɢ..! sᴇᴇ ʏᴏᴜ ɴᴇxᴛ ᴛɪᴍᴇ..! 👋</b>"
    )
