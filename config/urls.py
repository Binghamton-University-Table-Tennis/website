from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import src.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', src.views.index, name='index'),
    url(r'^log', src.views.log, name='log'),
    url(r'^about', src.views.about, name='about'),
    url(r'^ladder', src.views.ladder, name='ladder'),
    url(r'^contact', src.views.contact, name='contact'),
    url(r'^rules', src.views.rules, name='rules'),
    url(r'^stats/(?P<player>.*)', src.views.stats, name='stats'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', src.views.search, name='search'),
    url(r'^attendance/', src.views.attendance, name='attendance'),
    url(r'^history/(?P<date>.*)', src.views.history, name='history'),
]
