from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase

from .. import models
from ..views import make_song, make_title


class SongGeneratorTestCase(TestCase):
    """Page to generate lyrics."""

    @patch("taytay.views.make_song")
    @patch("taytay.views.make_title")
    def test_render_page(self, mock_title, mock_song):
        """Grab the page."""
        mock_song.return_value = 'Shake it off...'
        mock_title.return_value = 'Shake It Off'
        with self.assertTemplateUsed('taytay/song-generator.html'):
            response = self.client.get(reverse('new-song'))
            self.assertEqual(response.status_code, 200)
            mock_song.assert_called_with(album=None)
            mock_title.assert_called_with(mock_song.return_value)

    @patch("taytay.views.make_song")
    @patch("taytay.views.make_title")
    def test_save_song(self, mock_title, mock_song):
        """Save a generated song."""
        # Generate song and it should be saved in the session
        mock_song.return_value = 'Shake it off...'
        mock_title.return_value = 'Shake It Off'
        self.client.get(reverse('new-song'))
        response = self.client.post(reverse('new-song'))
        song = models.UserSong.objects.latest('created_date')
        self.assertEqual(song.title, 'Shake It Off')
        self.assertRedirects(response, song.get_absolute_url())

    @patch("taytay.views.make_song")
    @patch("taytay.views.make_title")
    def test_failed_save(self, mock_title, mock_song):
        """Can't save if there is no song in the session."""
        mock_song.return_value = 'Shake it off...'
        mock_title.return_value = 'Shake It Off'
        response = self.client.post(reverse('new-song'))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(models.UserSong.DoesNotExist):
            models.UserSong.objects.latest('created_date')

    @patch("markovify.text.NewlineText")
    def test_make_song_all_albums(self, mock_markov):
        """Feeding all lyrics into the markov model."""
        mock_markov.return_value.make_sentence.return_value = 'Shake it off.'
        red = models.Album.objects.create(
            title='Red', slug='red', producers=[], genres=[])
        models.Song.objects.create(
            title='Red', slug='red', album=red, producers=[], writers=[],
            lyrics='Loving him was red.')
        swift = models.Album.objects.create(
            title='1989', slug='1989', producers=[], genres=[])
        models.Song.objects.create(
            title='Shake It Off', slug='shake-it-off', album=swift, producers=[], writers=[],
            lyrics='Shake it off.')
        result = make_song()
        self.assertEqual(len(result.splitlines()), 28)
        mock_markov.assert_called_with('Loving him was red.Shake it off.', state_size=2)

    @patch("markovify.text.NewlineText")
    def test_make_song_single_album(self, mock_markov):
        """Feeding only a single album into the markov model."""
        mock_markov.return_value.make_sentence.return_value = 'Shake it off.'
        red = models.Album.objects.create(
            title='Red', slug='red', producers=[], genres=[])
        models.Song.objects.create(
            title='Red', slug='red', album=red, producers=[], writers=[],
            lyrics='Loving him was red.')
        swift = models.Album.objects.create(
            title='1989', slug='1989', producers=[], genres=[])
        models.Song.objects.create(
            title='Shake It Off', slug='shake-it-off', album=swift, producers=[], writers=[],
            lyrics='Shake it off.')
        result = make_song(album='Red')
        self.assertEqual(len(result.splitlines()), 28)
        mock_markov.assert_called_with('Loving him was red.', state_size=2)

    @patch("markovify.text.NewlineText")
    def test_make_title(self, mock_markov):
        """Generate a title for a song."""
        mock_markov.return_value.make_sentence.side_effect = [None, 'I go on too many dates']
        song = '''I stay up too late, got nothing in my brain
            That's what people say mmm, that's what people say mm
            I go on too many dates, but I can't make 'em stay
            At least that's what people say mmm, that's what people say mmm'''
        result = make_title(song=song)
        mock_markov.assert_called_with(song)
        self.assertEqual(result, 'I Go On')


class SongDetailTestCase(TestCase):
    """Details of a newly generated song."""

    def setUp(self):
        self.song = models.UserSong.objects.create(
            title='Shake It Off', lyrics='I stay out too late...')

    def test_render_page(self):
        """View the song details."""
        with self.assertTemplateUsed('taytay/song-detail.html'):
            response = self.client.get(self.song.get_absolute_url())
            self.assertEqual(response.status_code, 200)


class SongListTestCase(TestCase):
    """Listing previously generated songs."""

    def setUp(self):
        self.song = models.UserSong.objects.create(
            title='Shake It Off', lyrics='I stay out too late...')

    def test_render_page(self):
        """View the song details."""
        with self.assertTemplateUsed('taytay/song-list.html'):
            response = self.client.get(reverse('song-list'))
            self.assertEqual(response.status_code, 200)
