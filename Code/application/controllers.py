from flask import Flask, request
from flask import render_template
from flask import current_app as app
from application.database import db
from application.models import *
from sqlalchemy import func
import matplotlib.pyplot as plt 

@app.route("/")
def intro():
    return render_template('intro.html')
#admin login
@app.route("/admin/validate",methods=["GET","POST"])
def admin_validate():
    if request.method == "GET":
        return render_template("adminlogin.html")
    elif request.method == "POST":
        user_id = request.form["userid"]
        password = request.form["password"]
        exists = db.session.query(db.session.query(Users).filter_by(user_id=user_id,
        password=password, user_type='admin').exists()).scalar()
        if (exists):
            song = Songs.query.all()
            album = Album.query.all()
            return render_template("admindashboard.html", user=user_id, song=song, 
            album=album)
        else:
            return render_template("invalid_login.html")
#user login
@app.route("/user/validate",methods=["GET","POST"])
def user_validate():
    if request.method == "GET":
        return render_template("userlogin.html")
    elif request.method == "POST":
        user_id = request.form["userid"]
        password = request.form["password"]
        exists = db.session.query(db.session.query(Users).filter_by(user_id=user_id,
        password=password, user_type='user').exists()).scalar()
        if (exists):
            song = Songs.query.all()
            album = Album.query.all()
            playlist=Playlist.query.filter_by(user_id=user_id)
            return render_template("userdashboard.html", user=user_id, song=song,album=album,playlist=playlist)
        else:
            return render_template("invalid_login.html")
#user registration
@app.route("/user/register",methods=["GET","POST"])
def user_register():
    if request.method == "GET":
        return render_template("userregistor.html")
    elif request.method == "POST":
        user_id = request.form["userid"]
        password = request.form["password"]
        username = request.form["username"]
        user_type = 'user'
        new_user = Users(user_id = user_id, password = password, user_name=username, user_type = user_type)
        db.session.add(new_user)
        db.session.commit()
        return render_template("userlogin.html")
#creator login
@app.route("/creator/validate",methods=["GET","POST"])
def creator_validate():
    if request.method == "GET":
        return render_template("creatorlogin.html")
    elif request.method == "POST":
        user_id = request.form["userid"]
        password = request.form["password"]
        exists = db.session.query(db.session.query(Users).filter_by(user_id=user_id,
        password=password, user_type='creator').exists()).scalar()
        if (exists):
            song = Songs.query.all()
            album = Album.query.all()
            return render_template("creatordashboard.html", user=user_id, song=song, 
            album=album)
        else:
            return render_template("invalid_login.html")

#creator register
@app.route("/creator/register",methods=["GET","POST"])
def creator_register():
    if request.method == "GET":
        return render_template("creatorregister.html")
    elif request.method == "POST":
        user_id = request.form["userid"]
        password = request.form["password"]
        username = request.form["username"]
        user_type = 'creator'
        new_user = Users(user_id = user_id, password = password, user_name=username, user_type = user_type)
        db.session.add(new_user)
        db.session.commit()
        return render_template("creatorlogin.html")
#user album display    
@app.route("/user/display/album/<alb_id>/<user>",methods=["GET"])
def display_by_alb(alb_id, user):
    song = Songs.query.filter_by(album_id=alb_id).all()
    alb = Album.query.filter_by(album_id=alb_id).first()
    album = Album.query.all()
    return render_template("userdashboard_album.html",   alb=alb, album=album, song=song, user=user)
#user dashboard
@app.route("/user/display/all/<user>",methods=["GET"])
def user_display_all(user):
    song = Songs.query.all()
    album =Album.query.all() 
    playlist=Playlist.query.filter_by(user_id=user)
    return render_template("userdashboard.html", user=user, song=song, album=album,playlist=playlist)
#user song display
@app.route("/user/view/add/<alb_id>/<song_id>/<user>", methods=["GET", "POST"])
def user_view_song(user, song_id, alb_id):
    if request.method == "GET":
        song = Songs.query.filter_by(song_id= song_id).first()
        print(song)
        alb =  Album.query.filter_by(album_id = alb_id).first()
        alb_name = alb.album_name
        print(alb_name)
        return render_template("usersongview.html", user = user,song=song, alb_name = alb_name)
#user playlist create
@app.route("/user/playlist/create/<user>",methods=["GET","POST"])
def create_playlist(user):
    if request.method == "GET":
        playlist=Playlist.query.all()
        return render_template("user_add_playlist.html",playlist=playlist,user=user)
    elif request.method == "POST":
        playlist_name = request.form["playlist"]
        plt=Playlist(playlist_name=playlist_name,user_id=user)
        db.session.add(plt)
        db.session.commit()
        album = Album.query.all()
        song = Songs.query.all()
        playlist=Playlist.query.filter_by(user_id=user)
        return render_template("userdashboard.html",album = album, song=song,user=user,playlist=playlist) 
#user playlist display    
@app.route("/user/playlist/display/<plt_id>/<user>",methods=["GET"])
def display_playlist(plt_id,user):
    playlist_songs=Playlist_song.query.filter_by(playlist_id=plt_id).all()
    plt=Playlist.query.filter_by(playlist_id=plt_id).first()
    song= Songs.query.filter_by().all()
    playlist=Playlist.query.filter_by().all()
    return render_template("userdashboard_playlist.html",playlist=playlist,plt=plt,song=song,playlist_songs=playlist_songs,user=user)
#user add playlist song action(POST like)
@app.route("/user/playlist/add/song/<plt_id>/<sng_id>/<user>",methods=["GET"])
def add_songs(plt_id,sng_id,user):
    exists = db.session.query(db.session.query(Playlist_song).filter_by(playlist_id=plt_id,song_id=sng_id).exists()).scalar()
    if(exists):
        return render_template("already_available.html")
    song=Songs.query.filter_by(song_id=sng_id).first()
    playlist_song=Playlist_song(playlist_id=plt_id,song_id=sng_id)
    db.session.add(playlist_song)
    db.session.commit()
    playlist_songs=Playlist_song.query.filter_by(playlist_id=plt_id).all()
    plt=Playlist.query.filter_by(playlist_id=plt_id).first()
    song= Songs.query.filter_by().all()
    playlist=Playlist.query.filter_by().all()
    return render_template("userdashboard_playlist.html",playlist=playlist,plt=plt,song=song,playlist_songs=playlist_songs,user=user)
#user add playlist song link(GET)
@app.route("/user/playlist/add/<plt_id>/<user>",methods=["GET"])
def add_song_page(plt_id,user): 
    song=Songs.query.filter_by().all()
    plt=Playlist.query.filter_by(playlist_id=plt_id).first()
    return render_template("user_add_song.html",song=song,plt=plt,user=user)

#user update playlist
@app.route("/user/playlist/update/<plt_id>/<user>", methods = ["GET","POST"])
def update_playlsit(plt_id, user):
    if request.method == "GET":
        print("playlist ID", plt_id)
        playlist = Playlist.query.filter_by(playlist_id=plt_id,user_id=user).first()
        print("playlist name", playlist.playlist_name)
        return render_template("user_update_playlist.html", plt_id=plt_id, plt_name = playlist.playlist_name,user=user)
    elif request.method == "POST":
        upd_playlist = Playlist.query.filter_by(playlist_id=plt_id,user_id= user).first()
        upd_playlist.playlist_name = request.form["playlist"]
        db.session.add(upd_playlist)
        db.session.commit()
        song = Songs.query.all()
        album = Album.query.all()
        playlist=Playlist.query.filter_by(user_id=user).all()
        return render_template("userdashboard.html", user=user,song=song, album=album,playlist=playlist)       
#user delete playlist(complete)
@app.route("/user/playlist/delete/<plt_id>/<user>", methods = ["GET","POST"])
def delete_playlist(plt_id, user):
    del_playlist_song = Playlist_song.query.filter_by(playlist_id=plt_id).all()
    for plt_song in del_playlist_song:
        db.session.delete(plt_song)
        db.session.commit()
    del_playlist = Playlist.query.filter_by(playlist_id=plt_id).first()
    db.session.delete(del_playlist)
    db.session.commit()
    album = Album.query.all()
    song=Songs.query.all()
    playlist=Playlist.query.filter_by(user_id=user)
    return render_template("userdashboard.html",album= album, user=user,song=song,playlist=playlist)
#user delete playlist song 
@app.route("/user/playlist_song/delete/<plt_id>/<sng_id>/<user>",methods=["GET"])
def delete_playlist_song(plt_id,sng_id,user):
    del_playlist_song=Playlist_song.query.filter_by(playlist_id=plt_id,song_id=sng_id).first()
    db.session.delete(del_playlist_song)
    db.session.commit()
    playlist_songs=Playlist_song.query.filter_by(playlist_id=plt_id).all()
    plt=Playlist.query.filter_by(playlist_id=plt_id).first()
    song= Songs.query.filter_by().all()
    playlist=Playlist.query.filter_by().all()
    return render_template("userdashboard_playlist.html",playlist=playlist,plt=plt,song=song,playlist_songs=playlist_songs,user=user)
#creator create album
@app.route("/creator/album/create/<user>", methods=["GET","POST"])
def create_album(user):
    print("Creator", user)
    if request.method == "GET":
        album = Album.query.all()
        return render_template("creator_add_album.html", album = album, user=user)
    elif request.method == "POST":
        album_name = request.form["album"]
        alb = Album(album_name=album_name)
        print("Before Commit")
        db.session.add(alb)
        db.session.commit()
        print("After Commit")
        album = Album.query.all()
        song = Songs.query.all()
        return render_template("creatordashboard.html",album = album, song=song,user=user)
        
#creator update album
@app.route("/creator/album/update/<alb_id>/<user>", methods = ["GET","POST"])
def update_album(alb_id, user):
    if request.method == "GET":
        print("album ID", alb_id)
        album = Album.query.filter_by(album_id=alb_id).first()
        print("album", album.album_name)
        return render_template("creator_update_album.html", alb_id=alb_id, alb_name = album.album_name, user=user)
    elif request.method == "POST":
        upd_album = Album.query.filter_by(album_id=alb_id).first()
        upd_album.album_name = request.form["album"]
        db.session.add(upd_album)
        db.session.commit()
        song = Songs.query.all()
        album = Album.query.all()
        return render_template("creatordashboard.html", user=user,song=song, album=album)
    
#creator delete album(complete)
@app.route("/creator/album/delete/<alb_id>/<user>", methods = ["GET","POST"])
def delete_album(alb_id, user):
    del_songs = Songs.query.filter_by(album_id=alb_id).all()
    for sng in del_songs:
        db.session.delete(sng)
        db.session.commit()
    del_album = Album.query.filter_by(album_id=alb_id).first()
    db.session.delete(del_album)
    db.session.commit()
    album = Album.query.all()
    song=Songs.query.all()
    return render_template("creatordashboard.html",album= album, user=user,song=song) 
#creator add song
@app.route("/creator/song/create/<user>/<alb_id>", methods = ["GET", "POST"])
def add_song(alb_id, user):
    if request.method == "GET":
        return render_template("creator_add_song.html", alb_id=alb_id, user=user)
    elif request.method == "POST":
            song_name = request.form["song"]
            lyrics = request.form["lyrics"]
            artist = request.form["artist"]
            genre = request.form["genre"]
            album_id = alb_id
            sng = Songs(song_name = song_name, lyrics=lyrics,artist=artist,genre=genre, album_id=album_id)
            exists = db.session.query(db.session.query(Songs).filter_by(song_name=song_name,
            lyrics=lyrics, artist=artist,genre=genre).exists()).scalar()
            if(exists):
                return render_template("already_available.html")
            else:  
                db.session.add(sng)
                db.session.commit()
                song =Songs.query.all()
                album = Album.query.all()
                return render_template("creatordashboard.html", user=user,song=song, album=album)
#creator delete song
@app.route("/creator/song/delete/<sng_id>/<user>", methods = ["GET"])
def del_song(sng_id, user):
        del_song =Songs.query.filter_by(song_id=sng_id).first()
        db.session.delete(del_song)
        db.session.commit()
        song=Songs.query.all()
        album = Album.query.all()
        return render_template("creatordashboard.html", creator=user,song=song, album=album,user=user)
#creator update song
@app.route("/creator/song/update/<sng_id>/<user>", methods = ["GET", "POST"])
def update_song(sng_id, user):
    if request.method == "GET":
        sng = Songs.query.filter_by(song_id=sng_id).first()
        return render_template("creator_update_song.html", song=sng, user=user)
    elif request.method == "POST":
        upd_song = Songs.query.filter_by(song_id=sng_id).first()
        upd_song.song_name = request.form["song"]
        upd_song.artist=request.form["artist"]
        upd_song.genre=request.form["genre"]
        upd_song.lyrics = request.form["lyrics"]
        db.session.add(upd_song)
        db.session.commit()
        song = Songs.query.all()
        album = Album.query.all()
        return render_template("creatordashboard.html", user=user,song=song, album=album)
#admin user count
@app.route("/admin/user/count/user",methods=["GET"])
def user_count():
    user_count=Users.query.filter_by(user_type='user').count()
    user=Users.query.filter_by(user_type='user').all()
    return render_template("user_statistics.html",user_count=user_count,user_type="user")
#admin creator count
@app.route("/admin/creator/count",methods=["GET"])
def creator_count():
    creator_count=Users.query.filter_by(user_type='creator').count()
    creator=Users.query.filter_by(user_type='creator').all()
    return render_template("creator_statistics.html",user_count=creator_count,user_type="creator")
#admin album count
@app.route("/admin/album/count/all",methods=["GET"])
def album_count():
    album_count=Album.query.filter_by().count()
    album=Album.query.filter_by().all()
    song=Songs.query.filter_by().all()
    return render_template("album_statistics.html",album_count=album_count,album=album,user_type="album",song=song)
#admin user blacklist
@app.route("/user/delete/<user_id>",methods=["GET"])
def user_flag(user_id):
    del_user=Users.query.filter_by(user_id=user_id).first()
    db.session.delete(del_user)
    db.session.commit()
    user_count=Users.query.filter_by(user_type='user').count()
    user=Users.query.filter_by(user_type='user').all()
    return render_template("user_statistics.html",user_count=user_count,user=user,user_type="user")
#admin creator blacklist
@app.route("/creator/delete/<user_id>",methods=["GET"])
def creator_flag(user_id):
    del_user=Users.query.filter_by(user_id=user_id).first()
    db.session.delete(del_user)
    db.session.commit()
    user_count=Users.query.filter_by(user_type='user').count()
    user=Users.query.filter_by(user_type='user').all()
    return render_template("creator_statistics.html",user_count=user_count,user=user,user_type="creator")

#admin flag/delete album    
@app.route("/admin/album/delete/<alb_id>", methods = ["GET","POST"])
def flag_album(alb_id):
    del_songs = Songs.query.filter_by(album_id=alb_id).all()
    for sng in del_songs:
        db.session.delete(sng)
        db.session.commit()
    del_album = Album.query.filter_by(album_id=alb_id).first()
    db.session.delete(del_album)
    db.session.commit()
    song=Songs.query.filter_by().all()
    album_count=Album.query.filter_by().count()
    album=Album.query.filter_by().all()
    return render_template("album_statistics.html",album_count=album_count,album=album,user_type="album",song=song)
#admin song blacklist
@app.route("/admin/song/delete/<alb_id>/<sng_id>",methods=["GET","POST"])
def flag_song(alb_id,sng_id):
    del_song=Songs.query.filter_by(album_id=alb_id,song_id=sng_id).first()
    db.session.delete(del_song)
    db.session.commit()
    song=Songs.query.filter_by().all()
    album_count=Album.query.filter_by().count()
    album=Album.query.filter_by().all()
    return render_template("album_statistics.html",album_count=album_count,album=album,user_type="album",song=song)
#user song search(genre)
@app.route("/song/search/genre/<user>",methods=["GET","POST"])
def search_genre(user):
    if request.method=="POST":
        genre=request.form["genre"]
        genre_song = Songs.query.filter_by(genre=genre).all()
        return render_template("genre_songs.html",genre_song=genre_song,genre=genre,user=user)
#user song search(artist)    
@app.route("/song/search/artist/<user>",methods=["GET","POST"])
def search_artist(user):
    if request.method=="POST":
        artist=request.form["artist"]
        artist_song = Songs.query.filter_by(artist=artist).all()
        return render_template("artist_song.html",artist_song=artist_song,artist=artist,user=user)
#user song rating    
@app.route("/song/view/rating/<sng_id>/<user>",methods=["GET","POST"])
def song_rating(sng_id,user):
    if request.method=="GET":
        rating_temp =Rating.query.filter_by(song_id=sng_id).all()
        rating_present=Rating.query.filter_by(song_id=sng_id,user_id=user).count()
        if rating_present == 0:
            rtg=Rating(song_id=sng_id,user_id=user,rating=0)
            db.session.add(rtg)
            db.session.commit()        
        rating_result=sum(rate.rating for rate in rating_temp)
        rating_count=Rating.query.filter_by(song_id=sng_id).count()
        if rating_count == 0:
            rating_avg = 0
            song=Songs.query.filter_by(song_id=sng_id).first()
            return render_template("user_rating.html",rating_avg=rating_avg,song=song,user=user)
        else:
            rating_avg=rating_result/rating_count
            song=Songs.query.filter_by(song_id=sng_id).first()
            return render_template("user_rating.html",rating_avg=rating_avg,song=song,user=user)
    
    elif request.method=="POST":
        rate=request.form["rating"]
        exists = db.session.query(db.session.query(Rating).filter_by(user_id=user,
        song_id=sng_id).exists()).scalar()
        if(exists):
            rtg=Rating.query.filter_by(user_id=user,song_id=sng_id).first()
            db.session.delete(rtg)
            db.session.commit()
            rtg=Rating(song_id=sng_id,user_id=user,rating=rate)
            db.session.add(rtg)
            db.session.commit()
            album = Album.query.all()
            song=Songs.query.all()
            playlist=Playlist.query.filter_by(user_id=user)
            return render_template("userdashboard.html",album= album, user=user,song=song,playlist=playlist)
        else:
            rtg=Rating(song_id=sng_id,user_id=user,rating=rate)
            db.session.add(rtg)
            db.session.commit()
            album = Album.query.all()
            song=Songs.query.all()
            playlist=Playlist.query.filter_by(user_id=user)
            return render_template("userdashboard.html",album= album, user=user,song=song,playlist=playlist)

@app.route("/admin/user/back/user",methods=["GET"])
def admin_back():
    song = Songs.query.all()
    album = Album.query.all()
    return render_template("admindashboard.html", song=song, album=album)



