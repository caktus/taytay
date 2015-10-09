from django.core.urlresolvers import reverse
from django.test import override_settings, TestCase
from unittest.mock import patch

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SongGeneratorTestCase(TestCase):
    """Page to generate lyrics."""

    @patch("taytay.views.make_song")
    @patch("taytay.views.make_title")
    def test_render_page(self, mock_title, mock_song):
        """Grab the page."""
        with self.assertTemplateUsed('taytay/song-generator.html'):
            response = self.client.get(reverse('new-song'))
            self.assertEqual(response.status_code, 200)
