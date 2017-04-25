from hello.search import Search
from hello.genre_search import GenreSearch
from hello.director_search import DirectorSearch

class SearchFactory(object):
    def __init__(self, category):
        self.category = category

    def getSearchType(self, search_term):
        """factory method for search type"""
        category = self.category
        if category == "title":
            return Search(search_term)
        elif category == "genre":
            return GenreSearch(search_term)
        elif category == "director":
            return DirectorSearch(search_term)
        else: 
            return None
