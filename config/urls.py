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
    url(r'^stats', src.views.stats, name='stats'),
    url(r'^admin/', include(admin.site.urls)),
]
