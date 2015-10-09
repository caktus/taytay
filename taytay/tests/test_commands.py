import io
from unittest.mock import patch, Mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import override_settings, TestCase

from .. import models


class CommandMixin(object):
    """Helper for testing management commands."""

    command = ''

    def call_command(self, *args, **kwargs):
        """Call command and return stdout/stderr."""
        stdout, stderr = io.StringIO(), io.StringIO()
        kwargs['stdout'] = stdout
        kwargs['stderr'] = stderr
        call_command(self.command, *args, **kwargs)
        return stdout, stderr


@patch('requests.get')
@override_settings(BAELOR_API_KEY='XXXXXX')
class FetchSongDataTestCase(CommandMixin, TestCase):
    """Populate song data from Baelor API."""

    command = 'fetch_song_data'

    def test_not_configured(self, mock_get):
        """Raise error if the API key is not configured."""
        with self.settings(BAELOR_API_KEY=None):
            with self.assertRaises(CommandError):
                self.call_command()
        self.assertFalse(mock_get.called)

    def test_fetch_albums(self, mock_get):
        """Fetch all albums."""
        album_response = Mock()
        album_response.json.return_value = {
            "result": [
                {
                    "slug": "taylor-swift",
                    "name": "Taylor Swift",
                    "released_at": "2006-10-24T00:00:00",
                    "length": "00:38:26",
                    "label": "Big Machine",
                    "genres": [
                        "Country"
                    ],
                    "producers": [
                        "Scott Borchetta",
                        "Nathan Chapman",
                        "Robert Ellis Orrall"
                    ],
                    "songs": [
                    ],
                    "album_cover": {
                        "image_id": "c780c63f-8f19-4961-2873-08d21467e516"
                    }
                },
            ],
            "error": None,
            "success": True
        }
        mock_get.side_effect = [
            album_response,
        ]
        self.call_command()
        mock_get.assert_called_with(
            'https://baelor.io/api/v0/albums', headers={'Authorization': 'XXXXXX'})
        albums = models.Album.objects.all()
        self.assertEqual(albums.count(), 1)
        self.assertEqual(albums[0].title, 'Taylor Swift')
