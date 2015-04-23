from django.conf.urls import patterns, include, url
from rest_framework import routers
from django.contrib import admin

from map.views import SensorViewSet


admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'sensors', SensorViewSet)
urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('registration.backends.simple.urls')),
                       url(r'^api/', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^map/', include('map.urls')),
                       url(r'^', include('index.urls')),
                       url(r'^central/', include('central.urls')),
                       url(r'^report/', include('report_manager.urls')),
                       )
