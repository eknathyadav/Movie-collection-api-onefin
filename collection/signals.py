from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


@receiver(post_save, sender=User)
def generate_token(sender, user_instance, **kwargs):
    RefreshToken.for_user(user_instance)
