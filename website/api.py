from flask import Flask, Blueprint, flash, redirect, render_template, request, session, url_for
import database
import config

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


###Web hooks:

#Set volume here
@api.route('/api/setVolume', methods=['POST'])
def setVolume():
    config.volume = request.form['volume']
    return ''

#Set song time here
@api.route('/api/setTime', methods=['POST'])
def setTime():
    config.time = request.form['time']
    return ''

#Unpause here
@api.route('/api/play', methods=['POST'])
def play():
    return ''

#Pause here
@api.route('/api/pause', methods=['POST'])
def pause():
    return ''

#Play next song here
@api.route('/api/nextSong', methods=['POST'])
def nextSong():
    return ''

#Download song here:
def download(url):
    pass
