from requests.adapters import HTTPAdapter
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from requests.adapters import HTTPAdapter, Retry
from rest_framework import generics
from .serializers import UserSerializer, CollectionSerializer
from collection.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from collection.models import User, Movie, Collection, Genre, RequestServe
from rest_framework import status, viewsets
from collections import Counter
import time
import environ
import logging

# Create your views here.
env = environ.Env()
environ.Env.read_env()


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # def post -> create

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_instance = serializer.save()
        refresh = RefreshToken.for_user(
            user_instance)  # generating the JWT token
        access_token = str(refresh.access_token)
        headers = self.get_success_headers(serializer.data)
        res = {"access_token": access_token}
        return Response(res, status=status.HTTP_201_CREATED, headers=headers)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    # to get the favourite genres accross all the collections
    def get_favourite_genres(self, user_obj):
        genre_count = Counter()
        start = time.time()
        for collection in user_obj.collections.all():
            for movies in collection.movies.all():
                for genre in movies.genres.all().values_list("genre_name", flat=True):
                    genre_count[genre] += 1
        top_genres = genre_count.most_common(3)
        print("time taken ", time.time()-start)
        return [genre[0] for genre in top_genres]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response({"collection_uuid": serializer.data["uuid"]},
                        status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=self.request.user)
        serializer = self.get_serializer(queryset, many=True, context={
                                         "make_write_only": True})
        data = {"collections": serializer.data}
        data["favourite_genres"] = self.get_favourite_genres(
            self.request.user)
        custom_response = {"is_success": True,
                           "data": data}
        return Response(custom_response, status=status.HTTP_200_OK)


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs["timeout"]
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_movies(request):
    page = request.GET.get("page", None)
    logging.basicConfig(level=logging.DEBUG)
    session = requests.Session()
    user = env('username_tp')
    password = env('password_tp')
    session.auth = (user, password)

    retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[500, 502, 503, 504])
    adapter = TimeoutHTTPAdapter(timeout=2, max_retries=retries)
    session.mount('https://', adapter)
    if page is None:
        response = session.get(
            'https://demo.credy.in/api/v1/maya/movies/')
    else:
        response = session.get(
            f'https://demo.credy.in/api/v1/maya/movies/?page={page}')
    return Response(response.json(), status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def request_count(request):
    request_count = RequestServe.objects.all().count()
    return Response({"requests": request_count}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def request_reset(request):
    RequestServe.objects.all().delete()
    return Response({"message": "request count reset successfully"
                     })
