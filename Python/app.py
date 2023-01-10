from flask import Flask, render_template, request, session, url_for, redirect

import urllib.parse #for decoding URL

#============== SQLALCHEMY ==============

#SQL Alchemy initialization
import sqlalchemy as sqa
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sqa.create_engine("sqlite:///../Data/movie.db")

Base = declarative_base()

#SQL Alchemy Classes

#creates class for communicating with the movie table
class Movies(Base):
    __tablename__ = 'movies'
    
    id_movie = sqa.Column(sqa.Integer, primary_key=True)
    title_movie = sqa.Column(sqa.String)
    
    
    def __repr__(self):
        return "<Movie(id_movie='%i',title_movie='%s')>" % (self.id_movie, self.title_movie)

#creates class for communicating with the movie table
class Ratings(Base):
    __tablename__ = 'ratings'
    
    id_rating = sqa.Column(sqa.Integer, primary_key=True)
    id_movie = sqa.Column(sqa.Integer)
    id_user = sqa.Column(sqa.Integer)
    value_rating = sqa.Column(sqa.Float)
    timestamp_rating = sqa.Column(sqa.String)

    
    def __repr__(self):
        return "<Rating(id_rating='%i',id_movie='%i',id_user='%i',value_rating='%i',timestamp_rating='%s')>" % (self.id_rating,self.id_movie,self.id_user,self.value_rating, self.timestamp_rating)

#creates class for communicating with the movie table
class GenreList(Base):
    __tablename__ = 'genre_list'
    
    id_genre_item = sqa.Column(sqa.Integer, primary_key=True)
    id_movie = sqa.Column(sqa.Integer)
    name_genre = sqa.Column(sqa.String)
    
    
    def __repr__(self):
        return "<GenreList(id_genre_item='%i',id_movie='%i',name_genre='%s')>" % (self.id_genre_item,self.id_movie,self.id_user,self.name_genre)

#============== FLASK ==============

# Set the secret key to some random bytes. Keep this really secret!


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#REDIRECT TO HOME
@app.route("/",)
def index():
    return redirect(url_for('home'))

#MAIN HOME PAGE
@app.route("/MovieDB.io/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

#SHOWS A SIMPLE LIST OF MOVIES
@app.route("/MovieDB.io/movieList/<page>", methods=['GET', 'POST'])
def movieList(page=0):
    search="" #search term
    lsize=10 #list of elements per page
    args = request.args
    if(args):
        lsize = int(request.args['lsize'])
        search = request.args['searchBar']
        reset = request.args.get("reset")
        if(reset is None): #reset page in case of new search
            return redirect(url_for('.movieList', page=0, lsize=lsize,searchBar=search, reset='no'))
    print(args)

    movies = [] #list of movies

    i = int(page) #convert page to integer

    Session = sessionmaker(bind=engine) #session for SQAlchemy
    SQAsession = Session() #session for SQAlchemy

    #executing the query for the movie list (create a separate function later!!!)
    if(search):
        for m in SQAsession.query(Movies).filter(Movies.title_movie.like("%"+search+"%")).order_by(Movies.id_movie)[lsize*i:lsize+lsize*i]:
            movies.append(m.title_movie)
    else:
        for m in SQAsession.query(Movies).order_by(Movies.id_movie)[lsize*i:lsize+lsize*i]:
            movies.append(m.title_movie)

    next=url_for('.movieList', page=i+1, lsize=lsize,searchBar=search, reset='no')
    previous=url_for('.movieList', page=i-1,lsize=lsize,searchBar=search, reset='no')

    return render_template('movieList.html', movielist=movies, previous=previous, next=next, max=100)

if __name__ == '__main__':
    app.run(debug=True)