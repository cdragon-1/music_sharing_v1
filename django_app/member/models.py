# from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    pass


class BookmarkSong(models.Model):
    pass
