from django.shortcuts import render
from django.http import HttpResponse
import moviesdb

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    moviesdb.test()
    return render(request, 'index.html')


def db(request):

    movies = moviesdb.getAllMovies();
    # greeting = Greeting()
    # greeting.save()

    # greetings = Greet ing.objects.all()

    return render(request, 'index.html', {'movies': movies, 'test': 'wat are those'})
