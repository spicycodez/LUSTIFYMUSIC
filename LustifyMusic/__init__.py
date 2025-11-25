from LustifyMusic.core.bot import Lustify
from LustifyMusic.core.dir import dirr
from LustifyMusic.core.git import git
from LustifyMusic.core.userbot import Userbot
from LustifyMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Lustify()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
