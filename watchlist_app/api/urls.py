from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from watchlist_app.api.views import (MovieList, 
                                     MovieDetail, 
                                     StreamPlatformList, 
                                     StreamPlatformDetail,
                                     ReviewList,
                                     ReviewDetail,
                                     MytokenObtainPairView,
                                     RegistrationView, PasswordResetEmailVerifyView, PasswordChangeView)

urlpatterns = [
    path('user/token/', MytokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', RegistrationView.as_view(), name='register-user'),
    path('user/password-reset/<email>/', PasswordResetEmailVerifyView.as_view(), name='password-reset'),
    path('user/password-change/', PasswordChangeView.as_view(), name='password-change'),

    path('movies/', MovieList.as_view(), name='movie-list'),
    path('movie/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('stream-platforms/', StreamPlatformList.as_view(), name='stream-platform-list'),
    path('stream-platforms/<int:pk>/', StreamPlatformDetail.as_view(), name='stream-platform-detail'),

    path('movies/<int:movie_id>/reviews/', ReviewList.as_view(), name='review-list'),
    path('movies/<int:movie_id>/reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]