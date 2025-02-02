from django.urls import *
# from watchlist.api import views
from watchlist.api.views import (WatchListAV, WatchDetails, 
                                 StreamPlatformAV, StreamPlatformDetail, 
                                 ReviewList, ReviewDetail, ReviewCreate)

urlpatterns = [
    path('list', WatchListAV.as_view(), name='movie-list'),
    # path('create', views.movies_create, name='movie-create'),
    path('details/<int:id>/', WatchDetails.as_view(), name='movie-details'),
    path('stream', StreamPlatformAV.as_view(), name='stream-platform'),
    path('stream/<int:id>/', StreamPlatformDetail.as_view(), name='stream-detail'),
    
    path('stream/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('stream/reviews/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),
]
