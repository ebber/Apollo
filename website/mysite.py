from flask import Flask, Blueprint, flash, redirect, render_template, request, session, url_for
import database
import config

mysite = Blueprint('mysite', __name__, template_folder='templates')

@mysite.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html", user=session.get('user'), error=None)

@mysite.route('/', methods=['GET'])
def index():
    return render_template("index.html", user=session.get('user'), volume=config.volume, t=config.time)

@mysite.route('/library', methods=['GET'])
def library():
    user = session.get('user')
    userid = database.fetchUser(user)
    playlists = database.getPlaylists(userid)

    playlistID = request.args.get('playlist')
    query = request.args.get('query')
    order = request.args.get('sort')
    toreverse = request.args.get('reversed')

    if query is None:
        query = ''

    if playlistID is None or playlistID == "all" or playlistID not in map(lambda x: str(x.pid), playlists):
        songs = database.getSongs(query)
        allselected = True
    else:
        songs = database.getSongs(query, playlistID)
        allselected = False

    if toreverse == 'true':
        toreverse = True
    else:
        toreverse = False

    if order == 'title':
        songs = sorted(songs, key=lambda x: x.title, reverse=toreverse)
    if order == 'artist':
        songs = sorted(songs, key=lambda x: x.artist, reverse=toreverse)
    if order == 'duration':
        songs = sorted(songs, key=lambda x: x.get_length(), reverse=toreverse)

    return render_template("library.html", user=user, playlists=playlists, songs=songs, allselected=allselected, pid=playlistID)

@mysite.route('/queue', methods=['GET'])
def queue():
    return render_template("queue.html", user=session.get('user'), songs=config.queue)
