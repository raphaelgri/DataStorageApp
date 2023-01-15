-- Movies definition

CREATE TABLE Movies (
id_movie integer primary key,
title_movie text not null, year_movie INTEGER NOT NULL);

CREATE INDEX Movies_id_movie_IDX ON Movies (id_movie);


-- ratings definition

CREATE TABLE ratings (
id_rating integer primary key,
id_movie integer,
id_user integer,
value_rating integer,
timestamp_rating text);

CREATE INDEX ratings_id_rating_IDX ON ratings (id_rating,id_user,id_movie,value_rating);
	
-- genre_list definition

CREATE TABLE genre_list (
id_genre_item integer primary key,
id_movie integer,
name_genre text);

CREATE INDEX genre_list_id_movie_IDX ON genre_list (id_movie,id_genre_item);
	
-- reference_ratings definition

CREATE TABLE reference_ratings (
	id_reference INTEGER NOT NULL,
	average_rating REAL NOT NULL,
	timestamp_update TEXT NOT NULL
, onestar_rating INTEGER NOT NULL, twostar_rating INTEGER NOT NULL, threestar_rating INTEGER NOT NULL, fourstar_rating INTEGER NOT NULL, fivestar_rating INTEGER NOT NULL, count_rating INTEGER NOT NULL);

CREATE INDEX reference_ratings_id_reference_IDX ON reference_ratings (id_reference);

-- intersec_movies definition

CREATE TABLE intersec_movies (
	id_intersec INTEGER NOT NULL,
	id_movieA INTEGER NOT NULL,
	id_movieB INTEGER,
	count_value INTEGER NOT NULL
);

CREATE INDEX intersec_movies_id_intersec_IDX ON intersec_movies (id_intersec);

-- intersec_movies_2 definition

CREATE TABLE intersec_movies_2 (
	id_intersec_movie INTEGER NOT NULL,
	id_movieA INTEGER NOT NULL,
	id_movieB INTEGER NOT NULL,
	similarity_movie REAL NOT NULL
);

CREATE INDEX intersec_movies_2_id_intersec_movie_IDX ON intersec_movies_2 (id_intersec_movie,id_movieA,id_movieB);

-- intersec_users definition

CREATE TABLE intersec_users (
	id_intersec_user INTEGER NOT NULL,
	id_userA INTEGER NOT NULL,
	id_userB INTEGER NOT NULL,
	similarity_user REAL NOT NULL
);

CREATE INDEX intersec_users_id_intersec_user_IDX ON intersec_users (id_intersec_user,id_userA,id_userB);