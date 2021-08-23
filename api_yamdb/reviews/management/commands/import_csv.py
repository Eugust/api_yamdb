import csv
import os

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Review, Title

User = get_user_model()

PAIRS = {
    'users': ['User', 'users', 'filepath'],
    'genre': ['Genre', 'reviews', 'filepath'],
    'titles': ['Title', 'reviews', 'filepath'],
    'comments': ['Comment', 'reviews', 'filepath'],
    'review': ['Review', 'reviews', 'filepath'],
    'category': ['Category', 'reviews', 'filepath'],
    'genre_title': ['Title', 'reviews', 'filepath']
}


class Command(BaseCommand):
    help = 'Upload CSV files into models'

    def find_sources(self, path):
        files = []
        for root, dirs, file_names in os.walk(path):
            for file_name in file_names:
                if file_name.endswith('.csv'):
                    file_path = os.path.join(root, file_name)
                    files.append(file_path)
        self.stdout.write(
            self.style.SUCCESS('... %s files found' % len(files))
        )
        return files

    def handle_file(self, keyword):
        model_name = PAIRS[keyword][0]
        app_name = PAIRS[keyword][1]
        file_path = PAIRS[keyword][2]

        _model = apps.get_model(app_name, model_name)
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            header = next(reader)
            for row in reader:
                _object_dict = {key: value for key, value in zip(header, row)}
                if model_name == 'Title':
                    category = Category.objects.get(
                        pk=_object_dict['category']
                    )
                    _object_dict['category'] = category
                if model_name == 'Review':
                    title = Title.objects.get(pk=_object_dict['title_id'])
                    _object_dict['title'] = title
                    author = User.objects.get(pk=_object_dict['author'])
                    _object_dict['author'] = author
                    _object_dict['score'] = int(_object_dict['score'])
                if model_name == 'Comment':
                    author = User.objects.get(pk=_object_dict['author'])
                    _object_dict['author'] = author
                    review = Review.objects.get(pk=_object_dict['review_id'])
                    _object_dict['review'] = review

                try:
                    _model.objects.create(**_object_dict)
                    self.stdout.write(self.style.SUCCESS('Record created'))
                except ValueError:
                    self.stdout.write(self.style.ERROR('Creation error'))

    def handle_connections(self, keyword):
        file_path = PAIRS[keyword][2]

        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            header = next(reader)
            for row in reader:
                try:
                    _object_dict = {
                        key: value for key, value in zip(header, row)}
                    title = Title.objects.get(pk=_object_dict['title_id'])
                    genre, created = Genre.objects.get_or_create(
                        pk=_object_dict['genre_id']
                    )
                    if genre and genre not in title.genre.all():
                        title.genre.add(genre)
                        title.save()
                        self.stdout.write(
                            self.style.SUCCESS('Record created')
                        )
                except ValueError:
                    self.stdout.write(self.style.ERROR('Creation error'))

    def handle(self, *args, **options):
        files = self.find_sources(os.getcwd())
        for file_path in files:
            file_name = os.path.basename(file_path).split('.', 1)[0]
            if file_name in PAIRS:
                PAIRS[file_name][2] = file_path
                self.stdout.write(self.style.SUCCESS('Record path for file'))

        self.handle_file('users')
        self.handle_file('category')
        self.handle_file('genre')
        self.handle_file('titles')
        self.handle_file('review')
        self.handle_file('comments')
        self.handle_connections('genre_title')

        self.stdout.write(self.style.SUCCESS('Finished with files'))
