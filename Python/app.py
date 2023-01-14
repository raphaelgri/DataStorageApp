from flask import Flask, render_template, request, session, url_for, redirect
import numpy as np

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
    idms = [] #list of movie ids

    i = int(page) #convert page to integer

    #executing the query for the movie list (create a separate function later!!!)
    with dataSession() as SQAsession:
        if(genre =='all'):
            if(search):
                term = "%".join(search.split()) #searches in a more flexible way
                query = SQAsession.query(Movies.title_movie, Movies.year_movie, ReferenceRatings.average_rating, ReferenceRatings.count_rating, Movies.id_movie).filter(Movies.title_movie.like("%"+term+"%")).filter(Movies.id_movie == ReferenceRatings.id_reference).order_by(order_value, ReferenceRatings.count_rating.desc())[lsize*i:lsize+lsize*i]
                nrows = SQAsession.query(Movies.title_movie, Movies.year_movie, ReferenceRatings.average_rating, ReferenceRatings.count_rating, Movies.id_movie).filter(Movies.title_movie.like("%"+term+"%")).filter(Movies.id_movie == ReferenceRatings.id_reference).order_by(order_value, ReferenceRatings.count_rating.desc()).count()
            else:
                query = SQAsession.query(Movies.title_movie, Movies.year_movie,ReferenceRatings.average_rating, ReferenceRatings.count_rating, Movies.id_movie).filter(Movies.id_movie == ReferenceRatings.id_reference).order_by(order_value, ReferenceRatings.count_rating.desc())[lsize*i:lsize+lsize*i]
                nrows = SQAsession.query(Movies.title_movie, Movies.year_movie,ReferenceRatings.average_rating, ReferenceRatings.count_rating, Movies.id_movie).filter(Movies.id_movie == ReferenceRatings.id_reference).order_by(order_value, ReferenceRatings.count_rating.desc()).count()
        else:
            if(search):
                term = "%".join(search.split()) #searches in a more flexible way
                query = SQAsession.query(Movies.title_movie, Movies.year_movie, ReferenceRatings.average_rating, ReferenceRatings.count_rating, GenreList.id_movie, GenreList.name_genre).filter(Movies.title_movie.like("%"+term+"%")).filter(Movies.id_movie == ReferenceRatings.id_reference, Movies.id_movie == GenreList.id_movie, GenreList.name_genre == genre).order_by(order_value, ReferenceRatings.count_rating.desc())[lsize*i:lsize+lsize*i]
                nrows = SQAsession.query(Movies.title_movie, Movies.year_movie, ReferenceRatings.average_rating, ReferenceRatings.count_rating, GenreList.id_movie, GenreList.name_genre).filter(Movies.title_movie.like("%"+term+"%")).filter(Movies.id_movie == ReferenceRatings.id_reference, Movies.id_movie == GenreList.id_movie, GenreList.name_genre == genre).order_by(order_value, ReferenceRatings.count_rating.desc()).count()
            else:
                query = SQAsession.query(Movies.title_movie, Movies.year_movie,ReferenceRatings.average_rating, ReferenceRatings.count_rating, GenreList.id_movie, GenreList.name_genre).filter(Movies.id_movie == ReferenceRatings.id_reference, Movies.id_movie == GenreList.id_movie, GenreList.name_genre == genre).order_by(order_value, ReferenceRatings.count_rating.desc())[lsize*i:lsize+lsize*i]
                nrows = SQAsession.query(Movies.title_movie, Movies.year_movie,ReferenceRatings.average_rating, ReferenceRatings.count_rating, GenreList.id_movie, GenreList.name_genre).filter(Movies.id_movie == ReferenceRatings.id_reference, Movies.id_movie == GenreList.id_movie, GenreList.name_genre == genre).order_by(order_value, ReferenceRatings.count_rating.desc()).count()

        

        for m in query:
            movies.append(m[0])
            years.append(m[1])
            ratings.append(round(m[2],1))
            counts.append(m[3])
            idms.append(m[4])

    len_list = len(movies)
    movies=zip(movies, years, ratings, counts,idms) #put all information into one variable for the template

    #view rendering

    next=url_for('.movieList', page=i+1, lsize=lsize,searchBar=search, reset='no',orderby=ordercolumn, descasc=descasc, genre=genre)
    previous=url_for('.movieList', page=i-1,lsize=lsize,searchBar=search, reset='no',orderby=ordercolumn, descasc=descasc, genre=genre)
    #generate paged links
    pagenum = round(nrows/lsize) # number of pages
    pagelinks = [] #list of links to be displayed
    pageidexes = []
    lbound = max(int(page)-5, 0) #lower boundary of the list
    ubound = min(int(lbound)+11, pagenum) #upper boundary of the list
    for k in range(lbound, ubound): 
        pagelinks.append(url_for('.movieList', page=k, lsize=lsize,searchBar=search, reset='no',orderby=ordercolumn, descasc=descasc, genre=genre))
        pageidexes.append(k)

    if(len_list < lsize):
        maxflag=1 #limits navigation in the list
    else:
        maxflag=0 #limits navigation in the list

    pageitems = zip(pagelinks, pageidexes)

    return render_template('movieList.html', movielist=movies, previous=previous, next=next, max=maxflag, page=i,genreList=glist,search=search, pageitems=pageitems)

@app.route("/MovieDB.io/moviePage/<movieid>", methods=['GET', 'POST'])
def moviePage(movieid=0):

    averages = []
    counts = []
    ones = []
    twos = []
    threes = []
    fours = []
    fives = []

    #query for movie information
    with dataSession() as SQAsession:
        query = SQAsession.query(ReferenceRatings.id_reference,
                         ReferenceRatings.average_rating, 
                         ReferenceRatings.count_rating, 
                         ReferenceRatings.onestar_rating, 
                         ReferenceRatings.twostar_rating,
                         ReferenceRatings.threestar_rating,
                         ReferenceRatings.fourstar_rating,
                         ReferenceRatings.fivestar_rating).filter(ReferenceRatings.id_reference == movieid)
        for q in query:
            averages = round(q[1],1)
            counts = q[2]
            ones = q[3]
            twos = q[4]
            threes = q[5]
            fours = q[6]
            fives =q[7]
      
    with dataSession() as SQAsession:   
        movieq = SQAsession.query(Movies).filter(Movies.id_movie == movieid)
        
        references = [averages, counts, ones, twos, threes, fours, fives]
    print(references)

    #create bars for rating counts
    if(references[1] > 0):
        bars = [".bar-5 {width: " + str(round((references[6] / references[1])*100)) + "%; height: 18px; background-color: #33cc33;}",
                ".bar-4 {width: " + str(round((references[5] / references[1])*100)) + "%; height: 18px; background-color: #99ff33;}",
                ".bar-3 {width: " + str(round((references[4] / references[1])*100)) + "%; height: 18px; background-color: #ffff00;}",
                ".bar-2 {width: " + str(round((references[3] / references[1])*100)) + "%; height: 18px; background-color: #ff9933;}",
                ".bar-1 {width: " + str(round((references[2] / references[1])*100)) + "%; height: 18px; background-color: #ff0000;}"]
    else:
                bars = [".bar-5 {width: " + str(0) + "%; height: 18px; background-color: #33cc33;}",
                        ".bar-4 {width: " + str(0) + "%; height: 18px; background-color:  #99ff33;}",
                        ".bar-3 {width: " + str(0) + "%; height: 18px; background-color:  #ffff00;}",
                        ".bar-2 {width: " + str(0) + "%; height: 18px; background-color:  #ff9933;}",
                        ".bar-1 {width: " + str(0) + "%; height: 18px; background-color:  #ff0000;}"]
    st = "<style>"
    cst = "</style>"



    #create list of recommended movies

    list_movies = []
    list_count = []

    with dataSession() as SQAsession:
        intersecA = SQAsession.query(intersec_movies).filter(intersec_movies.id_movieA == movieid)
        for row in intersecA:
            list_movies.append(row.id_movieB)
            list_count.append(row.count_value)


    with dataSession() as SQAsession:
        intersecB = SQAsession.query(intersec_movies).filter(intersec_movies.id_movieB == movieid)
        for row in intersecB:
            list_movies.append(row.id_movieA)
            list_count.append(row.count_value)

    list_movies = np.asarray(list_movies)
    list_count = np.asarray(list_count)

    list_movies = np.flip(list_movies[np.argsort(list_count)])
    list_count = np.flip(np.sort(list_count))

    list_titles = []

    for k in range(0,5):
        with dataSession() as SQAsession:
            query = SQAsession.query(Movies.title_movie).filter(Movies.id_movie == int(list_movies[k])).all()
            list_titles.append(query[0][0])

    list_recommend = zip(list_movies[0:5], list_titles)


    return render_template('moviePage.html', movieid=movieid, references=references, title=movieq[0].title_movie, bars=bars, styletag=st, closestyletag=cst, recommended=list_recommend)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)