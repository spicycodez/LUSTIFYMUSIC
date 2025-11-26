from datetime import datetime
import random

from pyrogram import filters
from pyrogram.types import Message

from LustifyMusic import app
from LustifyMusic.core.call import Lustify
from LustifyMusic.utils import bot_sys_stats
from LustifyMusic.utils.decorators.language import language
from LustifyMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL

PING_IMAGES = [
    "https://files.catbox.moe/taeu8f.jpg",
    "https://files.catbox.moe/taeu8f.jpg",
]


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()

    # single spoiler image 
    wait_msg = await message.reply_photo(
        photo=random.choice(PING_IMAGES),
        caption=_["ping_1"].format(app.mention),
        has_spoiler=True
    )

    # Stats
    pytgping = await Lustify.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000

    # old msg dlt
    await wait_msg.delete()

    await message.reply_photo(
        photo=random.choice(PING_IMAGES),
        caption=_["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        has_spoiler=True,
        reply_markup=supp_markup(_),
    )
