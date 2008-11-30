# Django URL file.
# Copyright (C) 2008  Ryan Kavanagh <ryanakca@kubuntu.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from django.conf.urls.defaults import *
from cevote.voting.models import Position

# for the settings.DEBUG
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
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
