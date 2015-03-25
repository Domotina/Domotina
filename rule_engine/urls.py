from django.conf.urls import patterns, include, url


urlpatterns = patterns('rule_engine.views',
    url(r'^$', 'list_rules', name='list_rules'),
)
