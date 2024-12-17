from __future__ import unicode_literals

import yt_dlp as youtube_dl

from service.SongDao import before_save_song

base_url = "https://www.youtube.com/watch?v="


def progress(value):
    if value['status'] == 'finished':
        print("Download finished")

    elif value['status'] == 'downloading':
        print(value['filename'], value['_percent_str'], value['_eta_str'])


def download(video_id, client_id, file_name):
    ytdl_options = {
        'outtmpl': f'songs/{file_name}.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            'ffmpeg_location': '/usr/bin/ffmpeg /usr/share/ffmpeg',
        }],
        'progress_hooks': [progress]
    }

    with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
        url = base_url + video_id
        print(f"DOWNLOADING: {url}")
        ytdl.download([url])

    file_path = f"songs/{file_name}.mp3"

    before_save_song(file_path, video_id, file_name, client_id)





