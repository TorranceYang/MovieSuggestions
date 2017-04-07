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
    today = datetime(2017, 4, 7, tzinfo=None)

    for movie_id in movies:
        movie_id = str(movie_id[0]).zfill(7)
        imdb_page = urllib2.urlopen('http://www.imdb.com/title/tt' + movie_id).read()
        soup = BeautifulSoup(imdb_page, "lxml")
        for h4_tag in soup.find_all('h4'):
            if h4_tag.text == 'Gross:':
                cursor.execute('INSERT INTO GrossingInfo VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (movie_id, today, float(h4_tag.next_sibling.strip()[1:].replace(',',''))/1000000))

main()
