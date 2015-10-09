import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now


class Album(models.Model):
    """Collection of songs."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    label = models.CharField(max_length=255)
    genres = ArrayField(
        models.CharField(max_length=100), size=10)
    producers = ArrayField(
        models.CharField(max_length=100), size=10)

    def __str__(self):
        return self.title


class Song(models.Model):
    """Song lyrics and metadata."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    album = models.ForeignKey(Album)
    lyrics = models.TextField()
    writers = ArrayField(
        models.CharField(max_length=100), size=10)
    producers = ArrayField(
        models.CharField(max_length=100), size=10)

    def __str__(self):
        return self.title


def slug():
    """Generate a nice random string."""
    return '{0:x}'.format(uuid.uuid4().int)


class UserSong(models.Model):
    """Generated songs that the user liked enough to save."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=32, unique=True, default=slug)
    lyrics = models.TextField()
    created_date = models.DateTimeField(default=now)
