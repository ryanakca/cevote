from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'cevote.results.views.index'),
)
