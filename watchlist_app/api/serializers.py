from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'review_user', 'rating', 'review_text', 'created_at', 'updated_at']

class WatchlistSerializer(serializers.HyperlinkedModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    platforms = serializers.HyperlinkedRelatedField(
        view_name='stream-platform-detail',  
        read_only=True
    )

    class Meta:
        model = Watchlist
        fields = ['id', 'title', 'genre', 'description', 
                  'active', 'created', 'platforms', 'review_count', 'reviews', 'average_rating']
        
    def get_average_rating(self, obj):
        return obj.calculate_average_rating()
    def get_review_count(self, obj):
        return obj.calculate_review_count()


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movie-detail',  
    )

    class Meta:
        model = StreamPlatform
        fields = ['id', 'name', 'about', 'url', 'watchlist']
