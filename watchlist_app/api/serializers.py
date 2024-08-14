from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform, Review


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    movie = serializers.HyperlinkedRelatedField(
        view_name='movie-detail',
        queryset=Watchlist.objects.all(),
        lookup_field='pk'
    )
    class Meta:
        model = Review
        fields= ['id', 'movie', 'review_text', 'rating', 'created_at', 'updated_at', 'review_user']

class WatchlistSerializer(serializers.HyperlinkedModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    platforms = serializers.HyperlinkedRelatedField(
        view_name='stream-platform-detail',  
        read_only=True
    )

    class Meta:
        model = Watchlist
        fields = ['id', 'title', 'genre', 'description', 'active', 'created', 'platforms', 'reviews']


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movie-detail',  
    )

    class Meta:
        model = StreamPlatform
        fields = ['id', 'name', 'about', 'url', 'watchlist']
