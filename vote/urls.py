# Voting URL file.
# Copyright (C) 2008, 2009  Ryan Kavanagh <ryanakca@kubuntu.org>
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

from cevote import settings

urlpatterns = patterns('vote.views',
    (r'^$', 'vote'),
    (r'^login/$', 'login'),
)

urlpatterns += patterns('',
    (r'^success/$', 'django.contrib.auth.views.logout',
                    {'template_name': 'vote/success.html'}),
    (r'^copyright/$', 'django.views.generic.simple.direct_to_template',
                    {'template': 'vote/copyright.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^candidate_pictures/(?P<path>.*)$', 'django.views.static.serve', \
            {'document_root':
            '/home/ryan/work/cevote/media_dir/vote/candidate_pictures/'}),
    )
