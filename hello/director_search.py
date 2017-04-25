from hello.search import Search

class DirectorSearch(Search):
    def __init__(self, search_term):
        super(DirectorSearch, self).__init__(search_term)

    def getSearchResults(self):
        """override super class search"""
        cursor = super(DirectorSearch, self).getConnection().cursor()
        cursor.execute("""SELECT Movie.title from Movie NATURAL JOIN (SELECT director.id as director from director WHERE director.first_name = 'Peter') as Temp""")

        return super(DirectorSearch, self).getMovieQuery(cursor, "Movie.director")
