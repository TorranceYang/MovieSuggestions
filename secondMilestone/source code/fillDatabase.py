import psycopg2
from urlparse import urlparse
import os
import requests
import re
#Run sudo pip install IMDbPY
from imdb import IMDb
from datetime import datetime

top250_url = "http://akas.imdb.com/chart/top"


#Gets the IMDB Movie ID"s of the top 250 rate movies, snippet was taken from Stack Overflow
def scrape_top250():
    r = requests.get(top250_url)
    html = r.text.split("\n")
    result = []
    for line in html:
        line = line.rstrip("\n")
        m = re.search(r'data-titleid="tt(\d+?)">', line)
        if m:
            _id = m.group(1)
            result.append(_id)
    #
    return result

#Queries imdbpy package for more movie information
def insert_into_movies_and_directors(top250):
    ia = IMDb()
    for movie_id in top250:
        movie = ia.get_movie(movie_id)
        director = movie['director'][0]
        director_name = director["name"].split()
        first_name = director_name[0]
        last_name = ' '.join(director_name[1:]).strip()
        release_date = datetime(1980, 1, 1, tzinfo=None)
        try:
            release_date = datetime.strptime(requests.get('http://www.omdbapi.com/?i=tt' + movie_id).json()['Released'], '%d %b %Y')
        except Exception as e:
            print("Datetime not valid")
        print(movie)
        cursor.execute('INSERT INTO Director VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (director.getID(), first_name, last_name))
        cursor.execute('INSERT INTO Movie VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING', (movie_id, movie['title'], movie['genre'][0], director.getID(), release_date))

#Inserts ratings into database
def insert_ratings(top250):
    ia = IMDb()
    for movie_id in top250:
        movie = ia.get_movie(movie_id)['title']

        #Rotten Tomatoes does not have an api, so this is how we're scraping for these movie ratings
        search = requests.get('https://www.google.com/search?q=' + movie.replace(" ", "+") + '+rating')
        text = search.text
        for s in list(re.finditer('https://www.rottentomatoes.com', text)):
            temptext = text[:s.start()]
            index = temptext.rfind('<span') - 1
            rotten_rating = ''
            if search.text[index-3:index] == '100':
                rotten_rating = '100'
            else:
                rotten_rating = search.text[index-2:index]
            if rotten_rating.isdigit():
                break
            rotten_rating = 0
        #Get IMDb rating + Metascore from IMDb
        imdb_info = requests.get('http://www.omdbapi.com/?i=tt' + movie_id).json()
        imdb_rating = imdb_info['imdbRating']

        if imdb_info['Metascore'].isdigit():
            metascore_rating = imdb_info['Metascore']
            cursor.execute("INSERT INTO Rating VALUES (uuid_generate_v4(), %s, %s, %s, %s)", ("Metascore", movie_id, 100, metascore_rating))

        print movie, rotten_rating, imdb_rating, metascore_rating
        if rotten_rating > 0:
            cursor.execute("INSERT INTO Rating VALUES (uuid_generate_v4(), %s, %s, %s, %s) ON CONFLICT DO NOTHING", ("Rotten Tomatoes", movie_id, 100, float(rotten_rating)))
        cursor.execute("INSERT INTO Rating VALUES (uuid_generate_v4(), %s, %s, %s, %s) ON CONFLICT DO NOTHING", ("IMDb", movie_id, 10, imdb_rating))


def main():
    cursor.execute(open("createTables.sql", "r").read())
    top250 = scrape_top250()
    insert_into_movies_and_directors(top250)
    insert_ratings(top250)

url = urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()
main()
