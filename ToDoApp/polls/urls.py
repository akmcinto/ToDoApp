from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^$', views.detail, name='detail'),
    url(r'^$', views.results, name="results"),
    url(r'^$', views.vote, name='vote'),
]
