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

    row = moviesdb.query();
    # greeting = Greeting()
    # greeting.save()

    # greetings = Greeting.objects.all()

    return render(request, 'index.html', {'directors': row, 'test': 'wat are those'})
