from django.core.urlresolvers import reverse
from django.test import override_settings, TestCase


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SongGeneratorTestCase(TestCase):
    """Page to generate lyrics."""

    def test_render_page(self):
        """Grab the page."""
        with self.assertTemplateUsed('taytay/song-generator.html'):
            response = self.client.get(reverse('new-song'))
            self.assertEqual(response.status_code, 200)
