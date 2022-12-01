from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populate database with data from fixtures'

    def handle(self, *args, **options):
        # list contains application_name, file_name of fixtures
        fixtures_to_db = [
            ('users', 'User.json'),
            ('reviews', 'Category.json'),
            ('reviews', 'Title.json'),
            ('reviews', 'Genre.json'),
            ('reviews', 'Review.json'),
            ('reviews', 'Comment.json'),
        ]
        path_base = settings.BASE_DIR

        for app, file in fixtures_to_db:
            full_path_to_fixture = path_base / Path(app + '/fixtures/') / file
            call_command('loaddata', full_path_to_fixture)
