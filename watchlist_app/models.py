from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    created = models.DateTimeField(auto_now_add=True)
    platforms = models.ForeignKey("StreamPlatform", verbose_name=(""), on_delete=models.CASCADE, 
                                  null=True, related_name="watchlist")
    #platforms = models.ManyToManyField(StreamPlatform, related_name="watchlists", blank=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    movie = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name="reviews")
    review_text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.movie.title} - {self.rating}'