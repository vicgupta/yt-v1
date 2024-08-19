import datetime as dt
import uuid, os
import pandas as pd
from pytube import YouTube, extract
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from aster.db.sqlite3orm import SQLite3ORM
db = SQLite3ORM("ytdownloads.db")





def yt_get_transcript(video_link):
    video_id = extract.video_id(video_link) 
    transcript_lines = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = "".join(list(pd.DataFrame(transcript_lines)['text']))
    return transcript

def yt_download_video(url):
    currentDate = dt.datetime.now().strftime("%Y-%m-%d")
    previousDate = dt.datetime.now() - dt.timedelta(days=1)
    output_dir = "downloads/"
    currentOutputPath = output_dir + str(currentDate)
    previousOutputPath = output_dir + str(previousDate)

    if os.path.exists(currentOutputPath) == False:
        os.makedirs(currentOutputPath)
    else:
        if os.path.exists(previousOutputPath):
            os.rmdir(previousOutputPath)

    unique_filename = uuid.uuid4()
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': f'{currentOutputPath}/{unique_filename}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        # 'postprocessors': [{ 
        #     'key': 'FFmpegVideoConvertor',
        #     'preferedformat': 'mp4'
        # }]
    }
    full_filename = f'{currentOutputPath}/{unique_filename}.mp4'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([url])
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Unknown Title')
        duration = info.get('duration', 0)
        view_count = info.get('view_count', 0)
        filesize = os.path.getsize(full_filename)
        db.insert("downloads", {"url": url,"title":title, "duration": duration, "views": view_count,"filesize":filesize, "downloaded_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    return f'{currentOutputPath}/{unique_filename}.mp4'

def yt_video_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)