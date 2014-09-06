from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gitorial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'gitorial.views.index', name='index'),

    url(r'^user/(?P<username>.+)/', 'views.user', name='user'),
)
