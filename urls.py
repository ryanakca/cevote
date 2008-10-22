from django.conf.urls.defaults import *

# for the settings.DEBUG
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^cevote/', include('cevote.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^results/', include('cevote.results.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^$', include('cevote.voting.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media_dir/(?P<path>.*)$', 'django.views.static.serve', \
            {'document_root': '/home/ryan/work/cevote/media_dir/'}),
    )
