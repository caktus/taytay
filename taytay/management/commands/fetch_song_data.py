from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import requests

from ... import models


class Command(BaseCommand):
    help = 'Fetch song data from baelor.io'

    def handle(self, *args, **options):
        api_key = getattr(settings, 'BAELOR_API_KEY', None)
        if not api_key:
            raise CommandError('BAELOR_API_KEY has not been configured.')
        auth = {'Authorization': 'bearer {}'.format(api_key)}
        response = requests.get('https://baelor.io/api/v0/songs', headers=auth).json()
        if response['error']:
            raise CommandError('Error fetching songs: {error}'.format(**response))
        else:
            albums = {}
            for song in response['result']:
                song_slug = song['slug']
                song_info = {
                    'title': song['title'],
                    'writers': song['writers'],
                    'producers': song['producers'],
                }
                album = song['album']
                album_slug = album['slug']
                album_info = {
                    'title': album['name'],
                    'label': album['label'],
                    'genres': album['genres'],
                    'producers': album['producers'],
                }
                if album_slug not in albums:
                    albums[album_slug], _ = models.Album.objects.update_or_create(
                        slug=album_slug, defaults=album_info)
                song_info['album'] = albums[album_slug]
                song_info['lyrics'] = '\n'.join(line['content'] for line in song['lyrics'])
                models.Song.objects.update_or_create(
                    slug=song_slug, defaults=song_info)
