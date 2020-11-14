from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('movies', views.MovieViewSet)
router.register('ratings', views.RatingViewSet)
router.register('movie-rcmds', views.MovieRcmdViewSet)
# router.register('users', views.UserViewSet)
# router.register('images', views.ImageViewSet)

urlpatterns = [
    path('', include(router.urls))
]
