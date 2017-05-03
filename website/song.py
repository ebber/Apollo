
class Song:
    def __init__(self, sid, title, artist, length, path):
        self.sid = sid
        self.title = title
        self.artist = artist
        self.length = length
        self.path = path

    def get_length(self):
        time = self.length.split(':')
        minutes = int(time[0])
        seconds = int(time[1])

        return 60*minutes + seconds

class Playlist:
    def __init__(self, pid, userid, title, selected):
        self.pid = pid
        self.userid=userid
        self.title=title
        self.selected = selected
