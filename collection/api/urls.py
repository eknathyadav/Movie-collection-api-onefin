from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'collection', views.CollectionViewSet,
                basename='collection')

urlpatterns = [

    path('register/', views.UserRegisterView.as_view(), name="register_user"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('movies/', views.get_movies, name="get_movies"),
    path('', include(router.urls)),
    path('request-count/', views.request_count, name="request_count"),
    path('request-count/reset/', views.request_reset, name="request_reset")

]
