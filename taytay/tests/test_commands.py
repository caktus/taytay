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

    def test_album_error(self, mock_get):
        """Handle errors when fetching albums."""
        album_response = Mock()
        album_response.json.return_value = {
            "result": [
            ],
            "error": '0x1073',
            "success": False
        }
        mock_get.side_effect = [
            album_response,
        ]
        with self.assertRaises(CommandError):
            self.call_command()
        mock_get.assert_called_with(
            'https://baelor.io/api/v0/albums', headers={'Authorization': 'XXXXXX'})
        albums = models.Album.objects.all()
        self.assertEqual(albums.count(), 0)

    def test_fetch_lyrics(self, mock_get):
        """Fetch lyrics for each of the songs."""
        album_response = Mock()
        album_response.json.return_value = {
            "result": [
                {
                    "slug": "1989",
                    "name": "1989",
                    "released_at": "2014-10-27T00:00:00",
                    "length": "01:08:36",
                    "label": "Big Machine",
                    "genres": [
                        "Pop",
                        "Synthpop"
                    ],
                    "producers": [
                        "Max Martin",
                        "Taylor Swift",
                        "Jack Antonoff",
                        "Nathan Chapman",
                        "Imogen Heap",
                        "Greg Kurstin",
                        "Mattman & Robin",
                        "Ali Payami",
                        "Shellback",
                        "Ryan Tedder",
                        "Noel Zancanella"
                    ],
                    "songs": [
                        {
                            "index": 3,
                            "slug": "style",
                            "title": "Style",
                            "length": "00:03:51",
                            "writers": [
                                "Taylor Swift",
                                "Max Martin",
                                "Shellback",
                                "Ali Payami"
                            ],
                            "producers": [
                                "Max Martin",
                                "Shellback",
                                "Ali Payami"
                            ],
                            "has_lyrics": True
                        },
                    ],
                    "album_cover": {
                        "image_id": "ca9232a3-363a-4be6-2870-08d21467e516"
                    }
                },
            ],
            "error": None,
            "success": True
        }
        lyric_response = Mock()
        lyric_response.json.return_value = {
            "result": {
                "lyrics": "Midnight\nYou come and pick me up, no headlights\nLong drive\nCould end in burning flames or paradise\nFade into view, oh\nIt's been a while since I have even heard from you (heard from you)\n\nI should just tell you to leave 'cause I\nKnow exactly where it leads but I\nWatch us go 'round and 'round each time\n\nYou got that James Dean daydream look in your eye\nAnd I got that red lip classic thing that you like\nAnd then we go crashing down, we come back every time\n'Cause we never go out of style\nWe never go out of style\n\nYou got that long hair, slick back, white t-shirt\nAnd I got that good girl faith and a tight little skirt\nAnd when we go crashing down, we come back every time\n we never go out of style\nWe never go out of style\n\nSo it goes\nHe can't keep his wild eyes on the road, \nTakes me home\nLights are off, he's taking off his coat, \nI say I heard, oh\nThat you've been out and about with some other girl\nSome other girl\n\nHe says what you heard is true but I\nCan't stop thinking about you and I\nI said I've been there too a few times\n\n'Cause you got that James Dean daydream look in your eye\nAnd I got that red lip classic thing that you like\nAnd then we go crashing down, we come back every time\n'Cause we never go out of style\nWe never go out of style\n\nYou got that long hair, slick back, white t-shirt\nAnd I got that good girl faith and a tight little skirt\nAnd when we go crashing down, we come back every time\n we never go out of style\nWe never go out of style\n\nTake me home\nJust take me home\nYeah, just take me home\n\n(Out of style)\n\nOh, you got that James Dean daydream look in your eye\nAnd I got that red lip classic thing that you like\nAnd then we go crashing down, we come back every time\n we never go out of style\nWe never go out of style",
                "song": {
                    "index": 3,
                    "slug": "style",
                    "title": "Style",
                    "length": "00:03:51",
                    "writers": [
                        "Taylor Swift",
                        "Max Martin",
                        "Shellback",
                        "Ali Payami"
                    ],
                    "producers": [
                        "Max Martin",
                        "Shellback",
                        "Ali Payami"
                    ],
                    "album": {
                        "slug": "1989",
                        "name": "1989",
                        "released_at": "2014-10-27T00:00:00",
                        "length": "01:08:36",
                        "label": "Big Machine",
                        "genres": [
                            "Pop",
                            "Synthpop"
                        ],
                        "producers": [
                            "Max Martin",
                            "Taylor Swift",
                            "Jack Antonoff",
                            "Nathan Chapman",
                            "Imogen Heap",
                            "Greg Kurstin",
                            "Mattman & Robin",
                            "Ali Payami",
                            "Shellback",
                            "Ryan Tedder",
                            "Noel Zancanella"
                        ],
                        "album_cover": {
                            "image_id": "ca9232a3-363a-4be6-2870-08d21467e516"
                        }
                    },
                    "has_lyrics": True
                }
            },
            "error": None,
            "success": True
        }
        mock_get.side_effect = [
            album_response,
            lyric_response,
        ]
        self.call_command()
        mock_get.assert_called_with(
            'https://baelor.io/api/v0/songs/style/lyrics', headers={'Authorization': 'XXXXXX'})
        songs = models.Song.objects.all()
        self.assertEqual(songs.count(), 1)
        self.assertEqual(songs[0].title, 'Style')

    def test_no_lyrics(self, mock_get):
        """Skip if lyrics aren't avaliable."""
        album_response = Mock()
        album_response.json.return_value = {
            "result": [
                {
                    "slug": "1989",
                    "name": "1989",
                    "released_at": "2014-10-27T00:00:00",
                    "length": "01:08:36",
                    "label": "Big Machine",
                    "genres": [
                        "Pop",
                        "Synthpop"
                    ],
                    "producers": [
                        "Max Martin",
                        "Taylor Swift",
                        "Jack Antonoff",
                        "Nathan Chapman",
                        "Imogen Heap",
                        "Greg Kurstin",
                        "Mattman & Robin",
                        "Ali Payami",
                        "Shellback",
                        "Ryan Tedder",
                        "Noel Zancanella"
                    ],
                    "songs": [
                        {
                            "index": 3,
                            "slug": "style",
                            "title": "Style",
                            "length": "00:03:51",
                            "writers": [
                                "Taylor Swift",
                                "Max Martin",
                                "Shellback",
                                "Ali Payami"
                            ],
                            "producers": [
                                "Max Martin",
                                "Shellback",
                                "Ali Payami"
                            ],
                            "has_lyrics": False
                        },
                    ],
                    "album_cover": {
                        "image_id": "ca9232a3-363a-4be6-2870-08d21467e516"
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
        self.assertEqual(mock_get.call_count, 1)
        songs = models.Song.objects.all()
        self.assertEqual(songs.count(), 0)
