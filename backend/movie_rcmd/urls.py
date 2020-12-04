from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('movies', views.MovieViewSet)
router.register('ratings', views.RatingViewSet)
router.register('movie-rcmds', views.MovieRcmdViewSet)
router.register('rcmd-stats', views.RcmdStatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('run-recommendation/', views.RunRecommendation.as_view()),
    path('kafka/', views.KafkaForward.as_view())
]
