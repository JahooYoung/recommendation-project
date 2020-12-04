from django.contrib import admin

# Register your models here.

from .models import *


# class MovieAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,      {'fields': ['title']}),
#         ('Details', {'fields': ['imdb_id']}),
#     ]
#     list_display = ('title', 'imdb_id')
# admin.site.register(Movie, MovieAdmin)

admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(MovieRcmd)
admin.site.register(RcmdStat)
