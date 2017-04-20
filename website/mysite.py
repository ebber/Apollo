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

    if query is None:
        query = ''

    if playlistID is None or playlistID == "all":
        songs = database.getSongs(query)
        allselected = True
    elif playlistID not in map(lambda x: str(x.pid), playlists):
        return '', 400
    else:
        songs = database.getSongs(query, playlistID)
        allselected = False

    return render_template("library.html", user=user, playlists=playlists, songs=songs, allselected=allselected)

@mysite.route('/queue', methods=['GET'])
def queue():
    return render_template("queue.html", user=session.get('user'))
