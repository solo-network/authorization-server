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


from django.conf                         import settings
from django.views.decorators.csrf        import csrf_exempt
from django.views.decorators.http        import require_GET, require_POST, require_http_methods
from authlete.django.handler             import *
from .authorization_decision_endpoint    import AuthorizationDecisionEndpoint
from .authorization_endpoint             import AuthorizationEndpoint
from .introspection_endpoint             import IntrospectionEndpoint
from .spi.token_request_handler_spi_impl import TokenRequestHandlerSpiImpl
from .user_info import UserInfo, Root, CreateUser
from django.http import JsonResponse


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def authorization(request):
    """Authorization Endpoint"""
    return AuthorizationEndpoint(settings.AUTHLETE_API).handle(request)


@require_POST
def authorization_decision(request):
    """Authorization Decision Endpoint"""
    return AuthorizationDecisionEndpoint(settings.AUTHLETE_API).handle(request)


@require_GET
def configuration(request):
    """Discovery Endpoint (.well-known/openid-configuration)"""
    return ConfigurationRequestHandler(settings.AUTHLETE_API).handle(request)


@require_POST
@csrf_exempt
def introspection(request):
    """Introspection Endpoint"""
    return IntrospectionEndpoint(settings.AUTHLETE_API).handle(request)


@require_GET
def jwks(request):
    """JWK Set Endpoint"""
    return JwksRequestHandler(settings.AUTHLETE_API).handle(request)


@require_POST
@csrf_exempt
def revocation(request):
    """Revocation Endpoint"""
    return RevocationRequestHandler(settings.AUTHLETE_API).handle(request)


@require_POST
@csrf_exempt
def token(request):
    """Token Endpoint"""
    return TokenRequestHandler(
        settings.AUTHLETE_API, TokenRequestHandlerSpiImpl()).handle(request)

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def userinfo(request):
    """User Info"""
    return CreateUser(settings.AUTHLETE_API).handle(request)

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def root(request):
    """User Info"""
    return Root(settings.AUTHLETE_API).handle(request)

@csrf_exempt
def handle_user(request, username):
    return CreateUser(settings.AUTHLETE_API).get_user_by_username(username)

@csrf_exempt
def activate_user(request, username):
    return CreateUser(settings.AUTHLETE_API).activate_user(username)

@csrf_exempt
def deactivate_user(request, username):
    return CreateUser(settings.AUTHLETE_API).deactivate_user(username)

@csrf_exempt
def remove_user(request, username):
    return CreateUser(settings.AUTHLETE_API).remove_user(username)

@csrf_exempt
def handle_users(request, page):
    return CreateUser(settings.AUTHLETE_API).get_users_by_page(page)

@csrf_exempt
def deactivate_users(request):
    return CreateUser(settings.AUTHLETE_API).deactivate_users()

@require_http_methods(['POST'])
@csrf_exempt
def handle_user_updates(request):
    if request.method == 'POST':
        update_data = request.body.decode('utf-8')
        response_message = CreateUser(settings.AUTHLETE_API).handle_user_updates(update_data)
        return JsonResponse({'message': response_message})