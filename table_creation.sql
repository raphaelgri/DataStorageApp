 create table movies (
	id_movie integer primary key,
	title_movie text not null);


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