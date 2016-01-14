from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase

from .. import models


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
