import unittest
from tagging.spotify_meta_retriever import spotify_metaRetriever

class spotifyMetaRetrieverTest(unittest.TestCase):


    spotifyRetriever = spotify_metaRetriever()

    def test_remove_extraneous(self):
        query = "official video test"
        new_querry = self.spotifyRetriever.removeExtraneous(query)
        self.assertEqual("test", new_querry.replace(" ",""))

