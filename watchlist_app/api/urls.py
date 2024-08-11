from django.urls import path
from watchlist_app.api.views import MovieList, MovieDetail, StreamPlatformAV

urlpatterns = [
    path('list/', MovieList.as_view(), name='movie-list'),
    path('movie/<int:pk>', MovieDetail.as_view(), name='movie-detail'),
    path('stream_platforms/', StreamPlatformAV.as_view(), name='stream-platform')
]
