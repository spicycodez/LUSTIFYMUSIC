import asyncio
import glob
import os
import random
import re
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from LustifyMusic import LOGGER
from LustifyMusic.utils.formatters import time_to_seconds

logger = LOGGER(__name__)


# ==========================
# COOKIE HANDLING (OPTIONAL)
# ==========================
def cookie_txt_file():
    try:
        folder_path = f"{os.getcwd()}/cookies"
        txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
        if not txt_files:
            return None
        return f"cookies/{os.path.basename(random.choice(txt_files))}"
    except Exception:
        return None


# ==========================
# DIRECT yt-dlp DOWNLOADER
# ==========================
async def direct_ytdlp_download(vid_id: str, is_video: bool = False):
    try:
        url = f"https://youtu.be/{vid_id}"

        if is_video:
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "quiet": True,
                "noplaylist": True,
            }
        else:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "quiet": True,
                "noplaylist": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

        cookie = cookie_txt_file()
        if cookie:
            ydl_opts["cookiefile"] = cookie

        loop = asyncio.get_running_loop()

        def run():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return info.get("id"), info.get("ext")

        vid, ext = await loop.run_in_executor(None, run)

        if is_video:
            return f"downloads/{vid}.{ext}"
        else:
            return f"downloads/{vid}.mp3"

    except Exception as e:
        logger.error(f"Direct yt-dlp download failed: {str(e)}")
        return None


# ==========================
# MAIN YOUTUBE CLASS
# ==========================
class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    # --------------------------
    # CHECK IF LINK IS YOUTUBE
    # --------------------------
    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    # --------------------------
    # EXTRACT URL FROM MESSAGE
    # --------------------------
    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        text = ""
        offset = None
        length = None

        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url

        if offset is None:
            return None

        return text[offset: offset + length]

    # ==========================
    # DETAILS (SEARCH OR URL)
    # ==========================
    async def details(self, link: str, videoid: Union[bool, str] = None):
        # If not a YouTube URL, treat as search query
        if not re.search(self.regex, link):
            query = link
        else:
            if videoid:
                link = self.base + link
            query = link.split("&")[0].split("?si=")[0]

        results = VideosSearch(query, limit=1)
        data = await results.next()

        for result in data.get("result", []):
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]

            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(time_to_seconds(duration_min))

            return title, duration_min, duration_sec, thumbnail, vidid

        raise ValueError("No results found for this query")

    # ==========================
    # TITLE
    # ==========================
    async def title(self, link: str, videoid: Union[bool, str] = None):
        if not re.search(self.regex, link):
            query = link
        else:
            if videoid:
                link = self.base + link
            query = link.split("&")[0].split("?si=")[0]

        results = VideosSearch(query, limit=1)
        data = await results.next()

        for result in data.get("result", []):
            return result["title"]

        raise ValueError("No title found")

    # ==========================
    # DURATION
    # ==========================
    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if not re.search(self.regex, link):
            query = link
        else:
            if videoid:
                link = self.base + link
            query = link.split("&")[0].split("?si=")[0]

        results = VideosSearch(query, limit=1)
        data = await results.next()

        for result in data.get("result", []):
            return result["duration"]

        raise ValueError("No duration found")

    # ==========================
    # THUMBNAIL
    # ==========================
    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if not re.search(self.regex, link):
            query = link
        else:
            if videoid:
                link = self.base + link
            query = link.split("&")[0].split("?si=")[0]

        results = VideosSearch(query, limit=1)
        data = await results.next()

        for result in data.get("result", []):
            return result["thumbnails"][0]["url"].split("?")[0]

        raise ValueError("No thumbnail found")

    # ==========================
    # GET STREAM URL (VC PLAY)
    # ==========================
    async def video(self, link: str, videoid: Union[bool, str] = None):
        if not re.search(self.regex, link):
            # Search first to get video ID
            results = VideosSearch(link, limit=1)
            data = await results.next()
            for result in data.get("result", []):
                link = f"https://youtu.be/{result['id']}"
                break

        if videoid:
            link = self.base + link

        link = link.split("&")[0].split("?si=")[0]

        try:
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp",
                "-g",
                "-f",
                "best[height<=?720][width<=?1280]",
                link,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()

            if stdout:
                return 1, stdout.decode().split("\n")[0]
            else:
                return 0, stderr.decode()

        except Exception as e:
            return 0, str(e)

    # ==========================
    # PLAYLIST
    # ==========================
    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if not re.search(self.regex, link):
            raise ValueError("Playlist requires a YouTube URL")

        if videoid:
            link = self.listbase + link

        link = link.split("&")[0].split("?si=")[0]

        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-i",
            "--get-id",
            "--flat-playlist",
            "--playlist-end",
            str(limit),
            "--skip-download",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()
        result = stdout.decode().split("\n")
        return [x for x in result if x]

    # ==========================
    # TRACK INFO
    # ==========================
    async def track(self, link: str, videoid: Union[bool, str] = None):
        if not re.search(self.regex, link):
            query = link
        else:
            if videoid:
                link = self.base + link
            query = link.split("&")[0].split("?si=")[0]

        results = VideosSearch(query, limit=1)
        data = await results.next()

        for result in data.get("result", []):
            track_details = {
                "title": result["title"],
                "link": result["link"],
                "vidid": result["id"],
                "duration_min": result["duration"],
                "thumb": result["thumbnails"][0]["url"].split("?")[0],
            }
            return track_details, result["id"]

        raise ValueError("No track found for this query")

    # ==========================
    # FORMATS
    # ==========================
    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if not re.search(self.regex, link):
            raise ValueError("Formats require a YouTube URL")

        if videoid:
            link = self.base + link

        link = link.split("&")[0].split("?si=")[0]

        ydl_opts = {"quiet": True}
        cookie = cookie_txt_file()
        if cookie:
            ydl_opts["cookiefile"] = cookie

        formats_available = []

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            r = ydl.extract_info(link, download=False)
            for fmt in r.get("formats", []):
                try:
                    if "dash" in str(fmt.get("format", "")).lower():
                        continue
                    formats_available.append({
                        "format": fmt.get("format"),
                        "filesize": fmt.get("filesize"),
                        "format_id": fmt.get("format_id"),
                        "ext": fmt.get("ext"),
                        "format_note": fmt.get("format_note"),
                        "yturl": link,
                    })
                except Exception:
                    continue

        return formats_available, link

    # ==========================
    # SLIDER SEARCH
    # ==========================
    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if not re.search(self.regex, link):
            query = link
        else:
            if videoid:
                link = self.base + link
            query = link.split("&")[0].split("?si=")[0]

        try:
            results = []
            search = VideosSearch(query, limit=10)
            search_results = (await search.next()).get("result", [])

            for result in search_results:
                duration_str = result.get("duration", "0:00")
                parts = duration_str.split(":")
                duration_secs = 0

                if len(parts) == 3:
                    duration_secs = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                elif len(parts) == 2:
                    duration_secs = int(parts[0]) * 60 + int(parts[1])

                if duration_secs <= 3600:
                    results.append(result)

            if not results or query_type >= len(results):
                raise ValueError("No suitable videos found")

            selected = results[query_type]
            return (
                selected["title"],
                selected["duration"],
                selected["thumbnails"][0]["url"].split("?")[0],
                selected["id"]
            )

        except Exception as e:
            logger.error(f"Error in slider: {str(e)}")
            raise ValueError("Failed to fetch video details")

    # ==========================
    # DOWNLOAD ENTRY POINT
    # ==========================
    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ):
        # Determine video ID
        if re.search(self.regex, link):
            vid_id = link.split("v=")[-1].split("&")[0].replace("youtu.be/", "")
        else:
            # Search to get video ID
            results = VideosSearch(link, limit=1)
            data = await results.next()
            for result in data.get("result", []):
                vid_id = result["id"]
                break
            else:
                return None, False

        # ===== DIRECT yt-dlp MODE =====

        if songvideo:
            fpath = await direct_ytdlp_download(vid_id, is_video=True)
            return fpath

        elif songaudio:
            fpath = await direct_ytdlp_download(vid_id, is_video=False)
            return fpath

        elif video:
            direct = True
            downloaded_file = await direct_ytdlp_download(vid_id, is_video=True)
        else:
            direct = True
            downloaded_file = await direct_ytdlp_download(vid_id, is_video=False)

        return downloaded_file, direct
