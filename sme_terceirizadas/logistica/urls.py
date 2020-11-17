from django.urls import include, path
from rest_framework import routers

from .api import viewsets

router = routers.DefaultRouter()

router.register('solicitacao-remessa', viewsets.SolicitacaoModelViewSet,
                basename='solicitacao-remessa')

urlpatterns = [
    path('', include(router.urls)),
]
