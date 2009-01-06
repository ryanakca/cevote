# Voting URL file.
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

urlpatterns = patterns('cevote.voting.views',
    (r'^$', 'vote'),
    (r'^login/$', 'login'),
)

urlpatterns += patterns('',
    (r'^success/$', 'django.contrib.auth.views.logout',
                    {'template_name': 'vote/success.html'})
)
