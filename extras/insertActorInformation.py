import urllib
import psycopg2
from urlparse import urlparse
import os
import os.path
import requests
import re
from imdb import IMDb

unofficial_api = "http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q="

def main():
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

    cursor.execute('SELECT id FROM Movie');
    movies = cursor.fetchall();

    for movie_id in movies:
        movie_id = str(movie_id[0]).zfill(7)
        imdb_info = requests.get('http://www.omdbapi.com/?i=tt' + movie_id).json()
        actors = imdb_info["Actors"].split(", ")
        for actor in actors:
            actor_search = requests.get(unofficial_api + actor.replace(" ", "+")).json()
            try:
                actor_info = actor_search["name_popular"][0]
                if actor_info["name"] == actor:
                    actor_name = actor.split()
                    first_name = actor_name[0]
                    last_name = ' '.join(actor_name[1:]).strip()
                    cursor.execute('INSERT INTO Actor VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (int(actor_info["id"][2:]), first_name, last_name))
                    cursor.execute('INSERT INTO StarredIn Values (%s, %s) ON CONFLICT DO NOTHING', (int(actor_info["id"][2:]), movie_id))
                    print "Inserted " + first_name + " " + last_name
                else:
                    print "Couldn't find " + actor
            except Exception as e:
                print "Error for " + actor + str(e)

main()
