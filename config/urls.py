from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gitorial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # helper URLs for authentication
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Admin site
    url(r'^admin/', include(admin.site.urls)),

    # Gitorial site
    url('', include('gitorial.urls')),
)
