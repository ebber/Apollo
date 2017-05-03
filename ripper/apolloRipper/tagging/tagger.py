from ripper.apolloRipper.model.song import Song
import logging

from ripper.apolloRipper.tagging.spotify_meta_retriever import spotify_metaRetriever

class Tagger():

    logger = logging.getLogger("TaggerLogger")
    spotifyRetriever = spotify_metaRetriever()

    def __init__(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fhdlr = logging.FileHandler('logs/taggerLog.log')
        fhdlr.setLevel(logging.DEBUG)
        fhdlr.setFormatter(formatter)

        self.logger.addHandler(fhdlr)
        self.logger.addHandler(ch)

    def tag_song(self, song):
       return self.tag_spotify(song)

    def tag_spotify(self, song):
        try:
            metaData = self.spotifyRetriever.retrieve_metadata(song)
            song.fillMetadta(metaData)
            return 0
        except AttributeError as err:
            self.logger.warning("Failed to tag: " + song.filename)
            return -1

