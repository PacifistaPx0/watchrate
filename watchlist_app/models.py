from django.db import models

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