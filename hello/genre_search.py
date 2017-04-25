from hello.search import Search

class GenreSearch(Search):
    def __init__(self, search_term):
        super(GenreSearch, self).__init__(search_term)

    def getSearchResults(self):
        """override super class search"""
        cursor = super(GenreSearch, self).getConnection().cursor()
        return super(GenreSearch, self).getMovieQuery(cursor, "Movie.genre")
