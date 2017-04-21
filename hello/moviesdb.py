import os
import psycopg2
import urlparse

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
      title, genre, plot, date_released, director.first_name, director.last_name, string_agg(rating_score::text, ',') AS ratings, string_agg(max_rating::text, ',') as max_ratings, string_agg(source_name, ',') as sources, amount_grossed
    FROM
      Movie, Director, Rating, GrossingInfo
    WHERE
      Movie.director = Director.id AND Rating.movie_id = Movie.id AND GrossingInfo.movie_id = Movie.id
    GROUP BY
      1, 2, 3, 4, 5, 6, 10
    """)

    all_rows = cursor.fetchall()

    movies = []
    for row in all_rows:
        movies.append(Movie(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    return movies

class Movie:
    def __init__(self, title, genre, plot, date_released, director_fname, director_lname, ratings, max_ratings, sources, grossed):
        self.title = title
        self.genre = genre
        self.plot = plot
        self.date_released = date_released
        self.director_fname = director_fname
        self.director_lname = director_lname
        self.grossed = grossed

        ratings_array = ratings.split(",")
        ##This can just be a constant, but this is just a meaningless proof of concept so it doesn't really matter
        max_ratings_array = max_ratings.split(",")
        sources_array = sources.split(",")

        try:
            self.rotten_rating = ratings_array[sources_array.index("Rotten Tomatoes")]
        except:
            self.rotten_rating = "N/A"
        try:
            self.metascore = ratings_array[sources_array.index("Metascore")]
        except:
            self.metascore = "N/A"

        try:
            self.imdb_rating = ratings_array[sources_array.index("IMDb")]
        except:
            self.imdb_rating = "N/A"

        self.rotten_max = 100
        self.metascore_max = 100
        self.imdb_max = 10
