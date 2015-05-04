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
    url(r'^report/$', 'central_month_report', name="central_month_report"),
    url(r'^report/gen/', 'generate_monthly_report', name="generate_monthly_report"),
    url(r'^report/web/', 'generate_monthly_report_web', name="generate_monthly_report_web"),
    url(r'^getHouses/$', 'getHouses', name="getHouses"),
    url(r'^(?P<place_pk>\d+)/delegateoption/', 'delegateoption', name="delegateoption"),
    url(r'^([0-9])/edit/([0-9])/$', 'editdelegate', name='editdelegate'),

        # Administracion de urbanizaciones y/o edificios
    url(r'^neighborhood$', 'list_neighborhoods', name='list_neighborhoods'),
    url(r'^neighborhood/new$', 'create_neighborhood', name='create_neighborhood'),
    url(r'^neighborhood/(?P<neighborhood_pk>\d+)/delete$', 'delete_neighborhood', name='delete_neighborhood'),
    url(r'^neighborhood/(?P<neighborhood_pk>\d+)$', 'edit_neighborhood', name='edit_neighborhood'),
)
