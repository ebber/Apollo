#from distutils.core import setup
#from distutils.core import setup
from setuptools import setup
setup(
  name = 'apolloRipper',
  packages = ['apolloRipper'], # this must be the same as the name above
  version = '0.3',
  description = 'The ripper and tagger for Apollo',
  author = 'Erik Beitel',
  author_email = 'erik.beitel@gmail.com',
  url = 'https://github.com/ebber/apolloRipper', # use the URL to the github repo
  download_url = 'https://github.com/ebber/apolloRipper/archive/0.3.tar.gz', # I'll explain this in a second
  install_requires=[
   "logging",
   "youtube_dl",
   "ffprobe",
   "spotipy"
    ],
  keywords = ['audio', 'youtube ripper'], # arbitrary keywords
  classifiers = [],
)
