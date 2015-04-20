from django.conf.urls import patterns, include, url


urlpatterns = patterns('central.views',
    url(r'^$', 'central_home', name='central_home'),
    url(r'^create/', 'central_create', name="central_create"),
    url(r'^owner/', 'central_owner_principal', name="central_owner_principal"),
    url(r'^owner_individual/', 'central_individual_load', name="central_individual_load"),
    url(r'^owner_huge/', 'central_huge_load', name="central_huge_load"),
    url(r'^delegate/', 'central_delegate', name="central_delegate"),
    url(r'^delegate_individual/', 'central_individual_delegate_load', name="central_individual_delegate_load"),
    url(r'^delegate_huge/', 'central_huge_delegate_load', name="central_huge_delegate_load"),
    url(r'^building-neigh/', 'central_building_neigh', name="central_building_neigh"),
    url(r'^create_building-neigh/', 'central_building_create', name="central_building_create"),
    url(r'^report/', 'central_month_report', name="central_month_report"),
    url(r'^getHouses/$', 'getHouses', name="getHouses"),
)
