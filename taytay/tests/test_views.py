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
