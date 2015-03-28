from django.conf.urls import patterns, include, url


urlpatterns = patterns('rule_engine.views',
    url(r'^$', 'list_rules', name='list_rules'),
    url(r'^new$', 'create_rule', name='create_rule'),
    url(r'^(?P<rule>\d+)$', 'edit_rule', name='edit_rule'),
    url(r'^(?P<rule>\d+)/delete$', 'delete_rule', name='delete_rule'),
)
