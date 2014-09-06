from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Pages
    url(r'^$', 'gitorial.views.index', name='index'),

    # logout
    url(r'logout/', 'gitorial.views.logout', name='logout'),

    # API
    url(r'^api/(?P<username>.+)/(?P<tutname>[0-9]+)', views.tutorial),
    url(r'^api/(?P<username>.+)', views.user),
)
