from flask import Flask, render_template, request, session, url_for, redirect

import urllib.parse #for decoding URL

from data import *

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
    #initialize default variables
    glist = []
    #check if session values are already generated
    if not session.get("GenreList"):
        with dataSession() as SQAsession:
            glist = [m[0].strip('\n') for m in (SQAsession.query(GenreList.name_genre.distinct()))]
            session['GenreList'] = glist
    else:
        glist = session['GenreList']
    return render_template('home.html', genreList=glist)

#SHOWS A SIMPLE LIST OF MOVIES
@app.route("/MovieDB.io/movieList/<page>", methods=['GET', 'POST'])
def movieList(page=0):
    #initialize default variables
    glist = []
    #check if session values are already generated
    if not session.get("GenreList"):
        with dataSession() as SQAsession:
            glist = [m[0].strip('\n') for m in (SQAsession.query(GenreList.name_genre.distinct()))]
            session['GenreList'] = glist
    else:
        glist = session['GenreList']

    
    search="" #search term
    lsize=10 #list of elements per page
    ordercolumn='id'
    descasc='desc'
    genre='all'

    #request processing
    args = request.args
    orderdict = {   "id" : Movies.id_movie,
                    "title" : Movies.title_movie,
                    "year" : Movies.year_movie,
                    "rating" : ReferenceRatings.average_rating}
    
    if(args):
        lsize = int(request.args['lsize'])
        search = request.args['searchBar']
        reset = request.args.get("reset")
        ordercolumn = request.args.get("orderby") # what will be used to order
        descasc = request.args.get("descasc") # what will be used to order
        genre = request.args.get("genre") #what genre will be used to filter
        if(genre is None):
            genre='all'
        if(reset is None): #reset page in case of new search
            return redirect(url_for('.movieList', page=0, lsize=lsize,searchBar=search, reset='no', orderby=ordercolumn, descasc=descasc, genre=genre))
    
    if(descasc == 'desc'):
        order_value = orderdict[ordercolumn].desc()
    else:
        order_value = orderdict[ordercolumn]

    print(args)

    #databse processing
    movies = [] #list of movies
    years = [] #list of years
    ratings = [] #list of ratings
    counts = [] #list of rating count

    i = int(page) #convert page to integer

    #executing the query for the movie list (create a separate function later!!!)
    with dataSession() as SQAsession:
        if(genre =='all'):
            if(search):
                term = "%".join(search.split()) #searches in a more flexible way
                query = SQAsession.query(Movies.title_movie, Movies.year_movie, ReferenceRatings.average_rating, ReferenceRatings.count_rating).filter(Movies.title_movie.like("%"+term+"%")).filter(Movies.id_movie == ReferenceRatings.id_reference).order_by(order_value)[lsize*i:lsize+lsize*i]
            else:
                query = SQAsession.query(Movies.title_movie, Movies.year_movie,ReferenceRatings.average_rating, ReferenceRatings.count_rating).filter(Movies.id_movie == ReferenceRatings.id_reference).order_by(order_value)[lsize*i:lsize+lsize*i]
        else:
            if(search):
                term = "%".join(search.split()) #searches in a more flexible way
                query = SQAsession.query(Movies.title_movie, Movies.year_movie, ReferenceRatings.average_rating, ReferenceRatings.count_rating, GenreList.id_movie, GenreList.name_genre).filter(Movies.title_movie.like("%"+term+"%")).filter(Movies.id_movie == ReferenceRatings.id_reference, Movies.id_movie == GenreList.id_movie, GenreList.name_genre == genre).order_by(order_value)[lsize*i:lsize+lsize*i]
            else:
                query = SQAsession.query(Movies.title_movie, Movies.year_movie,ReferenceRatings.average_rating, ReferenceRatings.count_rating, GenreList.id_movie, GenreList.name_genre).filter(Movies.id_movie == ReferenceRatings.id_reference, Movies.id_movie == GenreList.id_movie, GenreList.name_genre == genre).order_by(order_value)[lsize*i:lsize+lsize*i]

        for m in query:
            movies.append(m[0])
            years.append(m[1])
            ratings.append(round(m[2],1))
            counts.append(m[3])

    len_list = len(movies)
    movies=zip(movies, years, ratings, counts) #put all information into one variable for the template

    #view rendering

    next=url_for('.movieList', page=i+1, lsize=lsize,searchBar=search, reset='no',orderby=ordercolumn, descasc=descasc)
    previous=url_for('.movieList', page=i-1,lsize=lsize,searchBar=search, reset='no',orderby=ordercolumn, descasc=descasc)

    if(len_list < lsize):
        maxflag=1 #limits navigation in the list
    else:
        maxflag=0 #limits navigation in the list

    return render_template('movieList.html', movielist=movies, previous=previous, next=next, max=maxflag, page=i,genreList=glist,search=search)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)