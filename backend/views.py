from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello world 123! ")

def index(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)