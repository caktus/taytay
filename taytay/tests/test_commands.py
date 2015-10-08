import io

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


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


class FetchSongDataTestCase(CommandMixin, TestCase):
    """Populate song data from Baelor API."""

    command = 'fetch_song_data'

    def test_not_configured(self):
        """Raise error if the API key is not configured."""
        with self.settings(BAELOR_API_KEY=None):
            with self.assertRaises(CommandError):
                self.call_command()
