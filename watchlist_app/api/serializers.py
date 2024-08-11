from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform, Review


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields= "__all__"

class WatchlistSerializer(serializers.HyperlinkedModelSerializer):
    review = ReviewSerializer(many=True, read_only=True)

    platforms = serializers.HyperlinkedRelatedField(
        view_name='stream-platform-detail',  
        read_only=True
    )

    class Meta:
        model = Watchlist
        fields = ['id', 'title', 'genre', 'description', 'active', 'created', 'platforms']


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movie-detail',  
    )

    class Meta:
        model = StreamPlatform
        fields = ['id', 'name', 'about', 'url', 'watchlist']
