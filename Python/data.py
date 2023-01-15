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
    year_movie = sqa.Column(sqa.Integer)
    
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

    
#creates class temporary reference of average rating
class ReferenceRatings(Base):
    __tablename__ = 'reference_ratings'
    
    id_reference = sqa.Column(sqa.Integer, primary_key=True)
    average_rating = sqa.Column(sqa.Float)
    timestamp_update = sqa.Column(sqa.String)
    onestar_rating = sqa.Column(sqa.Integer)
    twostar_rating = sqa.Column(sqa.Integer)
    threestar_rating = sqa.Column(sqa.Integer)
    fourstar_rating = sqa.Column(sqa.Integer)
    fivestar_rating = sqa.Column(sqa.Integer)
    count_rating = sqa.Column(sqa.Integer)
    

    
    def __repr__(self):
        return "<Rating(id_movie='%i',average_rating='%i',timestamp_update='%s')>" % (self.id_movie,self.average_rating, self.timestamp_update)

class intersec_movies(Base):
    __tablename__ = 'intersec_movies'
    
    id_intersec = sqa.Column(sqa.Integer, primary_key=True, index=True)
    id_movieA = sqa.Column(sqa.Integer)
    id_movieB = sqa.Column(sqa.Integer)
    count_value = sqa.Column(sqa.Integer)
    
    def __repr__(self):
        return "<intersec_movies(id_moviAe='%i',id_moviAe='%i',count='%i')>" % (self.id_movieA,self.id_movieB, self.count_value)

class intersec_movies_2(Base):
    __tablename__ = 'intersec_movies_2'
    
    id_intersec_movie = sqa.Column(sqa.Integer, primary_key=True, index=True)
    id_movieA = sqa.Column(sqa.Integer, index=True)
    id_movieB = sqa.Column(sqa.Integer, index=True)
    similarity_movie = sqa.Column(sqa.Integer)
    
    def __repr__(self):
        return "<intersec_movies(id_intersec_movie='%i',id_movieA='%i',id_movieB='%i', similarity='%i')>" % (self.id_intersec_movie,self.id_movieA,self.id_movieB, self.similarity_movie)

def dataSession():
    Session = sessionmaker(bind=engine) #session for SQAlchemy
    SQAsession = Session() #session for SQAlchemy
    return SQAsession