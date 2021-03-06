import os

from ripper.apolloRipper import config
from ripper.apolloRipper.ripper.ytRipper import Ripper
from ripper.apolloRipper.model.song import Song
from ripper.apolloRipper.tagging.tagger import Tagger
from mPlayer.apolloMusicPlayer.customplayer import mPlayer

import logging

tagger = Tagger()
ripper = Ripper()
player = mPlayer()
notDone = True

logger = logging.getLogger("mainLoopLogger")
#goes through all songs in the directory, calls tagFile
def tagDir(dir=config.DIR_UNTAGGED):
    logger.info("tagging songs in "+dir)
    for filename in os.listdir(dir):
        if filename.endswith(".mp3"):
            song = Song(dir, filename)
            if tagger.tag_song(song) == -1:
                song.save(config.DIR_FAILED_TAG)
            else: #song was succesfully tagged move it to completed songs
                song.save(config.DIR_TAGGED)

#really this should spawn a child process
def tag_continous(dir = config.DIR_UNTAGGED):
    logger.info("Tagging songs contiously in "+dir)
    files = os.listdir(dir)
    while(notDone):
        new_files = os.listdir(dir)
        for fname in new_files:
            if fname not in files:
                song = Song(dir, filename=fname)
                pass


def rip_playlist(playlist_url):
    logger.info("ripping playlist " + playlist_url)
    ripper.rip(playlist_url)

def print_prompt():
    help_text = "help\n"
    help_text += " tag <directory> - tag a directory \n"
    help_text += " rip <playlist url> - rip a song or playlist from youtube \n"
    help_text += " volume - [volume] \n"
    help_text += " q - quit"

    print(help_text)



while True:
    input_cmd = raw_input("What do you want to do?")
    print(input_cmd)
    cmd= input_cmd.rstrip().split(" ")
    if '?' == cmd[0]:
        print_prompt()
    elif "tag" == cmd[0]:
        tagDir(config.DIR_UNTAGGED)
    elif "rip" == cmd[0]:
        if len(cmd) == 1:
            print("seperate the command and playlist with a space")
        else:
            rip_playlist(cmd[1])
    elif "play" == cmd[0]:
            player.play()
    elif "pause" == cmd[0]:
	    player.pause()
    elif "skip" == cmd[0]:
	    player.skip()
    elif "list" == cmd[0]:
	    player.print_queue();
    elif "queue" == cmd[0]:
        if len(cmd) == 1:
            print("seperate the command and playlist with a space")
        else:
            player.add_song_to_queue(cmd[1])
    elif "volume" == cmd[0]:
        if len(cmd) == 1:
            print("seperate the command and playlist with a space")
        else:
            player.change_volume(int(cmd[1]))
  
    elif 'q' == cmd[0]:
        break
    else:
        print_prompt()
