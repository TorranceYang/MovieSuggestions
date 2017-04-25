"""where all the view stuff goes i guess"""
from django.shortcuts import render
#from django.http import HttpResponse
import hello.moviesdb as moviesdb
from hello.search import Search
from hello.search_factory import SearchFactory


# Create your views here.
def index(request):
    """hello world test?"""
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def search_movies(request):
    """execute search request"""
    if request.method == "GET":
        title = request.GET.get('searchTitle', None)
        genre = request.GET.get('searchGenre', None)
        director  = request.GET.get('searchDirector', None)
        rating = request.GET.get('searchRating', None)

        search_type = Search(title)
        movies = search_type.getSearchResults()
        return render(request, 'index.html', {'movies': movies})


def db(request):
    """return all movies"""
    movies = moviesdb.getAllMovies()
    # greeting = Greeting()
    # greeting.save()

    # greetings = Greet ing.objects.all()

    return render(request, 'index.html', {'movies': movies, 'test': 'wat are those'})
