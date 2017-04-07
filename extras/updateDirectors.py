import urllib
import psycopg2
from urlparse import urlparse
import os
import os.path
import requests
import re
from imdb import IMDb

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

    cursor.execute('SELECT id FROM Director');
    directors = cursor.fetchall();
    ia = IMDb()
    for director_id in directors:
        director_id = str(director_id[0]).zfill(7)
        director = ia.get_person(director_id)
        if not os.path.exists('../hello/static/directors/' + director_id + '.jpg'):
            urllib.urlretrieve(director['headshot'], '../hello/static/directors/' + director_id + '.jpg')

        cursor.execute('UPDATE Director SET mini_bio = (%s) WHERE id = (%s)', (director['mini biography'], director_id))
main()
