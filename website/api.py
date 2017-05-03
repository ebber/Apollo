from flask import Flask, Blueprint, flash, redirect, render_template, request, session, url_for
from ..mPlayer.apolloMusicPlayer.customplayer import mPlayer
from ..ripper.apolloRipper.ripper.ytRipper import Ripper
from threading import Thread
import json
import database
import config
import search

ripper = Ripper()
player = mPlayer()
api = Blueprint('api', __name__, template_folder='templates')

@api.route('/api/register', methods=['POST'])
def register():
    try:
        email = request.form['email']
        password = request.form['password']
    except:
        return response('', 400)

    if not database.fetchUser(email) is None:
        error = 'Error: Username already exists'
    else:
        database.addUser(email, password)
        session['user'] = email

        flash('Success: Logging in')
        return redirect(url_for('mysite.index')) 

    return render_template('login.html', error=error)

@api.route('/api/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except:
        return response('', 400)

    if not database.validateUser(email, password):
        error = 'Error: Incorrect username or password'
    else:
        session['user'] = email
        flash('Success: Logging in')
        return redirect(url_for('mysite.index'))

    return render_template('login.html', error=error)

@api.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return render_template('login.html', error=None)

@api.route('/api/queueAdd', methods=['POST'])
def queueAdd():
    sid = request.form['songid']

    for s in config.queue:
        if s.sid == int(sid):
            return '{"type": "error", "error": "Already in Queue"}'

    newsong = database.getSong(sid)
    config.queue.append(newsong)
    pos = len(config.queue)
    player.queue = map(lambda x: x.path, config.queue)
    return '{"type": "success", "song": "' + newsong.title + '", "position": ' + str(pos) + '}'

@api.route('/api/playlistAdd', methods=['POST'])
def playlistAdd():
    songid = request.form['songid']
    playlistID = request.form['playlistid']

    user = session['user']
    userid = database.fetchUser(user)
    playlists = database.getPlaylists(userid)

    if playlistID not in map(lambda x: str(x.pid), playlists):
        return '', 400 

    database.addToPlaylist(playlistID, songid)
    return ''

@api.route('/api/playlistRemove', methods=['POST'])
def playlistRemove():
    songid = request.form['songid']
    playlistID = request.form['playlistid']
    
    user = session['user']
    userid = database.fetchUser(user)
    playlists = database.getPlaylists(userid)

    if playlistID not in map(lambda x: str(x.pid), playlists):
        return '', 400 

    database.removeFromPlaylist(playlistID, songid)
    return ''

@api.route('/api/queueUpdate', methods=['POST'])
def queueUpdate():
    config.queue = map(lambda x: database.getSong(x), request.form.getlist('queue[]'))
    player.queue = map(lambda x: x.path, config.queue)
    return ''

@api.route('/api/createPlaylist', methods=['POST'])
def createPlaylist():
    title = request.form['title']
    userid = database.fetchUser(session['user'])

    database.createPlaylist(userid, title)
    return ''

@api.route('/api/libraryAdd', methods=['POST'])
def libraryAdd():
    title = request.form['title']
    url = search.get_url(title)
    thread = Thread(target=download, args=(url,))
    thread.start()

    title = search.get_song_title(url.replace('https://www.youtube.com/watch?v=', ''))
    artist = ''
    length = 0
    
    database.addSong(title, artist, length, 'songs/untaggedSongs/' + title)
    return redirect(url_for('mysite.library'))

###Web hooks:

#Set volume here
@api.route('/api/setVolume', methods=['POST'])
def setVolume():
    config.volume = request.form['volume']
    player.change_volume(config.volume)
    return ''

#Set song time here
@api.route('/api/setTime', methods=['POST'])
def setTime():
    config.time = request.form['time']
    return ''

#Unpause here
@api.route('/api/play', methods=['POST'])
def play():
    player.play()
    return ''

#Pause here
@api.route('/api/pause', methods=['POST'])
def pause():
    player.pause()
    return ''

#Play next song here
@api.route('/api/nextSong', methods=['POST'])
def nextSong():
    config.queue = config.queue[1:]
    player.skip()
    return ''

#Download song here:
def download(url):
    ripper.rip(url)
