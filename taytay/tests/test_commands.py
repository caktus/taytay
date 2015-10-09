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

    def test_fetch_songs(self, mock_get):
        """Fetch all songs."""
        songs_response = Mock()
        songs_response.json.return_value = {
            'result': [
                {
                    "index": 1,
                    "slug": "welcome-to-new-york",
                    "title": "Welcome to New York",
                    "length": "00:03:32",
                    "writers": [
                        "Taylor Swift",
                        "Ryan Tedder"
                    ],
                    "producers": [
                        "Ryan Tedder",
                        "Noel Zancanella",
                        "Taylor Swift"
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
                    "lyrics": []
                }
            ],
            'error': None,
            'success': True,
        }
        mock_get.side_effect = [
            songs_response,
        ]
        self.call_command()
        mock_get.assert_called_with(
            'https://baelor.io/api/v0/songs', headers={'Authorization': 'bearer XXXXXX'})
        songs = models.Song.objects.all()
        self.assertEqual(songs.count(), 1)
        self.assertEqual(songs[0].title, 'Welcome to New York')
        albums = models.Album.objects.all()
        self.assertEqual(albums.count(), 1)
        self.assertEqual(albums[0].title, '1989')

    def test_song_error(self, mock_get):
        """Handle errors when fetching songs."""
        songs_response = Mock()
        songs_response.json.return_value = {
            'result': [],
            'error': '0x1073',
            'success': False
        }
        mock_get.side_effect = [
            songs_response,
        ]
        with self.assertRaises(CommandError):
            self.call_command()
        mock_get.assert_called_with(
            'https://baelor.io/api/v0/songs', headers={'Authorization': 'bearer XXXXXX'})
        albums = models.Album.objects.all()
        self.assertEqual(albums.count(), 0)

    def test_build_lyrics(self, mock_get):
        """Build song lyrics from the response data."""
        songs_response = Mock()
        songs_response.json.return_value = {
            'result': [
                {
                    "index": 2,
                    "slug": "blank-space",
                    "title": "Blank Space",
                    "length": "00:03:51",
                    "writers": [
                        "Taylor Swift",
                        "Max Martin",
                        "Shellback"
                    ],
                    "producers": [
                        "Max Martin",
                        "Shellback"
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
                    "lyrics": [
                        {
                            "content": "Nice to meet you",
                            "time_code": "00:00:04.8100000"
                        },
                        {
                            "content": "Where you been?",
                            "time_code": "00:00:07.1800000"
                        },
                        {
                            "content": "I could show you incredible things",
                            "time_code": "00:00:08.3500000"
                        },
                        {
                            "content": "Magic, madness, heaven, sin",
                            "time_code": "00:00:10.6100000"
                        },
                        {
                            "content": "Saw you there and I thought oh my god",
                            "time_code": "00:00:13.2500000"
                        },
                        {
                            "content": "Look at that face, you look like my next mistake",
                            "time_code": "00:00:16.2100000"
                        },
                        {
                            "content": "Love's a game, wanna play",
                            "time_code": "00:00:20.0200000"
                        },
                        {
                            "content": "New money, suit and tie",
                            "time_code": "00:00:25.2400000"
                        },
                        {
                            "content": "I can read you like a magazine",
                            "time_code": "00:00:28.1800000"
                        },
                        {
                            "content": "Ain't it funny rumors fly",
                            "time_code": "00:00:30.6900000"
                        },
                        {
                            "content": "And I know you heard about me",
                            "time_code": "00:00:33.2800000"
                        },
                        {
                            "content": "So hey, let's be friends",
                            "time_code": "00:00:35.1700000"
                        },
                        {
                            "content": "I'm dying to see how this one ends",
                            "time_code": "00:00:37.4600000"
                        },
                        {
                            "content": "Grab your passport and my hand",
                            "time_code": "00:00:39.9900000"
                        },
                        {
                            "content": "I could make the bad guys good for a weekend",
                            "time_code": "00:00:42.5600000"
                        },
                        {
                            "content": "So it's gonna be forever",
                            "time_code": "00:00:45.2400000"
                        },
                        {
                            "content": "Or it's gonna go down in flames",
                            "time_code": "00:00:47.7600000"
                        },
                        {
                            "content": "You can tell me when it's over",
                            "time_code": "00:00:50.5100000"
                        },
                        {
                            "content": "If the high was worth the pain",
                            "time_code": "00:00:52.3800000"
                        },
                        {
                            "content": "Got a long list of ex-lovers",
                            "time_code": "00:00:55.3600000"
                        },
                        {
                            "content": "They'll tell you I'm insane",
                            "time_code": "00:00:57.9700000"
                        },
                        {
                            "content": "Cause you know I love the players",
                            "time_code": "00:01:00.5000000"
                        },
                        {
                            "content": "And you love the game",
                            "time_code": "00:01:02.7400000"
                        },
                        {
                            "content": "Cause we're young and we're reckless",
                            "time_code": "00:01:05.3900000"
                        },
                        {
                            "content": "We'll take this way too far",
                            "time_code": "00:01:07.5800000"
                        },
                        {
                            "content": "It'll leave you breathless",
                            "time_code": "00:01:10.3700000"
                        },
                        {
                            "content": "Or with a nasty scar",
                            "time_code": "00:01:13.2200000"
                        },
                        {
                            "content": "Got a long list of ex-lovers",
                            "time_code": "00:01:15.1400000"
                        },
                        {
                            "content": "They'll tell you I'm insane",
                            "time_code": "00:01:17.7900000"
                        },
                        {
                            "content": "But I got a blank space baby",
                            "time_code": "00:01:20.2700000"
                        },
                        {
                            "content": "And I'll write your name",
                            "time_code": "00:01:23.7200000"
                        },
                        {
                            "content": "Cherry lips",
                            "time_code": "00:01:30.5500000"
                        },
                        {
                            "content": "Crystal skies",
                            "time_code": "00:01:31.9900000"
                        },
                        {
                            "content": "I could show you incredible things",
                            "time_code": "00:01:33.2900000"
                        },
                        {
                            "content": "Stolen kisses, pretty lies",
                            "time_code": "00:01:35.7100000"
                        },
                        {
                            "content": "You're the king baby I'm your queen",
                            "time_code": "00:01:38.2700000"
                        },
                        {
                            "content": "Find out what you want",
                            "time_code": "00:01:40.4500000"
                        },
                        {
                            "content": "Be that girl for a month",
                            "time_code": "00:01:42.6200000"
                        },
                        {
                            "content": "But the worst is yet to come",
                            "time_code": "00:01:45.1700000"
                        },
                        {
                            "content": "Oh no",
                            "time_code": "00:01:49"
                        },
                        {
                            "content": "Screaming, crying, perfect storms",
                            "time_code": "00:01:50.6900000"
                        },
                        {
                            "content": "I could make all the tables turn",
                            "time_code": "00:01:53.3000000"
                        },
                        {
                            "content": "Rose garden filled with thorns",
                            "time_code": "00:01:55.7000000"
                        },
                        {
                            "content": "Keep you second guessing like oh my god",
                            "time_code": "00:01:58.2900000"
                        },
                        {
                            "content": "Who is she? I get drunk on jealousy",
                            "time_code": "00:02:01.2200000"
                        },
                        {
                            "content": "But you'll come back each time you leave",
                            "time_code": "00:02:04.8700000"
                        },
                        {
                            "content": "Cause darling I'm a nightmare dressed like a daydream",
                            "time_code": "00:02:07.5600000"
                        },
                        {
                            "content": "So it's gonna be forever",
                            "time_code": "00:02:10.3100000"
                        },
                        {
                            "content": "Or it's gonna go down in flames",
                            "time_code": "00:02:12.8300000"
                        },
                        {
                            "content": "You can tell me when it's over",
                            "time_code": "00:02:15.3200000"
                        },
                        {
                            "content": "If the high was worth the pain",
                            "time_code": "00:02:17.7700000"
                        },
                        {
                            "content": "Got a long list of ex-lovers",
                            "time_code": "00:02:20.2300000"
                        },
                        {
                            "content": "They'll tell you I'm insane",
                            "time_code": "00:02:22.9500000"
                        },
                        {
                            "content": "Cause you know I love the players",
                            "time_code": "00:02:25.3200000"
                        },
                        {
                            "content": "And you love the game",
                            "time_code": "00:02:27.9100000"
                        },
                        {
                            "content": "Cause we're young and we're reckless",
                            "time_code": "00:02:30.2700000"
                        },
                        {
                            "content": "We'll take this way too far and leave you breathless",
                            "time_code": "00:02:32.8100000"
                        },
                        {
                            "content": "Or with a nasty scar",
                            "time_code": "00:02:37.9200000"
                        },
                        {
                            "content": "Got a long list of ex-lovers",
                            "time_code": "00:02:40.4600000"
                        },
                        {
                            "content": "They'll tell you I'm insane",
                            "time_code": "00:02:42.8500000"
                        },
                        {
                            "content": "But I got a blank space baby",
                            "time_code": "00:02:45.6600000"
                        },
                        {
                            "content": "And I'll write your name",
                            "time_code": "00:02:48.9000000"
                        },
                        {
                            "content": "Boys only want love if it's torture",
                            "time_code": "00:02:51.0700000"
                        },
                        {
                            "content": "Don't say I didn't say I didn't warn you",
                            "time_code": "00:02:55.0700000"
                        },
                        {
                            "content": "Boys only want love if it's torture",
                            "time_code": "00:03:00.1300000"
                        },
                        {
                            "content": "Don't say I didn't say I didn't warn you",
                            "time_code": "00:03:05.0300000"
                        },
                        {
                            "content": "So it's gonna be forever",
                            "time_code": "00:03:10.1500000"
                        },
                        {
                            "content": "Or it's gonna go down in flames",
                            "time_code": "00:03:12.6800000"
                        },
                        {
                            "content": "You can tell me when it's over",
                            "time_code": "00:03:15.3400000"
                        },
                        {
                            "content": "If the high was worth the pain",
                            "time_code": "00:03:17.9700000"
                        },
                        {
                            "content": "Got a long list of ex-lovers",
                            "time_code": "00:03:20.4500000"
                        },
                        {
                            "content": "They'll tell you I'm insane",
                            "time_code": "00:03:23.1000000"
                        },
                        {
                            "content": "Cause you know I love the players",
                            "time_code": "00:03:25.6200000"
                        },
                        {
                            "content": "And you love the game",
                            "time_code": "00:03:28.1500000"
                        },
                        {
                            "content": "Cause we're young and we're reckless",
                            "time_code": "00:03:30.8500000"
                        },
                        {
                            "content": "We'll take this way too far and leave you breathless",
                            "time_code": "00:03:33.0900000"
                        },
                        {
                            "content": "Or with a nasty scar",
                            "time_code": "00:03:38.2700000"
                        },
                        {
                            "content": "Got a long list of ex-lovers",
                            "time_code": "00:03:40.6700000"
                        },
                        {
                            "content": "They'll tell you I'm insane",
                            "time_code": "00:03:43.1500000"
                        },
                        {
                            "content": "But I got a blank space baby",
                            "time_code": "00:03:45.4200000"
                        },
                        {
                            "content": "And I'll write your name",
                            "time_code": "00:03:49.1900000"
                        },
                        {
                            "content": "",
                            "time_code": "00:03:51.5100000"
                        }
                    ]
                }
            ],
            'error': None,
            'success': True,
        }
        mock_get.side_effect = [
            songs_response,
        ]
        self.call_command()
        mock_get.assert_called_with(
            'https://baelor.io/api/v0/songs', headers={'Authorization': 'bearer XXXXXX'})
        songs = models.Song.objects.all()
        self.assertEqual(songs.count(), 1)
        self.assertTrue(songs[0].lyrics)
