from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_index, name='home_index'),
    url(r'^map/$', views.home_index, name='home_index'),
    # url(r'^page$', views.home_index, name='home_index'),
    url(r'^search$', views.search_article, name='search_article'),
    url(r'^map/(?P<article>[^/]+)/$', views.display_map, name='display_map'),
    url(r'^mapelem/(?P<article>[^/]+)/$', views.map_elements, name='display_map'),
    # url(r'^debug/(?P<url>[^/]+)/$', views.display_scores_debug)
    # url(r'^(?P<userpage>\w+)/', include('topics.urls')),
]