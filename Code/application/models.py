from .database import db


class Users(db.Model):
    user_id = db.Column(db.String,primary_key = True)
    password = db.Column(db.String, nullable = False)
    user_name = db.Column(db.String)
    user_type = db.Column(db.String, nullable = False)

class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key = True)
    album_name = db.Column(db.String, unique = True)
    songs = db.relationship("Songs", backref='Album', lazy=True)

class Songs(db.Model):
    song_id = db.Column(db.Integer, primary_key = True)
    song_name = db.Column(db.String, nullable = False,unique=True)
    lyrics = db.Column(db.String, nullable = False)
    artist= db.Column(db.String, nullable=False)
    genre= db.Column(db.String, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey(Album.album_id), nullable=False)

class Rating(db.Model):
    rating_id=db.Column(db.Integer,primary_key=True,)
    song_id = db.Column(db.Integer,db.ForeignKey(Songs.song_id),nullable=False)
    user_id = db.Column(db.String,db.ForeignKey(Users.user_id),nullable=False)  
    rating = db.Column(db.Integer,nullable=False)

class Playlist(db.Model):
    playlist_id=db.Column(db.Integer,primary_key=True)
    playlist_name=db.Column(db.String,unique=True)
    user_id = db.Column(db.String,db.ForeignKey(Users.user_id),nullable=False)

class Playlist_song(db.Model):
    playlist_song_id=db.Column(db.Integer,primary_key=True)
    playlist_id=db.Column(db.Integer,db.ForeignKey(Playlist.playlist_id),nullable=False) 
    song_id = db.Column(db.Integer,db.ForeignKey(Songs.song_id),nullable=False)   






    