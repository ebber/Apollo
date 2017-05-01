from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import os
import json, requests
import sys

DEVELOPER_KEY = os.environ['YOUTUBEKEY']
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"

#Appears to use 102 credits, have 1,000,000 per day
def get_url(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    response = youtube.search().list(q=query, part='id, snippet', maxResults=25).execute()

    for result in response.get('items', []):
        if result['id']['kind'] == 'youtube#video':
            return 'https://www.youtube.com/watch?v=' + str(result['id']['videoId'])

#Appears to use 3 credits
def get_song_title(songId):
    songData = requests.get('https://www.googleapis.com/youtube/v3/videos/?id=' + songId +'&part=snippet' \
                          + '&key=' + os.environ['YOUTUBEKEY'])
    return json.loads(songData.content)['items'][0]['snippet']['title']

if __name__ == '__main__':
    print get_url(sys.argv[1])
