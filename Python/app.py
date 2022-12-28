from flask import Flask, render_template, request

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

app = Flask(__name__)

@app.route("/<page>")
def hello_world(page):
    
    #connects to the database
    Session = sessionmaker(bind=engine)
    session = Session()
    i = int(page)
    html = "<p>Hello, World!</p>"
    html = "<p>Movies from " + str(1+30*i) + " to " + str(30+30*i) + "</p>"
    previous = "<a href="+str(i-1)+">Previous Page</a>"
    next =  "<a href="+str(i+1)+">Next Page</a>"
    if(i > 0): links = previous+next
    else: links = next

    
    for m in session.query(Movies).order_by(Movies.id_movie)[1+30*i:30+30*i]:
        html = html + '<p>' + m.title_movie + '</p>\n'
        
    html = html + links
    return html

if __name__ == '__main__':
    app.run(debug=True)