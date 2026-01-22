import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()


API_ID = int(getenv("API_ID", "24208695"))

API_HASH = getenv("API_HASH", "fa96a7eb2dffe7f4cc8ba1399b68d24d")

BOT_TOKEN = getenv("BOT_TOKEN", "7850675931:AAFVjBhaO9D2ZNdRZjbATkAsCqZAdvD2hNs")

MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://LUSTIFYXMUSIC:Abhi77394@lustifymusic.evxnqby.mongodb.net/?retryWrites=true&w=majority&appName=LUSTIFYMUSIC")

YTPROXY_URL = getenv("YTPROXY_URL", 'https://tgapi.xbitcode.com') ## xBit Music Endpoint.
YT_API_KEY = getenv("YT_API_KEY" , "" ) ## Your API key like: xbit_10000000xx0233 Get from  https://t.me/tgmusic_apibot

#API_URL = getenv("API_URL", "https://tgapi.xbitcode.com") #YTPROXY_URL = getenv("YTPROXY_URL", 'https://tgapi.xbitcode.com')
#VIDEO_API_URL = getenv("VIDEO_API_URL", "https://api.video.thequickearn.xyz")
#API_KEY = getenv("API_KEY", "NxGBNexGenBotse151bd")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 54000))

SONG_DOWNLOAD_DURATION = int(
    getenv("SONG_DOWNLOAD_DURATION_LIMIT", "54000")
)

LOGGER_ID = int(getenv("LOGGER_ID", -1003356124495))

OWNER_ID = int(getenv("OWNER_ID", "7603581459"))

BOT_USERNAME = getenv("BOT_USERNAME" , "LustifyMusicBot")

COMMAND_HANDLER = getenv("COMMAND_HANDLER", "! / .").split()

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/spicycodez/LUSTIFYMUSIC",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", "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"
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/SpicyxNetwork")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/ChatHouseGc")

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
AUTO_SUGGESTION_MODE = getenv("AUTO_SUGGESTION_MODE", "True")
AUTO_SUGGESTION_TIME = int(
    getenv("AUTO_SUGGESTION_TIME", "500"))

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)



PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

CLEANMODE_DELETE_MINS = int(
    getenv("CLEANMODE_MINS", "5"))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 21474836480))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 21474836480))



# Get your pyrogram v2 session from @Shsusu_bot on Telegram
STRING1 = getenv("STRING_SESSION", "BQFZuDsAlI9PGTSv2KJ1V4LbUe7LBoNvQExsvz_7dpQnbm3Y0Hka65rjndUHb_2gD24FMaYTwiZXUzZDzyjCWMV5q0ADG6ki648XCgWOw52UIgTyRWR-PMrIQh9Um0uIJSP_EPgJ6LGAIUQ1gWMjYnAJqurqoaQqCyv_sGzKxOMGyvl6okB-kK2G5py4J7fpId6aBmYIvfH24UtU9HHz18dx2AkOKmDcffRD3yp2dkSyZW69MUGQc6vck2vlFU-tn9uRKflDAH7fAao9a97v2JLzZNPfqMjXkXUR4EjxY2rsrgwyjEZMcOlOHj04nfK1ZxCFj9P8nZ9EmOdPE_Y8NnBhMWRArAAAAAGMQVi8AA")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
chatstats = {}
userstats = {}
clean = {}

autoclean = []

START_IMG_URL = getenv(
    "START_IMG_URL", "https://files.catbox.moe/aov76u.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://files.catbox.moe/aov76u.jpg"
)
PLAYLIST_IMG_URL = "https://files.catbox.moe/aov76u.jpg"
STATS_IMG_URL = "https://files.catbox.moe/aov76u.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/aov76u.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/aov76u.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/aov76u.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/aov76u.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/aov76u.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/aov76u.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/aov76u.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/aov76u.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(
    time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
