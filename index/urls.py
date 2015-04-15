from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('index.views',
    url(r'^$', 'home', name='init'),
)