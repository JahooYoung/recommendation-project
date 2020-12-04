from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *

# class UserConciseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username']

class RcmdStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RcmdStat
        fields = '__all__'
        read_only_fields = ['timestamp', 'rcmd_click_num']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'movie']
        read_only_fields = ['id']


class MovieRcmdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRcmd
        fields = ['id', 'movie']
        read_only_fields = ['id']
        depth = 1


class MovieSerializer(serializers.ModelSerializer):
    # owner = UserConciseSerializer(read_only=True)
    # rating = RatingSerializer(source='ratings')

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genres', 'imdb_id', 'mean_rating', 'total_rating']
        read_only_fields = ['id', 'title', 'genres', 'imdb_id', 'mean_rating', 'total_rating']
        # depth = 1

    # @classmethod
    # def many_init(cls, *args, **kwargs):
    #     allow_empty = kwargs.pop('allow_empty', None)
    #     child_serializer = cls(*args, **kwargs)
    #     # Don't show body when retrieving multiple movies
    #     child_serializer.fields.pop('ratings')
    #     list_kwargs = {
    #         'child': child_serializer,
    #     }
    #     if allow_empty is not None:
    #         list_kwargs['allow_empty'] = allow_empty
    #     list_kwargs.update({
    #         key: value for key, value in kwargs.items()
    #         if key in serializers.LIST_SERIALIZER_KWARGS
    #     })
    #     meta = getattr(cls, 'Meta', None)
    #     list_serializer_class = getattr(meta, 'list_serializer_class', serializers.ListSerializer)
    #     return list_serializer_class(*args, **list_kwargs)


# class UserSerializer(serializers.ModelSerializer):
#     documents = serializers.HyperlinkedRelatedField(
#         many=True, view_name='document-detail', read_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'is_staff', 'documents']


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = ['image', 'document']
