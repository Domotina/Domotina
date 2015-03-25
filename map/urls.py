from django.conf.urls import patterns, include, url


urlpatterns = patterns('map.views',
    url(r'^$', 'my_places', name='map_home'),
    url(r'(?P<pk>\d+)/$', 'place_view', name='map_place_view'),
    url(r'(?P<place>\d+)/rules/', include('rule_engine.urls')),
)
