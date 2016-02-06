from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.index_public, name='index-public'),
]
