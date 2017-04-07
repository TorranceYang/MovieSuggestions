import os
import praw
import psycopg2
import re
import sys
from urlparse import urlparse


def get_movie_alias(movie_name):
    return movie_name


def insert_into_table(movie_name, post_type, score, timestamp, post_content):
    cursor.execute("INSERT INTO Reddit VALUES (%S, %S, %S, %S) ON CONFLICT DO NOTHING", movie_name, post_type, score, timestamp, post_content)


def get_r_movies_posts(time, limit=None):
    reddit = praw.Reddit(user_agent='Comment Extraction', client_id='xLVOBTSVWhVo0A', client_secret='jGLMgJ25D8r2EgALZV6Gitw_UG4')
    r_movies = reddit.subreddit('movies')
    return r_movies.top(time_filter=time, limit=limit)


def get_cursor(db_url):
    url = urlparse(db_url)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return conn.cursor()

cursor = get_cursor(os.environ["DATABASE_URL"])

for post in get_r_movies_posts("month", None):
    searchTitle = re.search(get_movie_alias(sys.argv[1]), post.title, re.I)
    if searchTitle:
        insert_into_table(sys.argv[1], "Post", post.score, post.created, post)
        post.comments.replace_more(limit=0)
        comment_queue = post.comments[:]
        while comment_queue:
            comment = comment_queue.pop(0)
            searchComments = re.search(get_movie_alias(sys.argv[1]), comment.body, re.I)
            if searchComments:
                insert_into_table(sys.argv[1], "Comment", post.score, post.created, comment)
            comment_queue.extend(comment.replies)
