from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_index, name='home_index'),
    url(r'^page$', views.home_index, name='home_index')
]