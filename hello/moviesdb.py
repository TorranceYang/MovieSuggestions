import os
import psycopg2
import urlparse
import datetime

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

def getAllMovies():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
     Movie.id, title, genre, plot, date_released, Director.id, Director.first_name, Director.last_name, amount_grossed, movies_actors, actor_ids, string_agg(rating_score::text, ',') AS ratings, string_agg(source_name, ',') as sources
    FROM
      Movie, Director, Rating, GrossingInfo, (SELECT movie_id, string_agg(first_name || ' ' || last_name, ',') as movies_actors, string_agg(actor_id::text, ',') as actor_ids FROM Actor, StarredIn WHERE actor.id = StarredIn.actor_id GROUP BY 1) AS ActorsInMovies
    WHERE
      Movie.director = Director.id AND Rating.movie_id = Movie.id AND GrossingInfo.movie_id = Movie.id AND Movie.id = ActorsInMovies.movie_id AND Rating.movie_id = ActorsInMovies.movie_id
    GROUP BY
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    """)

    all_rows = cursor.fetchall()

    movies = []
    for row in all_rows:
        movies.append(Movie(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]))
    return movies

#Have no idea how to do this any better
class Movie:
    def __init__(self, movie_id, title, genre, plot, date_released, director_id, director_fname, director_lname, grossed, actors, actor_ids, ratings, sources):
        self.poster_path = "../static/posters/" + str(movie_id).zfill(7) + ".jpg"
        self.title = title
        self.genre = genre
        self.plot = plot
        self.imdb_link = "https://www.imdb.com/title/tt" + str(movie_id).zfill(7)
        self.date_released = date_released
        self.director_id = str(director_id).zfill(7)
        self.director_name = director_fname + " " + director_lname
        self.director_link = "http://www.imdb.com/name/nm" + str(director_id).zfill(7)
        self.actors = actors.split(",")
        split_ids = actor_ids.split(",")
        self.actor_ids = ["http://www.imdb.com/name/nm" + str(actor_id).zfill(7) for actor_id in split_ids]
        self.zipped_actors = zip(self.actors, self.actor_ids)
        self.grossed = "%.2f" % grossed

        ratings_array = ratings.split(",")
        sources_array = sources.split(",")

        try:
            self.rotten_rating = ratings_array[sources_array.index("Rotten Tomatoes")]
            self.rotten_rating_text = "width:" + str(self.rotten_rating) + "%"
        except:
            self.rotten_rating = "N/A"
        try:
            self.metascore = ratings_array[sources_array.index("Metascore")]
            self.metascore_text = "width:" + str(self.metascore) + "%"
        except:
            self.metascore = "N/A"

        try:
            self.imdb_rating = ratings_array[sources_array.index("IMDb")]
            self.imdb_rating_text = "width:" + str(int(float(self.imdb_rating) * 10)) + "%"
        except:

            self.imdb_rating = "N/A"

        #Filler
        self.custom_score = 90

        self.rotten_max = 100
        self.metascore_max = 100
        self.imdb_max = 10
