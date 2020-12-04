from django.conf import settings

if settings.IS_PRODUCTION:
    from djongo import models
else:
    from django.db import models


# Create your models here.

class Movie(models.Model):
    # owner = models.ForeignKey('auth.User', related_name="documents", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    genres = models.TextField(max_length=300, blank=True)
    imdb_id = models.IntegerField(null=True)
    mean_rating = models.FloatField(default=0.0)  # only calculate in static dataset
    total_rating = models.FloatField(default=0.0)
    # tmdb_id = models.IntegerField(null=True)

    # class Meta:
    #     # The default ordering for the object, for use when obtaining lists of objects
    #     ordering = ('-last_modified',)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        super(Movie, self).save(*args, **kwargs)


class Rating(models.Model):
    user = models.ForeignKey('auth.User', related_name='ratings', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('user', 'movie')


class MovieRcmd(models.Model):
    user = models.ForeignKey('auth.User', related_name='movie_rcmd', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='+', on_delete=models.CASCADE)
    rating = models.FloatField()


class RcmdStat(models.Model):
    timestamp = models.IntegerField(primary_key=True)
    rcmd_click_num = models.IntegerField()

    class Meta:
        ordering = ('-timestamp',)
