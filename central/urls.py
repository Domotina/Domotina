from django.conf.urls import patterns, include, url


urlpatterns = patterns('central.views',
    url(r'^$', 'central_home', name='central_home'),
    url(r'^create/', 'central_create', name="central_create"),
    url(r'^owner/', 'central_owner_principal', name="central_owner_principal"),
    url(r'^owner_individual/', 'central_individual_load', name="central_individual_load"),
    url(r'^owner_huge/', 'central_huge_load', name="central_huge_load"),
    url(r'^create_owner/', 'create_owner', name="create_owner")
)
