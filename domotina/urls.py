from django.conf.urls import patterns, include, url
from rest_framework import routers
from event_manager import views
from django.contrib import admin

admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^map/', include('map.urls')),
    url(r'^sensor/', include('sensor.urls')),
)