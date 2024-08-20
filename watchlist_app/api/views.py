import random

from django.http import Http404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from watchlist_app.models import Watchlist, StreamPlatform, Review
from userauths.models import User, Profile
from watchlist_app.api.serializers import (WatchlistSerializer, 
                                           StreamPlatformSerializer, 
                                           ReviewSerializer, 
                                           MyTokenObtainPairSerializer,
                                           RegistrationSerializer,
                                           UserSerializer)
from watchlist_app.api.permissions import ReviewUserOrReadOnly

def generate_random_otp(length=6):
    otp = "".join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

class PasswordResetEmailVerifyView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs['email'] #api/v1/password-email-verify/example@gmail.com/

        user = User.objects.filter(email=email).first()
        if user:

            uuid64 = user.pk
            refresh = RefreshToken.for_user(user) #refresh token for user
            refresh_token = str(refresh.access_token) #get the access token

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()

            link = f"http://localhost:8000/create-new-password/?otp={user.otp}&uuid64={uuid64}&=refresh_token{refresh_token}"
            
            #after getting the link, send it to user via email
            context = {
                "link": link,
                "username": user.username
            }

            subject = "Password Reset Email"
            text_body = render_to_string('email/password_reset.txt', context)
            html_body = render_to_string('email/password_reset.html', context)

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[user.email],
                body=text_body
            )

            msg.attach_alternative(html_body, "text/html")
            msg.send()

            print("link======",link)

        return user
    
class PasswordChangeView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        payload = request.data

        otp = payload['otp']
        uuid64 = payload['uuid64']
        password = payload['password']

        user = User.objects.get(id=uuid64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.save()

            return Response({"message": "Password changed successfully."}, status=status.HTTP_201_CREATED)
        
        else:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class MytokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Review.objects.filter(movie_id=movie_id)

    def perform_create(self, serializer):
        movie_id = self.kwargs['movie_id'] #fetch the movie id from the URL
        movie = Watchlist.objects.get(id=movie_id) #get the movie instance

        # raise error if user tries to create more than one review for the same movie
        user = self.request.user
        if Review.objects.filter(movie=movie, review_user=user).exists():
            raise serializers.ValidationError(
                "User has already reviewed this movie.")

        serializer.save(movie=movie, review_user=user)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    #queryset = Review.objects.all()  # this filters by pk
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Review.objects.filter(movie_id=movie_id)

    def get_object(self):
        # Fetch the review object
        obj = super().get_object()
        # Additional checks can be added here if needed
        return obj


class MovieList(generics.ListCreateAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class StreamPlatformList(generics.ListCreateAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class StreamPlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    def get_serializer_context(self):
        return {'request': self.request}


""" class StreamPlatformList(APIView):
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetail(APIView):
    def get_object(self, pk):
        try:
            return StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        platform = self.get_object(pk)
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = self.get_object(pk)
        serializer = StreamPlatformSerializer(platform, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = self.get_object(pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 """
