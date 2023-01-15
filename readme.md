# Data Storage Project: MovieDB.io

## About

### Structure
This project was built using python and flask for generating a user interface. The connection with the database is done via SQLalchemy that maps the database to classes. The database is a sqlite database and is loaded using the loadData.py script. The average ratings are generated by updateTemp.py and the similarity values for the recommendation system are generated with updateRecommendation.py. The application itself is started by running flask in the ./python directory and is contained in app.py. All the HTML templates are located in /templates and the CSS is in /static/style.

### Navigation

The project allows the user to list movies, rank them according to: id, year, rating and title. It is also possible to filter the Genre of the movie and obtain the best rated movies of each genre. In all pages it is possible to search for a specific movie title and filter the results. There are four possible pages a user can access:
-Home
-Movie List
-Movie Page
-User Page

#### Home
Contains only the basic elements, allowing the user to navigate the application.

#### Movie List
Shows a list of movies, and is shown everytime a user inputs a search term in the search bar.

#### Movie Page
An individual page generated for each movie, contains the count of ratings and when the movie has enough ratings, a list of recommended movies.

#### User Page
An individual page generated for each user, contains a list with the movies the user liked and another list with recommended movies.

## Database

The database is built using the table_creating.sql script and contains 7 different tables. The database is the file Data/movie.db available [here](https://1drv.ms/u/s!AkuZVmKUlu2HjaN5dOuWKIkRKYtqlA?e=rjDycO) or [here]
-Movies
-Ratings
-Genre_List
-Reference_ratings *
-Intersec_users *
-Intersec_movies *
-Intersec_movies_2 *

*Those tables are only references to speed up the application and are to be updated by the scripts on a regular basis.

### Movies
The movie table contain the movie id, the movie's title and its year.

### Ratings
The ratings table will contain an id for each row (so it have a primary key), the movie id, the user id, the rating and the timestamp.

### Genre_list
The table contains an id for each row (so it have a primary key), the movie id and the genre name.

### Reference_ratings *
This table is generated so the calculation of averages only happens once (since it is computationaly costly). It contains the reference id (same as movie id), average rating, count of 1, 2,3 ,4 and 5 star ratings and the count of ratings for each movie.

### intersec_users
This table contain the similarity for each pair of users A and B. It is also generated so it saves computational resources. Not all pairs will be contained in this table, as there is a threshold of number of ratings per user.

### intersec_movies
This table contain the similarity for each pair of movies A and B. It is also generated so it saves computational resources. Not all pairs will be contained in this table, as there is a threshold of number of ratings per user. The similarity in this case is a simple count of how many users like both movie A and movie B.

### intersec_movies_2
This table contain the similarity for each pair of movies A and B. It is also generated so it saves computational resources. Not all pairs will be contained in this table, as there is a threshold of number of ratings per user. The similarity in this case is calculated as the proportion of users that like both Movie A and Movie B. Explained further in the Recommendation section.

## Recommendation
To perform the recommendation of movies, the updateRecommendation script will generate the interse tables for movies and for users. The similarity is calculated as follows:

### For Movies
How many users liked (star >= 3.5) both Movie A and Movie B, divided by how many users like Movie A or Movie B. In other words, is the intersection divided by the union. The intuition behind that is to check how similar the pool of users that like a movie is to another.

### For Users
For users the same operation applies, but instead of creating groups of users, the scrip will create groups of movies liked by each user. The final recommendation is the union of the 3 most similar users, excluding all the movies already rated by the user.

### Ranking recommendations

After retrieving the most similar movies, simply show the ranked list ordered by the similarity.
For the recomendation of movies to users, the order is given by the ratings of each movie.
