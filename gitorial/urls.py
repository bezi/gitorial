from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Pages
    url(r'^$', 'gitorial.views.index', name='index'),

    # login/logout
    url(r'logout/', 'gitorial.views.logout', name='logout'),

    # get session
    url(r'api/session/', 'gitorial.views.session', name='session'),

    # API
    url(r'^api/(?P<username>.+)/(?P<tutnum>[0-9]+)/$', views.tutorial),
    url(r'^api/(?P<username>.+)/(?P<repo>.+)/$', views.tutorial_new),
    url(r'^api/(?P<username>.+)/$', views.user_view),
)
