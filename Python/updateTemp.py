from data import *
import numpy as np


with dataSession() as session:
    #Update reference table (contains the average rating and stars count)
    max_movie = session.query(func.max(Movies.id_movie)).all()[0][0] + 1 #number of movies

    aavg = np.zeros(max_movie)
    acount = np.zeros(max_movie)
    aone = np.zeros(max_movie)
    atwo = np.zeros(max_movie)
    athree = np.zeros(max_movie)
    afour = np.zeros(max_movie)
    afive = np.zeros(max_movie)

    #queries for temporary information
    one_star = session.query(Ratings.id_movie, func.count(Ratings.value_rating)).filter(Ratings.value_rating <= 1).group_by(Ratings.id_movie).order_by(Ratings.id_movie)
    two_star = session.query(Ratings.id_movie, func.count(Ratings.value_rating)).filter(Ratings.value_rating <= 2, Ratings.value_rating > 1).group_by(Ratings.id_movie).order_by(Ratings.id_movie) 
    three_star = session.query(Ratings.id_movie, func.count(Ratings.value_rating)).filter(Ratings.value_rating <= 3, Ratings.value_rating > 2).group_by(Ratings.id_movie).order_by(Ratings.id_movie)
    four_star = session.query(Ratings.id_movie, func.count(Ratings.value_rating)).filter(Ratings.value_rating <= 4, Ratings.value_rating > 3).group_by(Ratings.id_movie).order_by(Ratings.id_movie)
    five_star = session.query(Ratings.id_movie, func.count(Ratings.value_rating)).filter(Ratings.value_rating <= 5, Ratings.value_rating > 4).group_by(Ratings.id_movie).order_by(Ratings.id_movie)
    average = session.query(Ratings.id_movie, func.avg(Ratings.value_rating), func.count(Ratings.value_rating)).group_by(Ratings.id_movie).order_by(Ratings.id_movie)


    list_values = zip(average,one_star,two_star,three_star,four_star,five_star)

    for item in list_values:
        aavg[item[0][0]] = item[0][1]
        acount[item[0][0]] = item[0][2]
        aone[item[1][0]] = item[1][1]
        atwo[item[2][0]] = item[2][1]
        athree[item[3][0]] = item[3][1]
        afour[item[4][0]] = item[4][1]
        afive[item[5][0]] = item[5][1]
    
    #delete previous data
    rfavg = session.query(ReferenceRatings) #queries references
 
    rfavg.delete() #delete reference

    session.commit()

    #load data into the database

    for i in range(0, max_movie):
        idm = i
        avg = aavg[i]
        time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        one = aone[i]
        two = atwo[i]
        three = athree[i]
        four = afour[i]
        five = afive[i]
        count = acount[i]
    
    
        rf = ReferenceRatings(id_reference=idm, 
                            average_rating=round(avg,1), 
                            timestamp_update=time, 
                            onestar_rating=one, 
                            twostar_rating=two,
                            threestar_rating=three,
                            fourstar_rating=four,
                            fivestar_rating=five,
                            count_rating=count)
        session.add(rf)
session.commit()