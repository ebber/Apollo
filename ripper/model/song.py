import taglib
from fileOps import move_file
import os

class Song:
    #file path should be dir+filename
    def __init__(self, dir, filename):
        self.song = taglib.File(dir+filename)
        self.filename = filename
        self.dir = dir

    def fillMetadta(self, basicMeta):
        #print basicMeta
        self.setTitle(basicMeta["TITLE"][0])
        self.setArtist(basicMeta["ARTIST"][0])
        self.setAlbum(basicMeta["ALBUM"][0])
        self.save()

    def setTitle(self, newTitle):
        try:
            self.song.tags["TITLE"] = [newTitle]
        except:
            return -1
        return 1;

    def getTitle(self):
        return self.song.tags.get("TITLE")

    def setArtist(self, newArtist):
        try:
            self.song.tags["ARTIST"] = [newArtist]
        except:
            return -1
        return 1;

    def getArtist(self):
        return self.song.tags["ARTIST"]

    def setAlbum(self, newAlbum):
        try:
            self.song.tags["ALBUM"] = [newAlbum]
        except:
            return -1
        return 1;

    def getAlbum(self):
        return self.song.tags["ALBUM"]

    def printTags(self):
        print(self.song.tags)

    #filename comes from /songs
    def save(self, destDir = None):
        retVal = self.song.save()
        if None is destDir:
            return retVal

        #at top level dict
        title = self.getTitle()[0] if self.getTitle() != None else self.filename
        move_file(self.dir + self.filename, destDir + title +".mp3")

        return retVal






