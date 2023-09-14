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


import logging
from django.contrib.auth import authenticate, login
from authlete.django.handler.authorization_request_decision_handler import AuthorizationRequestDecisionHandler
from .base_endpoint                                                 import BaseEndpoint
from .spi.authorization_request_decision_handler_spi_impl           import AuthorizationRequestDecisionHandlerSpiImpl
import requests
import json
from django.contrib.auth.models import User
from django.shortcuts           import redirect
from django.http import QueryDict
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from logs.setup_log import logger

logger = logging.getLogger(__name__)


class AuthorizationDecisionEndpoint(BaseEndpoint):
    def __init__(self, api):
        super().__init__(api)


    def handle(self, request):
        try:
            logger.debug('in handle function')
            # Authenticate the user if necessary.
            authentication = self.__authenticateUserIfNecessary(request)
            logger.debug(f'authentication function result: {authenticate}')
            print(f'authentication function result: {authenticate}')
            # Flag which indicates whether the user has given authorization
            # to the client application or not.
            authorized = self.__isClientAuthorized(request)
            logger.debug(f'authorization function debug: {authorized}')

            # Log headers
            for header, value in request.headers:
                logger.debug('Header: %s: %s', header, value)

            # Log data (body)
            logger.debug('Body: %s', request.data.decode('utf-8'))

            # Process the authorization request according to the user's decision.
            if authentication:
                print('Authenticated! Returning OAuth defult flow')
                return self.__handleDecision(request, authorized)
            else:
                logger.debug('Authentication failed. Returning error to template.')
                uri = request.POST['uri']
                uri_parts = list(urlparse(uri))
                query = dict(parse_qsl(uri_parts[4]))
                query.update({'message': 'Acesso negado, verifique seu usuário e senha.'})
                uri_parts[4] = urlencode(query)
                uri = urlunparse(uri_parts)
                return redirect(uri)
        except Exception as error:
            logger.debug(error)
            return


    def __checkUserInCelepar(self, loginId, password):
        payload = {"username": loginId, "password": password}
        header = {'Content-Type': 'application/json'}
        response = requests.post('https://api.expresso.pr.gov.br/celepar/user/bind', headers=header, data=json.dumps(payload))
        return bool(response.json()['result'])

    def __checkIfUserExistsInDatabase(self, loginId, password):
        user = User.objects.filter(username=loginId).exists()
        if not user:
            user = User.objects.create_user(username=loginId, password=password)
            user.save()
        else:
            user = User.objects.get(username=loginId)
            password_match = user.check_password(password)
            if not password_match:
                user.set_password(password)
                user.save()

    def __authenticateUserIfNecessary(self, request):
        logger.debug("Check authentication for login ID {}.".format(request.POST.get('loginId')))
        if request.user.is_authenticated:
            # The user has already logged in.
            return

        loginId  = request.POST.get('loginId')
        loginId  = loginId.lower()
        password = request.POST.get('password')
        check_in_celepar = self.__checkUserInCelepar(loginId, password)
        if check_in_celepar:
            self.__checkIfUserExistsInDatabase(loginId, password)
            # Authenticate the user.
            user = authenticate(username=loginId, password=password)
            if user is None:
                # User authentication failed.
                logger.debug("authorization_decision_endpoint: User authentication failed. The presented login ID is {}.".format(loginId))
                return
            logger.debug("authorization_decision_endpoint: User authentication succeeded. The presented login ID is {}.".format(loginId))
            # Let the user log in.
            login(request, user)
            return True
        else:
            return False

    def __isClientAuthorized(self, request):
        # If the user pressed the "Authorize" button, the request contains
        # an "authorized" parameter.
        return ('authorized' in request.POST)


    def __handleDecision(self, request, authorized):
        try:
            spi     = AuthorizationRequestDecisionHandlerSpiImpl(request, authorized)
            handler = AuthorizationRequestDecisionHandler(self.api, spi)
            # Parameters contained in the response from /api/auth/authorization API.
            session      = request.session
            ticket       = session.get('ticket')
            claimNames   = session.get('claimNames')
            claimLocales = session.get('claimLocales')

            return handler.handle(ticket, claimNames, claimLocales)
        except Exception as error:
            print(error)
  