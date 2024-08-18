from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

from watchlist_app.models import Watchlist, StreamPlatform, Review
from userauths.models import User, Profile


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'password2']

    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return attr

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )
        email_username, _ =  user.email.split('@')
        user.username = email_username
        user.set_password(validated_data['password'])
        user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username

        return token

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

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
