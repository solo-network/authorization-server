#
# Copyright (C) 2019 Authlete, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the
# License.


from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('authorization',          views.authorization),
    path('authorization/decision', views.authorization_decision, name='authorization_decision'),
    path('jwks',                   views.jwks),
    path('introspection',          views.introspection),
    path('revocation',             views.revocation),
    path('token',                  views.token),
    path('userinfo/',              views.userinfo),
    path('userupdates/',           views.handle_user_updates, name='handle_user_updates'),
    path('_user/<str:username>',   views.handle_user, name='handle_user'),
    path('_users/<int:page>/',     views.handle_users, name='handle_users'),
    path('_de_users/',             views.deactivate_users, name='deactivate_users'),
    path('_deact_user/<str:username>/', views.deactivate_user, name='deactivate_user'),
    path('_act_user/<str:username>/', views.activate_user, name='activate_user'),
    path('_ruser/<str:username>/', views.remove_user, name='remove_user'),
]
