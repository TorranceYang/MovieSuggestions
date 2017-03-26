CREATE TABLE Director
(
  id INTEGER NOT NULL PRIMARY KEY,
  first_name VARCHAR(256) NOT NULL,
  last_name VARCHAR(256) NOT NULL
);

CREATE TABLE Movie
(
  id INTEGER NOT NULL PRIMARY KEY,
  title VARCHAR(256) NOT NULL,
  genre VARCHAR(256) NOT NULL,
  director INTEGER NOT NULL REFERENCES Director(id),
  date_released VARCHAR(8) NOT NULL
);

CREATE TABLE Rating
(
  id INTEGER NOT NULL PRIMARY KEY,
  source_name VARCHAR(256) NOT NULL,
  movie_id INTEGER NOT NULL REFERENCES Movie(id),
  max_rating INTEGER NOT NULL,
  rating_score FLOAT NOT NULL CHECK(rating_score >= 0 AND rating_score <= max_rating)
);

--Amount grossed in is millions
CREATE TABLE GrossingInfo
(
  movie_id INTEGER NOT NULL REFERENCES Movie(id),
  date_timestamp VARCHAR(8) NOT NULL,
  amount_grossed FLOAT NOT NULL
);

-- Populate databases with data
INSERT INTO Director VALUES (1, 'Manoj', 'Shyamalan');
INSERT INTO Director VALUES (2, 'Michael', 'Bay');
INSERT INTO Director VALUES (3, 'Christopher', 'Nolan');
INSERT INTO Director VALUES (4, 'Stanley', 'Kubrick');

INSERT INTO Movie VALUES (1, 'The Sixth Sense', 'thriller', 1, '19990806');
INSERT INTO Movie VALUES (2, 'Transformers', 'action', 2, '20070603');
INSERT INTO Movie VALUES (3, 'Inception', 'thriller', 3, '20100713');
INSERT INTO Movie VALUES (4, 'A Clockwork Orange', 'dystopian', 4, '19720202');

INSERT INTO Rating VALUES (1, 'Rotten Tomatoes', 1, 100, 85);
INSERT INTO Rating VALUES (2, 'Rotten Tomatoes', 2, 100, 86);
INSERT INTO Rating VALUES (3, 'Rotten Tomatoes', 3, 100, 57);
INSERT INTO Rating VALUES (4, 'Rotten Tomatoes', 4, 100, 90);
INSERT INTO Rating VALUES (5, 'IMDB', 1, 10, 8.1);
INSERT INTO Rating VALUES (6, 'IMDB', 2, 10, 7.1);
INSERT INTO Rating VALUES (7, 'IMDB', 3, 10, 8.8);
INSERT INTO Rating VALUES (8, 'IMDB', 4, 10, 8.3);

INSERT INTO GrossingInfo VALUES (1, '20170227', 627.8);
INSERT INTO GrossingInfo VALUES (2, '20170227', 709.7);
INSERT INTO GrossingInfo VALUES (3, '20170227', 825.5);
INSERT INTO GrossingInfo VALUES (4, '20170227', 26.6);


--Find a thriller that is rated above an 8.3 on IMDB
SELECT title
FROM Movie, Rating
WHERE genre = 'thriller'
AND Movie.id = Rating.movie_id
AND source_name = 'IMDB'
AND rating_score > 8.3;

--Find all movies released in the 2000s
SELECT title
FROM Movie
WHERE date_released > '20000000';

--Find all movies who grossed over a 100 million dollars
SELECT title
FROM Movie, GrossingInfo
WHERE Movie.id = GrossingInfo.movie_id
AND amount_grossed > 100;
