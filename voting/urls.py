from django.conf.urls.defaults import *

urlpatterns = patterns('cevote.voting.views',
    (r'^$', 'vote'),
)
