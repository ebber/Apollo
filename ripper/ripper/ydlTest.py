from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'outtmpl': 'songs/untagged/%(title)s.%(ext)s', 
    'progress_hooks': [my_hook],
}

playlist_url = 'https://www.youtube.com/playlist?list=PLra91-sOzgVI64DrfOUnG-kmx8RG_tHIl'

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url ])
