"""where all the view stuff goes i guess"""
from django.shortcuts import render
#from django.http import HttpResponse
import hello.moviesdb as moviesdb
from hello.search import Search


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
        director = request.GET.get('searchDirector', None)
        actor = request.GET.get('searchActor', None)
        rating_source = request.GET.get('searchRatingSource', None)
        rating_value = request.GET.get('searchRatingValue', None)
        released = request.GET.get('searchReleased', None)
        grossed = request.GET.get('searchGrossed', None)
        plot = request.GET.get('searchPlot', None)

        search = Search(title, genre, director, actor, rating_source, rating_value, released, grossed, plot)
        return render(request, 'index.html', {'movies': search.getMovieQuery()})


def db(request):
    """return all movies"""
    movies = moviesdb.getAllMovies()
    # greeting = Greeting()
    # greeting.save()

    # greetings = Greet ing.objects.all()

    return render(request, 'index.html', {'movies': movies, 'test': 'wat are those'})
