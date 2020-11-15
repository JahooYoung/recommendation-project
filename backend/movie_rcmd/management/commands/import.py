import math
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from django.core.management.base import BaseCommand, CommandError
from ...models import Movie

class Command(BaseCommand):
    help = 'Import csv dataset'

    def add_arguments(self, parser):
        # parser.add_argument('datasets', nargs='+', type=str)
        parser.add_argument('dataset', type=str)

    def handle(self, *args, **options):
        dataset = Path(options['dataset'])
        self.stdout.write('importing "%s"' % dataset)

        movie_df = pd.read_csv(dataset / 'movies.csv')
        link_df = pd.read_csv(dataset / 'links.csv', usecols=['movieId', 'imdbId'])
        rating_df = pd.read_csv(dataset / 'ratings.csv', usecols=['userId', 'movieId', 'rating'])
        mean_rating_df = rating_df.groupby('movieId').mean()
        total_rating_df = rating_df.groupby('movieId').sum()
        movie_df = movie_df.merge(link_df, on='movieId') \
            .merge(mean_rating_df, on='movieId') \
            .merge(total_rating_df, on='movieId', suffixes=('_mean', '_sum'))
        Movie.objects.all().delete()
        Movie.objects.bulk_create(
            Movie(id=row.movieId, title=row.title, genres=row.genres, imdb_id=row.imdbId,
                mean_rating=row.rating_mean, total_rating=row.rating_sum)
            # for row in tqdm(movie_df.itertuples(), desc='importing movies', total=movie_df.size)
            for row in movie_df.itertuples()
        )

        self.stdout.write(self.style.SUCCESS('Successfully imported "%s"' % dataset))
