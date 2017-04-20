
class Song:
    def __init__(self, sid, title, artist, length):
        self.sid = sid
        self.title = title
        self.artist = artist
        self.length = length

class Playlist:
    def __init__(self, pid, userid, title, selected):
        self.pid = pid
        self.userid=userid
        self.title=title
        self.selected = selected
