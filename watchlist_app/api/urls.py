from django.urls import path
from watchlist_app.api.views import MovieList, MovieDetail, StreamPlatformList, StreamPlatformDetail

urlpatterns = [
    path('list/', MovieList.as_view(), name='movie-list'),
    path('movie/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('stream-platforms/', StreamPlatformList.as_view(), name='stream-platform-list'),
    path('stream-platforms/<int:pk>/', StreamPlatformDetail.as_view(), name='stream-platform-detail'),
]