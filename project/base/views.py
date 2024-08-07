from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def some_endpoint(request):
    return HttpResponse('<p>This content was loaded via HTMX!</p>')