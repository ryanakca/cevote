from django.conf.urls.defaults import *

urlpatterns = patterns('cevote.results.views',
    (r'^$', 'index'),
)
