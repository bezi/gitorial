from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Pages
    url(r'^$', 'gitorial.views.index', name='index'),

    # API
    url(r'^(?P<username>.+)/(?P<tutname>[0-9]+)', views.tutorial),
    url(r'^(?P<username>.+)', views.user),
)
