from django.contrib import admin

# Register your models here.
from .models import User, Movie, Collection, Genre, RequestServe
admin.site.register(Movie)
admin.site.register(Collection)
admin.site.register(RequestServe)
admin.site.register(Genre)
