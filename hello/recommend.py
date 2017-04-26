import os
import urlparse
import psycopg2
from hello.moviesdb import Movie
from datetime import datetime

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

class Recommend(object):
    def __init__(self, movie_id):
        self.movie = movie_id

    def getRecommended(self):
        cursor = conn.cursor()
        cursor.execute("""
        SELECT first_ids, title, genre, plot, date_released, director_id, director_fname, director_lname, amount_grossed, movies_actors, actor_ids, ratings, sources, similarity FROM (
                (
                    SELECT
                     Movie.id AS first_ids, title, genre, plot, date_released, Director.id AS director_id, Director.first_name AS director_fname, Director.last_name as director_lname, amount_grossed, movies_actors, actor_ids, string_agg(rating_score::text, ',') AS ratings, string_agg(source_name, ',') as sources
                    FROM
                      Movie, Director, Rating, GrossingInfo, (SELECT movie_id, string_agg(first_name || ' ' || last_name, ',') as movies_actors, string_agg(actor_id::text, ',') as actor_ids FROM Actor, StarredIn WHERE actor.id = StarredIn.actor_id GROUP BY 1) AS ActorsInMovies
                    WHERE
                      Movie.director = Director.id AND Rating.movie_id = Movie.id AND GrossingInfo.movie_id = Movie.id AND Movie.id = ActorsInMovies.movie_id AND Rating.movie_id = ActorsInMovies.movie_id
                    GROUP BY
                      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

                ) AS FOO
                JOIN
                (
                     SELECT Movie.id as second_ids, similarity(
                        (
                            SELECT title || ' ' || plot || ' ' || genre || ' ' || movies_actors || ' ' ||  Director.first_name || ' ' || Director.last_name
                            FROM Movie, Director, (SELECT movie_id, string_agg(first_name || ' ' || last_name, ',') as movies_actors, string_agg(actor_id::text, ',') as actor_ids FROM Actor, StarredIn WHERE actor.id = StarredIn.actor_id GROUP BY 1) AS ActorsInMovies
                            WHERE
                              Movie.id = (%s) AND Movie.director = Director.id AND Movie.id = ActorsInMovies.movie_id
                        ),
                        (
                            title || ' ' || plot || ' ' || genre || ' ' || movies_actors || ' ' ||  Director.first_name || ' ' || Director.last_name
                        )
                    )
                    FROM Movie, Director, (SELECT movie_id, string_agg(first_name || ' ' || last_name, ',') as movies_actors, string_agg(actor_id::text, ',') as actor_ids FROM Actor, StarredIn WHERE actor.id = StarredIn.actor_id GROUP BY 1) AS ActorsInMovies
                    WHERE
                      Movie.director = Director.id AND Movie.id = ActorsInMovies.movie_id

                ) AS FOO2
                ON first_ids = second_ids
            )
            ORDER BY similarity DESC LIMIT 11;
        """, (self.movie,))

        all_rows = cursor.fetchall()
        movies = []
        for row in all_rows:
            movie = Movie(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            movie.setSimilarity("%.2f" % (float(row[13] * 100)))
            movies.append(movie)
        return movies
