from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.

class Genre(models.Model):

    genre_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.genre_name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    description = models.CharField(max_length=1000)
    genres = models.ManyToManyField(Genre, related_name="movies")

    def __str__(self) -> str:
        return self.title


class Collection(models.Model):
    title = models.CharField(max_length=100)
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collections')
    movies = models.ManyToManyField(Movie, related_name="collections")

    def __str__(self) -> str:
        return self.title + " collection"


# model for logging request
class RequestServe(models.Model):
    endpoint = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
