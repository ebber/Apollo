#from distutils.core import setup
#from distutils.core import setup
from setuptools import setup
setup(
  name = 'apolloMusicPlayer',
  packages = ['apolloMusicPlayer'], # this must be the same as the name above
  version = '0.2',
  description = 'The music player for Apollo',
  author = 'Erik Beitel',
  author_email = 'erik.beitel@gmail.com',
  url = 'https://github.com/ebber/apolloMusicPlayer', # use the URL to the github repo
  download_url = 'https://github.com/ebber/apolloMusicPlayer/archive/0.2.tar.gz', # I'll explain this in a second
  install_requires=[
   "musicplayer",
   "logging"
    ],
  keywords = ['audio', 'music player'], # arbitrary keywords
  classifiers = [],
)
