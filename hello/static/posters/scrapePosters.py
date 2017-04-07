import urllib
import psycopg2
from urlparse import urlparse
import os
import os.path
import requests
import re

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
        if not os.path.exists(movie_id + 'jpg'):
            urllib.urlretrieve(requests.get('http://www.omdbapi.com/?i=tt' + movie_id).json()['Poster'], movie_id + ".jpg")

main()
