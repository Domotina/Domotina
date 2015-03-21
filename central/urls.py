from django.conf.urls import patterns, include, url


urlpatterns = patterns('central.views',
    url(r'^$', 'central_home', name='central_home'),
    url(r'^create/', 'central_create', name="central_create")
)
