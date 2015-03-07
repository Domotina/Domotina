from django.conf.urls import patterns, include, url


urlpatterns = patterns('map.views',
    url(r'^$', 'home', name='map_home'),
    url(r'(?P<pk>\d+)/$', 'place_view', name='map_place_view'),
)
