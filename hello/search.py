import os
import urlparse
import psycopg2
from hello.moviesdb import Movie
from datetime import datetime

class Search(object):
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

    def __init__(self, title, genre, director, actor, rating_source, rating_value, released, grossed, plot):
        self.conn = self.connect()
        self.movie_list = []
        
        #There should be a better way to do this, but this will work for the time being
        if title is not None:
            self.title = title.lower()
        else:
            self.title = ""

        if genre is not None:
            self.genre = genre.lower()
        else:
            self.genre = ""

        if director is not None:
            self.director = director.lower()
        else:
            self.director = ""

        if actor is not None:
            self.actor = actor.lower()
        else:
            self.actor = ""

        if rating_source is not None:
            self.rating_source = rating_source.lower()
        else:
            self.rating_source = ""

        if rating_value is not None and len(rating_value) > 0:
            self.rating_value = rating_value.lower()
        else:
            self.rating_value = 0

        if released is not None and len(released) > 0:
            self.released = datetime.strptime(released, '%Y')
        else:
            self.released = datetime.strptime("1920", '%Y')

        if grossed is not None and len(grossed) > 0:
            self.grossed = grossed.lower()
        else:
            self.grossed = 0

        if plot is not None:
            self.plot = plot.lower()
        else:
            self.plot = ""


    def getMovieQuery(self):
        """a common query with a few changes"""

        cursor = self.conn.cursor()

        commonQuery = """
        SELECT
         Movie.id, title, genre, plot, date_released, Director.id, Director.first_name, Director.last_name, amount_grossed, movies_actors, actor_ids, string_agg(rating_score::text, ',') AS ratings, string_agg(source_name, ',') as sources
        FROM
          Movie, Director, Rating, GrossingInfo, (SELECT movie_id, string_agg(first_name || ' ' || last_name, ',') as movies_actors, string_agg(actor_id::text, ',') as actor_ids FROM Actor, StarredIn WHERE actor.id = StarredIn.actor_id GROUP BY 1) AS ActorsInMovies
        WHERE
          Movie.director = Director.id AND Rating.movie_id = Movie.id AND GrossingInfo.movie_id = Movie.id AND Movie.id = ActorsInMovies.movie_id AND Rating.movie_id = ActorsInMovies.movie_id
          """

        groupingQuery = """
        GROUP BY
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
        """

        # Generates custom query
        searchParamters = "AND LOWER(title) LIKE \'%%" + self.title + "%%' AND LOWER(genre) LIKE '%%" + self.genre + "%%' AND LOWER(Director.first_name || ' ' || Director.last_name) LIKE '%%" + self.director + "%%' AND LOWER(movies_actors) LIKE '%%" + self.actor + "%%' AND date_released >= (%s) AND amount_grossed >= (%s) AND LOWER(plot) LIKE '%%" + self.plot + "%%'"

        cursor.execute(commonQuery + searchParamters + groupingQuery, (self.released, self.grossed))
        all_rows = cursor.fetchall()
        for row in all_rows:
            #Not an easy way to do this in SQL so I wrote it in python
            all_rating_sources = row[12].split(",")
            all_rating_sources = [s.lower() for s in all_rating_sources]
            all_ratings = row[11].split(",")

            if self.rating_source in all_rating_sources and float(all_ratings[all_rating_sources.index(self.rating_source)]) >= float(self.rating_value):
                self.movie_list.append(Movie(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]))

        return self

    def getMovieList(self):
        """getter for movie_list"""
        return self.movie_list
    
    def sortByCustomRating(self):
        """sorting movies"""
        self.movie_list.sort(key=lambda x:x.custom_score, reverse=True)
