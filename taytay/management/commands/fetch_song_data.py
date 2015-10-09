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
        # Get albums
        response = requests.get('https://baelor.io/api/v0/albums', headers=auth).json()
        if response['error']:
            raise CommandError('Error fetching albums: {error}'.format(**response))
        else:
            for item in response['result']:
                slug = item['slug']
                additional = {
                    'title': item['name'],
                    'label': item['label'],
                    'genres': item['genres'],
                    'producers': item['producers'],
                }
                album, _ = models.Album.objects.update_or_create(
                    slug=slug, defaults=additional)
                for song in item['songs']:
                    if song['has_lyrics']:
                        lyrics = requests.get(
                            'https://baelor.io/api/v0/songs/{slug}/lyrics'.format(**song),
                            headers=auth).json()
                        if lyrics['error']:
                            self.stderr.write(
                                'Error fetching song "{title}": {error}\n'.format(**song))
                        else:
                            rest = {
                                'title': song['title'],
                                'album': album,
                                'lyrics': lyrics['result']['lyrics'],
                                'writers': song['writers'],
                                'producers': song['producers'],
                            }
                            models.Song.objects.update_or_create(
                                slug=song['slug'], defaults=rest)
