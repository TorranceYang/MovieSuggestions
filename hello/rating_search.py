import os
import urlparse
import psycopg2
from hello.moviesdb import Movie
from hello.search import Search

class RatingSearch(Search):

    def __init__(self, search_term):
        super(RatingSearch, self).__init__(search_term)

    def getSearchResults(self):
        """override super class search"""
        cursor = super(RatingSearch, self).getConnection().cursor()
        return super(RatingSearch, self).getMovieQuery(cursor, "Movie.genre")
