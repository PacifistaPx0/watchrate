from django.urls import path
from watchlist_app.api.views import (MovieList, 
                                     MovieDetail, 
                                     StreamPlatformList, 
                                     StreamPlatformDetail,
                                     ReviewList,
                                     ReviewDetail,)

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('movie/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('stream-platforms/', StreamPlatformList.as_view(), name='stream-platform-list'),
    path('stream-platforms/<int:pk>/', StreamPlatformDetail.as_view(), name='stream-platform-detail'),

    path('movies/<int:movie_id>/reviews/', ReviewList.as_view(), name='review-list'),
    path('movies/<int:movie_id>/reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]