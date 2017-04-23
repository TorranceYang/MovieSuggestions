import os
import urlparse
import psycopg2
from hello.moviesdb import Movie

class Search:
    """Class for differnet types of searches"""
    def connect(self):
        """connect to database using env variables"""
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])
        return psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

    def __init__(self, search_term, category):
        self.conn = self.connect()
        self.search = search_term.lower()
        self.category = category

    def getSearchResults(self):
        """Do something with self.search to query"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT
         Movie.id, title, genre, plot, date_released, Director.id, Director.first_name, Director.last_name, amount_grossed, movies_actors, actor_ids, string_agg(rating_score::text, ',') AS ratings, string_agg(source_name, ',') as sources
        FROM
          Movie, Director, Rating, GrossingInfo, (SELECT movie_id, string_agg(first_name || ' ' || last_name, ',') as movies_actors, string_agg(actor_id::text, ',') as actor_ids FROM Actor, StarredIn WHERE actor.id = StarredIn.actor_id GROUP BY 1) AS ActorsInMovies
        WHERE
          Movie.director = Director.id AND Rating.movie_id = Movie.id AND GrossingInfo.movie_id = Movie.id AND Movie.id = ActorsInMovies.movie_id AND Rating.movie_id = ActorsInMovies.movie_id
          AND LOWER(Movie.title) LIKE LOWER('%""" + self.search + """%'
        ) GROUP BY
          1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
        """)

        all_rows = cursor.fetchall()
        movies = []
        for row in all_rows:
            movies.append(Movie(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]))
        return movies

    def sortResults(self, results):
        """sort query results"""
