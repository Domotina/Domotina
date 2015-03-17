from django.conf.urls import patterns, include, url


urlpatterns = patterns('central.views',
    url(r'^$', 'central_home', name='central_home'),
    url(r'(?P<pk>\d+)/$', 'central_create', name="central_create_view")
)
