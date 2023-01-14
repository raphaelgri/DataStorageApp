 create table movies (
	id_movie integer primary key,
	title_movie text not null,
	year_movie integer not null);


create table ratings (
	id_rating integer primary key,
	id_movie integer,
	id_user integer,
	value_rating integer,
	timestamp_rating text);
	
create table genre_list (
	id_genre_item integer primary key,
	id_movie integer,
	name_genre text);
	
CREATE TABLE reference_ratings (
	id_reference INTEGER NOT NULL,
	average_rating REAL NOT NULL,
	timestamp_update TEXT NOT NULL,
	onestar_rating INTEGER NOT NULL,
	twostar_rating INTEGER NOT NULL,
	threestar_rating INTEGER NOT NULL,
	fourstar_rating INTEGER NOT NULL,
	fivestar_rating INTEGER NOT NULL,
	count_rating INTEGER NOT NULL
);
CREATE INDEX reference_ratings_id_reference_IDX ON reference_ratings (id_reference);]

CREATE TABLE intersec_movies (
	id_intersec INTEGER NOT NULL,
	id_movieA INTEGER NOT NULL,
	id_movieB INTEGER NOT NULL,
	count_value INTEGER NOT NULL
);
CREATE INDEX intersec_movies_id_movieA_IDX ON intersec_movies (id_movieA,id_movieB);
