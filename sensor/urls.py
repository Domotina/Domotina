from django.conf.urls import patterns, include, url


urlpatterns = patterns('sensor.views',
    url(r'^$', 'home', name='sensor_home'),
    url(r'(?P<pk>\d+)/$', 'place_view', name='sensor_place_view'),
)
