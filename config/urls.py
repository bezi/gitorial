from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # helper URLs for authentication
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Admin site
    url(r'^admin/', include(admin.site.urls)),

    # Gitorial site
    url('', include('gitorial.urls')),
)
