"""where all the view stuff goes i guess"""
from django.shortcuts import render
#from django.http import HttpResponse
import moviesdb
from hello.search import Search


# Create your views here.
def index(request):
    """hello world test?"""
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def search_movies(request):
    """execute search request"""
    if request.method == "GET":
        search_results = Search(request.GET.get('searchBar', None), request.GET['categories'])
        movies = search_results.getSearchResults()
        return render(request, 'index.html', {'movies': movies})


def db(request):
    """return all movies"""
    movies = moviesdb.getAllMovies()
    # greeting = Greeting()
    # greeting.save()

    # greetings = Greet ing.objects.all()

    return render(request, 'index.html', {'movies': movies, 'test': 'wat are those'})
