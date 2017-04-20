import MySQLdb as db
import bcrypt
import os
import song

def connect():
    return db.connect(host='localhost', user='root', passwd=os.environ['ROOTPASSWD'], db='final_project')

def fetchUser(email):
    con = connect()
    cur = con.cursor()

    cur.execute('SELECT id, email FROM users WHERE email=%s', (email,))

    if cur.rowcount < 1:
        return None

    return cur.fetchone()[0] 

def addUser(email, password):
    con = connect()
    cur = con.cursor()

    salt = bcrypt.gensalt()
    pwhash = bcrypt.hashpw(password.encode('utf8'), salt)

    cur.execute('INSERT INTO users(email, pwhash) VALUES(%s, %s)', (email, pwhash))
    con.commit()

def validateUser(email, password):
    con = connect()
    cur = con.cursor()

    cur.execute('SELECT pwhash FROM users WHERE email=%s', (email,))
    if cur.rowcount < 1:
        return False

    pwhash = cur.fetchone()[0]
    return (bcrypt.hashpw(password.encode('utf8'), pwhash) == pwhash)

def getPlaylists(userid):
    con = connect()
    cur = con.cursor()

    cur.execute('SELECT id, userid, title FROM playlists WHERE userid=%s', (userid,))
    playlists = []

    for row in cur.fetchall():
        playlists.append(song.Playlist(row[0], row[1], row[2], False))

    return playlists

def getSongs(query, playlistid=""):
    con = connect()
    cur = con.cursor()

    query = '%' + query + '%'

    if playlistid == "":
        cur.execute('SELECT id, title, artist, length FROM songs WHERE title LIKE %s', (query,)) 
    else:
        cur.execute('SELECT id, title, artist, length FROM songs WHERE title LIKE %s AND id IN (SELECT songid FROM contains WHERE playlistID=%s)', (query, playlistid))

    songs = []
    for row in cur.fetchall():
        minutes = row[3] / 60
        seconds = row[3] % 60
        length = str(minutes) + ':' + str(seconds)
        
        songs.append(song.Song(row[0], row[1], row[2], length))

    return songs    
