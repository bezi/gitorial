from django.conf.urls import patterns, include, url
from django.contrib import admin

from gitorial import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gitorial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<username>.+)/(?P<tutname>[0-9]+)', views.tutorial),
    url(r'^(?P<username>.+)', views.user),
)
