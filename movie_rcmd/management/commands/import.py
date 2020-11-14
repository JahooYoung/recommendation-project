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
        movie_df = pd.read_csv(dataset / 'movies.csv')
        link_df = pd.read_csv(dataset / 'links.csv', usecols=['movieId', 'imdbId'])
        mean_rating_df = pd.read_csv(dataset / 'ratings.csv', usecols=['userId', 'movieId', 'rating'])\
            .groupby('movieId').mean()
        movie_df = movie_df.merge(link_df, on='movieId').merge(mean_rating_df, on='movieId')
        Movie.objects.all().delete()
        Movie.objects.bulk_create(
            Movie(id=row.movieId, title=row.title, genres=row.genres,
                imdb_id=row.imdbId, mean_rating=row.rating)
            # for row in tqdm(movie_df.itertuples(), desc='importing movies', total=movie_df.size)
            for row in movie_df.itertuples()
        )
        # for row in tqdm(movie_df.itertuples(), desc='importing movies', total=movie_df.size):
        #     # try:
        #     movie = Movie.objects.get_or_create(pk=row.movieId)[0]
        #     movie.title = row.title
        #     movie.genres = row.genres
        #     movie.imdb_id = row.imdbId
        #     movie.tmdb_id = int(row.tmdbId) if not math.isnan(row.tmdbId) else None
        #     movie.save()
            # except Exception as e:
            #     print(f'{row=}\n{movie=}')
            #     raise e

            # try:
            #     poll = Movie.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % dataset)

            # poll.opened = False
            # poll.save()

        self.stdout.write(self.style.SUCCESS('Successfully import "%s"' % dataset))
