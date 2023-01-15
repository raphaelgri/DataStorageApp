from data import *
import numpy as np


with dataSession() as session:
    #load the movies data into the movies table

    #open the file
    with open("Data/ml-25m/movies.csv", encoding='utf-8') as f:
        f.readline() #skip first line
        count=1
        for line in f:
            items = line.split(sep=',')
            movieid = items[0]
            #process the title and year
            title = (",".join(items[1:-1])).strip('\"').strip() #join all different items inside the title
            print(title)
            if(title[-6:][1:-1].isnumeric()): #check if year is correct
                year = int(title[-6:][1:-1]) #gets the year from the title
                title = title[:-7] #removes the year from the title if it is ther
            else:
                year = -1 #sets as -1 for unknown year
            
            #creates object
            mv = Movies(id_movie=int(movieid), title_movie=title, year_movie=year)
            #adds to section
            session.add(mv)
            genres = items[-1].split(sep="|")
            for genre in genres:
                genre = genre.strip('\n').strip('\n')
                gl = GenreList(id_genre_item=count,id_movie=int(movieid),name_genre=genre)
                count+=1
                session.add(gl)
            if(count%10000 == 0): 
                print(count)
                session.commit()
        session.commit()
        
    #load the ratings data into the rating table

    #open the file

    with open("Data/ml-25m/ratings.csv", encoding='utf-8') as f:
        f.readline() #skip first line
        count=1
        for line in f:
            items = line.split(sep=',')
            userid = items[0]
            movieid = items[1]
            rating = items[2]
            timestamp = items[3]
            #print(movieid)
            rt = Ratings(id_rating=count, id_movie=int(movieid), id_user=int(userid), value_rating=float(rating), timestamp_rating=timestamp)
            count+=1
            #session.add(rt)
            if(count%1000000 == 0): 
                print(count)
                #session.commit()
        #session.commit()