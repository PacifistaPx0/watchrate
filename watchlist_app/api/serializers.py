from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = "__all__"  # Or list specific fields like ['id', 'name', 'description', 'active']

class StreamPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatform
        fields = "__all__" 