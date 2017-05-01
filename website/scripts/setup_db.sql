CREATE DATABASE final_project;
USE final_project;

DROP TABLE contains;
DROP TABLE playlists;
DROP TABLE songs;
DROP TABLE users;

CREATE TABLE users(
    id INT AUTO_INCREMENT NOT NULL,
    email VARCHAR(128) UNIQUE NOT NUlL,
    pwhash BINARY(60) NOT NULL,
    priviledges VARCHAR(8) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE songs(
    id INT AUTO_INCREMENT NOT NULL,
    title VARCHAR(128) NOT NULL,
    artist VARCHAR(128) NOT NULL,
    length INT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE playlists(
    id INT AUTO_INCREMENT NOT NULL,
    userID INT NOT NULL,
    title VARCHAR(128) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(userID) REFERENCES users(id)
);

CREATE TABLE contains(
    playlistID INT NOT NULL,
    songID INT NOT NULL,
    PRIMARY KEY(playlistID, songID),
    FOREIGN KEY(playlistID) REFERENCES playlists(id),
    FOREIGN KEY(songID) REFERENCES songs(id)
);
