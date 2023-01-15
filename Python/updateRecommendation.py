from data import *
import numpy as np

import timeit #for timing
import matplotlib.pyplot as plt
import numpy as np

import time  # for tracking progress
from rich.progress import track

def RecomendationBetaFull(session,threshold,buffersize):
    ''' This function will calculate the similarity between all movies and updated the database
    session: session used for querying
    threshold: minium number of ratings
    buffersize: max number of insertions to the database'''
    rfavg = session.query(intersec_movies) #queries references
    
    rfavg.delete() #delete intersections

    session.commit()
    
    
    #SECTION 1 GET THE FULL RATINGS TABLE
    
    #now query the whole ratings table
    query = session.query(Ratings.id_movie, Ratings.id_user).filter(Ratings.value_rating >= 3.5)

    #create to lists to store the database information
    userlist = []
    movielist = []

    for q in query:
        userlist.append(q.id_user)
        movielist.append(q.id_movie)

    usersa = np.asarray(userlist) #turn into array for faster navigation
    moviesa = np.asarray(movielist) #turn into array for faster navigation
    
    # SECTION 2 GET THE FULL MOVIE TABLE

    id_list = [] #list of all movie ids

    query = session.query(Movies)
    for q in query:
        id_list.append(q.id_movie)

    id_list = np.asarray(id_list)
    
    # SECTION 3 GET A LIST OF USERS THAT LIKE EACH MOVIE

    users_movies = [[] for _ in range((max(id_list)+1))] #create the list

    for i in track(range(0, len(moviesa))):
        users_movies[moviesa[i]].append(usersa[i]) #append the user to the list of the movie

    for i in track(range(0, len(users_movies))): #turn into sets for ease of comparison later
        users_movies[i] = set(users_movies[i])
    
    # SECTION 4 CALCULATE SIMILARITY (HOW MANY PEOPLE LIKE BOTH MOVIE A and B?)
    
    
    buffer_cnt = 0
    id_inter = 0

    for i in track(range(0, len(id_list))):
        #print("Calculating: " + str(round(((i/len(id_list))*100),2)) + "%")
        if(len(users_movies[id_list[i]]) < threshold):
            continue
        for j in range(i+1, len(id_list)):
            if(len(users_movies[id_list[j]]) < threshold):
                continue
            #moviesA.append(id_list[i])
            #moviesB.append(id_list[j])

            #moviesA.append(id_list[j])
            #moviesB.append(id_list[i])
            #intersect and count
            tmp = len(users_movies[id_list[i]].intersection(users_movies[id_list[j]]))
            tmp2 = len(users_movies[id_list[i]].union(users_movies[id_list[j]]))
            tmp = round(tmp/tmp2,2)
            #print("ID_A:" + str(id_list[i]) + " ID_B:" + str(id_list[j]) + " COUNT:" +str(tmp))
            #count.append(tmp) #two times, for both combinations
            #count.append(tmp)

            inter = intersec_movies(id_intersec=id_inter,id_movieA=int(id_list[i]), id_movieB=int(id_list[j]), count_value=tmp)
            id_inter += 1
            session.add(inter)
            buffer_cnt += 1

            if(buffer_cnt >= buffersize):
                session.commit()
                buffer_cnt = 0

    session.commit()

def RecomendationAlphaFullUsers(session,threshold,buffersize):
    ''' This function will calculate the similarity between all users and updated the database
    session: session used for querying
    threshold: minium number of ratings by the user to receive recomendations
    buffersize: max number of insertions to the database'''
    rfavg = session.query(intersec_users) #queries references
    
    rfavg.delete() #delete intersections

    session.commit()
    
    
    #SECTION 1 GET THE FULL RATINGS TABLE
    
    #now query the whole ratings table
    query = session.query(Ratings.id_movie, Ratings.id_user).filter(Ratings.value_rating >= 3.5)

    #create to lists to store the database information
    userlist = []
    movielist = []

    for q in query:
        userlist.append(q.id_user)
        movielist.append(q.id_movie)

    usersa = np.asarray(userlist) #turn into array for faster navigation
    moviesa = np.asarray(movielist) #turn into array for faster navigation
    
    # SECTION 2 GET THE ALL USERS MOVIE TABLE

    id_list = [] #list of all user ids

    query = session.query(Ratings.id_user.distinct())
    for q in query:
        id_list.append(q[0])

    id_list = np.asarray(id_list)
    
    # SECTION 3 GET A LIST OF USERS THAT LIKE EACH MOVIE

    users_movies = [[] for _ in range((max(id_list)+1))] #create the list

    for i in track(range(0, len(moviesa))):
        users_movies[usersa[i]].append(moviesa[i]) #append the user to the list of the movie

    for i in track(range(0, len(users_movies))): #turn into sets for ease of comparison later
        users_movies[i] = set(users_movies[i])
    
    # SECTION 4 CALCULATE SIMILARITY (HOW MANY PEOPLE LIKE BOTH MOVIE A and B?)
    
    
    buffer_cnt = 0
    id_inter = 0

    for i in track(range(0, len(id_list))):
        if(len(users_movies[id_list[i]]) < threshold):
            continue
        print("Calculating: " + str(round(((i/len(id_list))*100),2)) + "%")
        for j in range(i+1, len(id_list)):
            if(len(users_movies[id_list[j]]) < threshold):
                continue
            #moviesA.append(id_list[i])
            #moviesB.append(id_list[j])

            #moviesA.append(id_list[j])
            #moviesB.append(id_list[i])
            #intersect and count
            tmp = len(users_movies[id_list[i]].intersection(users_movies[id_list[j]]))
            tmp2 = len(users_movies[id_list[i]].union(users_movies[id_list[j]]))
            tmp = round(tmp/tmp2,2)
            #print("ID_A:" + str(id_list[i]) + " ID_B:" + str(id_list[j]) + " COUNT:" +str(tmp))
            #count.append(tmp) #two times, for both combinations
            #count.append(tmp)

            inter = intersec_users(id_intersec_user=id_inter,id_userA=int(id_list[i]), id_userB=int(id_list[j]), similarity_user=tmp)
            id_inter += 1
            session.add(inter)
            buffer_cnt += 1

            if(buffer_cnt >= buffersize):
                session.commit()
                buffer_cnt = 0

    session.commit()

RecomendationBetaFull(session, 1000, 1000000) #generates table for movie recommendation
RecomendationAlphaFullUsers(dataSession(), 250, 1000000) #generates table for user recommendation