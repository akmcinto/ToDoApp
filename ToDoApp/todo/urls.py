"""
   Copyright 2016 Andrea McIntosh

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 """

from django.conf.urls import url, include
from . import views

app_name = 'todo'
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.list_details, name='detail'),
    url(r'^(?P<pk>[0-9]+)/newitem/$', views.new_item, name='new_item'),
    url(r'^newlist/$', views.new_list, name='new_list'),
    url(r'^register/$', views.register, name='register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', views.user_logout, name='logout'),
    url(r'^accounts/viewlists/$', views.view_lists, name='viewlists'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
