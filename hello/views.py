"""where all the view stuff goes i guess"""
from django.shortcuts import render
#from django.http import HttpResponse
import hello.moviesdb as moviesdb
from hello.search import Search
from hello.recommend import Recommend


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
        search.getMovieQuery().sortByCustomRating()
        return render(request, 'index.html', {'movies': search.getMovieList()})

def generate_recommendation(request):
    if request.method == "GET":
        movie_id = request.GET.get('movie', None)
        recommended = Recommend(movie_id)
        return render(request, 'recommended.html', {'recommended': recommended.getRecommended()})

def db(request):
    """return all movies"""
    movies = moviesdb.sortByCustomRating(moviesdb.getAllMovies())
    # greeting = Greeting()
    # greeting.save()

    # greetings = Greet ing.objects.all()

    return render(request, 'index.html', {'movies': movies, 'test': 'wat are those'})
