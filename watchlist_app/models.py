from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.conf import settings

class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=100)
    about = models.CharField(max_length=150)
    def __str__(self):
        return self.name


class Watchlist(models.Model):
    title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    description =  models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, 
                                validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
                                null=True, blank=True)
    review_count = models.PositiveIntegerField(default=0, null=True)
    created = models.DateTimeField(auto_now_add=True)
    platforms = models.ForeignKey("StreamPlatform", verbose_name=(""), on_delete=models.CASCADE, 
                                  null=True, related_name="watchlist")
    #platforms = models.ManyToManyField(StreamPlatform, related_name="watchlists", blank=True)

    def __str__(self):
        return self.title
    
    def calculate_average_rating(self):
        average = self.reviews.aggregate(average=Avg('rating'))['average']
        return average
    
    def calculate_review_count(self):
        return self.reviews.count()

    
class Review(models.Model):
    review_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review_user")
    movie = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name="reviews")
    review_text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.movie.title} - {self.rating}'