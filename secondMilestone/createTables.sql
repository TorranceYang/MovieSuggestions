CREATE TABLE IF NOT EXISTS Director
(
  id INTEGER NOT NULL PRIMARY KEY,
  first_name VARCHAR(256) NOT NULL,
  last_name VARCHAR(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS Movie
(
  id INTEGER NOT NULL PRIMARY KEY,
  title VARCHAR(256) NOT NULL,
  genre VARCHAR(256) NOT NULL,
  director INTEGER NOT NULL REFERENCES Director(id),
  date_released TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS Rating
(
  id UUID NOT NULL PRIMARY KEY,
  source_name VARCHAR(256) NOT NULL,
  movie_id INTEGER NOT NULL REFERENCES Movie(id),
  max_rating INTEGER NOT NULL,
  rating_score FLOAT NOT NULL CHECK(rating_score >= 0 AND rating_score <= max_rating)
);

--Amount grossed in is millions
CREATE TABLE IF NOT EXISTS GrossingInfo
(
  movie_id INTEGER NOT NULL REFERENCES Movie(id),
  date_timestamp TIMESTAMP NOT NULL,
  amount_grossed FLOAT NOT NULL
);
