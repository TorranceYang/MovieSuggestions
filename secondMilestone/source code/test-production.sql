/*movies with rating > 80*/
SELECT movie_id, source_name rating_score FROM Rating WHERE rating_score > 80;

/*get last names and titles of 10 oldest movies*/
SELECT Director.last_name, Movie.title FROM Movie JOIN Director ON Movie.director = Director.id ORDER BY date_released LIMIT 10; 

/*get last name, title, genre from 10 newest movies*/
SELECT Director.last_name, Movie.title, Movie.genre FROM Movie JOIN Director ON Movie.director = Director.id ORDER BY date_released DESC LIMIT 10; 

/*select movies titles and genre with rating above 70*/
SELECT Movie.title, Movie.genre FROM Movie JOIN Rating ON Movie.director = Rating.id WHERE rating_score > 70;

/*select movies where grossing more than 10 million and rating is above 80*/
SELECT Movie.title, Movie.genre FROM Movie NATURAL JOIN RATING NATURAL JOIN GrossingInfo WHERE GrossingInfo > 10 AND rating_score > 80;

