from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from watchlist_app.models import Watchlist, StreamPlatform, Review
from watchlist_app.api.serializers import WatchlistSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Review.objects.filter(movie_id=movie_id)

    def perform_create(self, serializer):
        movie_id = self.kwargs['movie_id']
        movie = Watchlist.objects.get(id=movie_id)
        serializer.save(movie=movie)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MovieList(APIView):
    def get(self, request):
        movies = Watchlist.objects.all()
        serializer = WatchlistSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchlistSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(APIView):
    def get_object(self, pk):
        try:
            return Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = WatchlistSerializer(movie, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = WatchlistSerializer(movie, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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