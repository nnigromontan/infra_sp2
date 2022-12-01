"""Автоматизация наполнения БД."""

import json
from csv import DictReader
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Настройки инструмента для создания фикстур."""

    help = 'Creates fixtures for applications from csv files with data'

    def handle(self, *args, **options):
        """Создает фикстуры для приложений из csv файла."""
        # list contains data_file, application_name, model_name
        file_to_table = [
            ('titles.csv', 'reviews', 'Title'),
            ('category.csv', 'reviews', 'Category'),
            ('comments.csv', 'reviews', 'Comment'),
            ('genre.csv', 'reviews', 'Genre'),
            ('review.csv', 'reviews', 'Review'),
            ('users.csv', 'users', 'User'),
        ]
        path_base = settings.BASE_DIR
        path_to_csv = Path('static/data/')

        fixture_item = {}

        for file, app, table in file_to_table:
            full_path_to_fixtures = path_base / Path(app + '/fixtures/')
            full_path_to_fixtures.mkdir(parents=True, exist_ok=True)
            with open(path_base / path_to_csv / file, 'r') as read_file:
                data = DictReader(read_file)
                fixture_to_add = []
                for row in data:
                    fixture_item = {}
                    fixture_item['model'] = app + '.' + table
                    fixture_item['pk'] = row.pop('id')
                    fixture_item['fields'] = row
                    fixture_to_add.append(fixture_item)
                with open(full_path_to_fixtures / (table + '.json'),
                          'w') as write_file:
                    write_file.write(json.dumps(fixture_to_add))
                    print('Created', table + '.json')
