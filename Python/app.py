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
    years = [] #list of years
    ratings = [] #list of ratings

    i = int(page) #convert page to integer

    #executing the query for the movie list (create a separate function later!!!)
    with dataSession() as SQAsession:
        if(search):
            term = "%".join(search.split()) #searches in a more flexible way
            for m in SQAsession.query(Movies.title_movie, Movies.year_movie, ReferenceRatings.average_rating).filter(Movies.title_movie.like("%"+term+"%")).filter(Movies.id_movie == ReferenceRatings.id_reference).order_by(Movies.id_movie)[lsize*i:lsize+lsize*i]:
                movies.append(m[0])
                years.append(m[1])
                ratings.append(round(m[2],1))
        else:
            for m in SQAsession.query(Movies.title_movie, Movies.year_movie,ReferenceRatings.average_rating).filter(Movies.id_movie == ReferenceRatings.id_reference).order_by(Movies.id_movie)[lsize*i:lsize+lsize*i]:
                movies.append(m[0])
                years.append(m[1])
                ratings.append(round(m[2],1))

    next=url_for('.movieList', page=i+1, lsize=lsize,searchBar=search, reset='no')
    previous=url_for('.movieList', page=i-1,lsize=lsize,searchBar=search, reset='no')

    if(len(movies) < lsize):
        maxflag=1 #limits navigation in the list
    else:
        maxflag=0 #limits navigation in the list

    movies=zip(movies, years, ratings) #put all information into one variable for the template

    return render_template('movieList.html', movielist=movies, previous=previous, next=next, max=maxflag, page=i)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)