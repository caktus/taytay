from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Fetch song data from baelor.io'

    def handle(self, *args, **options):
        api_key = getattr(settings, 'BAELOR_API_KEY', None)
        if not api_key:
            raise CommandError('BAELOR_API_KEY has not been configured.')
