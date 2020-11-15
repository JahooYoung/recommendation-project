import os
from django.http import Http404, HttpResponse, FileResponse
from rest_framework import viewsets, permissions, filters, generics, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *

# Create your views here.

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly,
    ]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        'title': ['exact'],
        'total_rating': ['gte']
    }
    search_fields = ['=id', 'title', 'genres', '^imdb_id']
    ordering_fields = ['id', 'imdb_id', 'mean_rating']

    # overrides method of class CreateModelMixin.
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        movie = self.get_object()
        data = self.get_serializer(movie).data
        try:
            rating = Rating.objects.get(user=request.user, movie=movie)
            data['rating'] = RatingSerializer(rating).data
        except Rating.DoesNotExist:
            pass
        return Response(data)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieRcmdViewSet(viewsets.ModelViewSet):
    queryset = MovieRcmd.objects.all()
    serializer_class = MovieRcmdSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)


# class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     # permission_classes = (IsEventHostAdminOrReadOnly|IsAdminUser,)
#     pk_type = 'movie'

#     def get(self, request, *args, **kwargs):
#         try:
#             movie = Movie.objects.get(pk=kwargs.get('pk'))
#         except Movie.DoesNotExist:
#             raise Http404
#         data = self.retrieve(request, *args, **kwargs).data

#         # data['event_admin'] = check_is_admin(request.user, obj)
#         try:
#             rating = Rating.objects.get(user=request.user, movie=movie)
#             data['rated'] = True
#             data['user_register_event'] = RatingSerializer(rating).data
#         except Rating.DoesNotExist:
#             data['rated'] = False

#         return Response(data)

RCMD_PROG = os.path.join(os.path.dirname(__file__), 'recommend.py')

class RunRecommendation(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    pid = None

    def get(self, request, *args, **kwargs):
        if self.pid is None:
            return Response(status=400)
        _, status = os.waitpid(self.pid, os.WNOHANG)
        is_ended = os.WIFSIGNALED(status) or os.WIFEXITED(status)
        if is_ended:
            self.pid = None
        return Response({'is_ended': is_ended})

    def post(self, request, *args, **kwargs):
        if self.pid is not None:
            return Response(status=400)
        self.pid = os.spawnvp(os.P_NOWAIT, 'python', [RCMD_PROG])
        return Response(status=201)
