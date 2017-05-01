import spotipy
import requests
import logging

#add auth
class spotify_metaRetriever:
  uselessWords = ["official video", "official video", "music video"]
  logger = logging.getLogger("Spotify Tagger Logger")

  def __init__(self):
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    fhdlr = logging.FileHandler('logs/sporitfyLog.log')
    fhdlr.setLevel(logging.DEBUG)
    fhdlr.setFormatter(formatter)

    self.logger.addHandler(fhdlr)
    self.logger.addHandler(ch)
    self.sp = spotipy.Spotify()

    try:
      results = self.sp.search(q='artist: Panic!', type='artist')
    except requests.exceptions.ConnectionError:
      self.logger.critical("Warning cannot connect to spotify")



  def removeExtraneous(self, q):
    lower = q.lower();
    for phrase in self.uselessWords:
      lower = lower.replace(phrase, "")

    return lower

  def smartSpotifyQuery(self, q):
    sQ = self.removeExtraneous(q)
    return self.spotifyQuery(sQ)


  def spotifyQuery(self, q):
    #print "Querrying spotify with: ", q
    result = self.sp.search(q, type='track', limit=1)
    tracks= result["tracks"]["items"]
    if len(tracks)>0:
      return tracks[0]
    else:
      #print "nothing returned from spotify",result
      return -1

    return result[0]

  def extractBasicMetadata(self, spotifyResult):
    basicData = {}
    if spotifyResult == -1:
      raise AttributeError #this means the song wasn't found
    print(spotifyResult)
    basicData["TITLE"] = [spotifyResult['name']]
    artists = [artist["name"] for artist in spotifyResult["artists"]]
    basicData["ARTIST"] = artists
    basicData["ALBUM"] = spotifyResult["album"]["name"]
    return basicData

  #takes a song
  def retrieve_metadata(self, song):
    query = song.filename.replace(".mp3", "");
    result = self.smartSpotifyQuery(query)
    metaData = self.extractBasicMetadata(result)
    return metaData


