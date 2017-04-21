import urllib2
import psycopg2
from urlparse import urlparse
import os
import os.path
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

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
        print(imdb_info["Plot"])
        cursor.execute('UPDATE Movie SET plot=(%s) WHERE id = (%s)', (imdb_info["Plot"], movie_id))
main()
