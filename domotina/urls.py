from django.conf.urls import patterns, include, url
from rest_framework import routers
from event_manager import views

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'domotina.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
