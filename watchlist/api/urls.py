from django.urls import *
# from watchlist.api import views
from watchlist.api.views import MovieList, MovieDetails

urlpatterns = [
    path('list', MovieList.as_view(), name='movie-list'),
    # path('create', views.movies_create, name='movie-create'),
    path('details/<int:id>', MovieDetails.as_view(), name='movie-details'),
]
