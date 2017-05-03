import MySQLdb as db
import bcrypt
import os
import song

def connect():
    return db.connect(host='localhost', user='root', passwd=os.environ['ROOTPASSWD'], db='final_project')

def addSong(title, artist, length, path):
    con = connect()
    cur = con.cursor()

    cur.execute('INSERT INTO songs(title, artist, length, path) VALUES(%s, %s, %s, %s)', (title, artist, length, path))
    con.commit()

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

    cur.execute('INSERT INTO users(email, pwhash, priviledges) VALUES(%s, %s, \'a\')', (email, pwhash))
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

def getSong(songid):
    con = connect()
    cur = con.cursor()
    
    cur.execute('SELECT id, title, artist, length, path FROM songs WHERE id=%s', (songid,))
    songtuple = cur.fetchone()

    seconds = songtuple[3] % 60
    minutes = songtuple[3] / 60
    length = str(minutes) + ':' + ('0' if seconds < 10 else '') + str(seconds)

    return song.Song(songtuple[0], songtuple[1], songtuple[2], length, songtuple[4])

def getSongs(query, playlistid=""):
    con = connect()
    cur = con.cursor()

    query = '%' + query + '%'

    if playlistid == "":
        cur.execute('SELECT id, title, artist, length, path FROM songs WHERE title LIKE %s', (query,)) 
    else:
        cur.execute('SELECT id, title, artist, length, path FROM songs WHERE title LIKE %s AND id IN (SELECT songid FROM contains WHERE playlistID=%s)', (query, playlistid))

    songs = []
    for row in cur.fetchall():
        minutes = row[3] / 60
        seconds = row[3] % 60
        length = str(minutes) + ':' + ('0' if seconds < 10 else '') + str(seconds)
        
        songs.append(song.Song(row[0], row[1], row[2], length, row[4]))

    return songs    

def addToPlaylist(playlistid, songid):
    con = connect()
    cur = con.cursor()

    cur.execute('INSERT IGNORE INTO contains(playlistID, songid) VALUES(%s, %s)', (playlistid, songid))
    con.commit()

def removeFromPlaylist(playlistid, songid):
    con = connect()
    cur = con.cursor()

    cur.execute('SELECT COUNT(*) FROM contains WHERE playlistID=%s AND NOT songid=%s', (playlistid, songid))
    numleft = cur.fetchone()[0]

    cur.execute('DELETE FROM contains WHERE playlistID=%s AND songid=%s', (playlistid, songid))
    con.commit()

    if numleft == 0:
        deletePlaylist(playlistid)

def createPlaylist(userid, title):
    con = connect()
    cur = con.cursor()
    
    cur.execute('INSERT INTO playlists(userid, title) VALUES(%s, %s)', (userid, title))
    con.commit()

def deletePlaylist(playlistid):
    con = connect()
    cur = con.cursor()

    cur.execute('DELETE FROM playlists WHERE id=%s;', (playlistid,)) 
    cur.execute('DELETE FROM contains WHERE playlistid=%s', (playlistid,))
    con.commit()
