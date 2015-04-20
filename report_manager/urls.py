from django.conf.urls import patterns, include, url


urlpatterns = patterns('report_manager.views',
    url(r'^(?P<place_pk>\d+)/$', 'home', name='report_home'),
    url(r'^(?P<place_pk>\d+)/events/$', 'events_in_date_range', name='report_events_in_date_range'),
)
