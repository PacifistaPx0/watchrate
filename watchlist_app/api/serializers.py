from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform



class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StreamPlatform
        fields = "__all__" 

class WatchlistSerializer(serializers.ModelSerializer):
    platforms = StreamPlatformSerializer(read_only=True)

    class Meta:
        model = Watchlist
        fields = "__all__"  # Or list specific fields like ['id', 'title', 'description', 'active']