from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    f = open("ripperLog.log",'w');
    def debug(self, msg):
	self.f.write("DEBUG"+msg)
	

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Ripper():
    """ripper class"""
    def __init__(self):
	self.ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
	    }],
	    'logger': MyLogger(),
	    'outtmpl': 'songs/untaggedSongs/%(title)s.%(ext)s', 
	    'progress_hooks': [self.my_hook],
	}

    def rip(self, playlist_url):
	"""rip a playlist or song"""
	with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
	    ydl.download([playlist_url ])

    def my_hook(self,d):
	"""hook for logging"""
        if d['status'] == 'finished':
	    print('Done downloading, now converting', d['filename'])

if __name__ == "__main__":
	print("testing download")
	playlist_url = 'https://www.youtube.com/playlist?list=PLra91-sOzgVIgiMr-pxMKwm5ZCYEXGWYX' 
	ripper = Ripper()
	ripper.rip(playlist_url)
