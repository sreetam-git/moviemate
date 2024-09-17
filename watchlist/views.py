from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Movie

# Create your views here.

def movies_list(request):
    movies = Movie.objects.all()
    response = {
        'status': 'valid',
        'data': list(movies.values())
        }
    return JsonResponse(response)

def movies_details(request, id):
    movie_detail = Movie.objects.get(pk=id) 
    
    response = {
        'status': 'valid',
        'data': {
            'title': movie_detail.name,
            'description': movie_detail.description,
        }
    }
    return JsonResponse(response)
