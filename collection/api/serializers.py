from rest_framework import serializers

from collection.models import User
from django.contrib.auth.hashers import make_password
from collection.models import User, Movie, Collection, Genre, RequestServe
from collections import Counter


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ["genre_name"]

    def create(self, validated):
        genre_obj, created = Genre.objects.get_or_create(**validated)
        return genre_obj


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = "__all__"

        extra_kwargs = {
            'uuid': {
                'read_only': False
            }
        }

    def create(self, validated):
        genres = validated.pop("genres")

        movie_obj, created = Movie.objects.get_or_create(
            uuid=validated["uuid"])

        if not created:
            return movie_obj

        movie_obj.title = validated["title"]
        movie_obj.description = validated["description"]
        movie_obj.save()
        for genre in genres:
            print(genre)
            genre_serializer = GenreSerializer(data=genre)
            if genre_serializer.is_valid():
                genre_instance = genre_serializer.save()
                movie_obj.genres.add(genre_instance)
        return movie_obj


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        flag = self.context.get("make_write_only", None)
        if flag:
            # if the request is Get for listing all the collections
            self.fields["movies"].write_only = True

    class Meta:
        model = Collection
        fields = "__all__"
        extra_kwargs = {
            'user': {
                'required': False,
                "write_only": True
            }
        }

    def create(self, validated):
        movies = validated.pop("movies")
        collection_obj = Collection.objects.create(**validated)
        for movie_dict in movies:
            movie_serializer = MovieSerializer(data=movie_dict)

            if movie_serializer.is_valid():
                movie_instance = movie_serializer.save()
                collection_obj.movies.add(movie_instance)
        return collection_obj

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        if "movies" in validated_data:
            movies = validated_data.pop("movies")
            for movie_dict in movies:
                movie_serializer = MovieSerializer(
                    data=movie_dict)
                if movie_serializer.is_valid():
                    movie_instance = movie_serializer.save()
                    instance.movies.add(movie_instance)
                else:
                    raise serializers.ValidationError(
                        {'movie': movie_serializer.errors})
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]

    # hashing the password

    def validate_password(self, value: str) -> str:
        return make_password(value)
