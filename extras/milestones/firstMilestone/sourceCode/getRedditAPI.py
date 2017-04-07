import praw
import re
import MySQLdb

db = MySQLdb.connect(host="db.host.url", user="me", passwd="123", db="cs316_project")
reddit = praw.Reddit(user_agent='Comment Extraction', client_id='xLVOBTSVWhVo0A', client_secret='jGLMgJ25D8r2EgALZV6Gitw_UG4');

r_movies = reddit.subreddit('movies')
posts = r_movies.top(time_filter='month', limit=None)

cursor = db.cursor()

for post in posts:
    searchTitle = re.search("Ghost in the Shell|GITS",post.title,re.I)
    if searchTitle:
        cur.execute("INSERT INTO Votes VALUES (Ghost_In_The_Shell,"+post.score+","+"Submission,"+post.created+","+post);
        print (post.title)
        print (post.score)
        post.comments.replace_more(limit=0)
        comment_queue = post.comments[:]
        while comment_queue:
            comment = comment_queue.pop(0)
            searchComments = re.search("Ghost in the Shell|GITS",comment.body,re.I)
            if searchComments:
                cur.execute("INSERT INTO Votes VALUES (Ghost_In_The_Shell,"+comment.score+","+"Comment,"+comment.created+","+comment);
            comment_queue.extend(comment.replies)