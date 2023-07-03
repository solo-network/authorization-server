from .base_endpoint                                                 import BaseEndpoint
from authlete.django.handler.spi.userinfo_request_handler_spi       import UserInfoRequestHandlerSpi
from authlete.django.handler.spi.userinfo_request_handler_spi_adapter import UserInfoRequestHandlerSpiAdapter
from authlete.django.handler.userinfo_request_handler               import UserInfoRequestHandler
from django.contrib.auth.models import User
from django.http import JsonResponse
import pandas
from authlete.django.web.request_utility          import RequestUtility
from authlete.dto.userinfo_request                import UserInfoRequest
from django.shortcuts           import redirect
from logs.setup_log import logging


class UserInfoObject(UserInfoRequestHandlerSpi):

    def getUserClaimValue(self, subject, claimName, languageTag):
        """Get the value of a claim of a user.

        This method may be called multiple times.

        Args:
            subject (str) : The subject (= unique identifier) of a user.
            claimName (str) : A claim name such as "name" and "family_name".
            languageTag (str) : A language tag such as "en" and "ja".

        Returns:
            object :
                The value of the claim. None if the value is not available.
                In most cases, an instance of str should be returned. When
                "claimName" is "address", an instance of authlete.dto.Address
                should be returned.
        """

        return {'subject': subject, 'claimName': claimName, 'languageTag': languageTag}
        


class UserInfo(BaseEndpoint):
    def __init__(self, api):
        super().__init__(api)

    def __callUserInfoApi(self, accessToken):
        # Create a request for /api/auth/userinfo API.
        try:
            req = UserInfoRequest()
            req.token = accessToken

            # Call /api/auth/userinfo API.
            return self.api.userinfo(req)
        except Exception as error:
            print(error)

    def handle(self, request):
        try:
            # accessToken = RequestUtility.extractBearerToken(request)
            # res = self.__callUserInfoApi(accessToken)

            # content = res.responseContent
            # print(f'content: {content}')
            return JsonResponse({'teste': 'tete'})
        except Exception as error:
            print(error)

class CreateUser(BaseEndpoint):
    def __init__(self, api):
        super().__init__(api)

    def handle(self, request):
        func = self.handling_excel()
        return JsonResponse({'Status': 'Done', 'Result': func})

    def get_first(self, row):
        nomes = row['Nome']
        lista_nomes = nomes.split(' ')
        primeiro_nome = lista_nomes[0]
        ultimo_nome = lista_nomes[-1]
        return ultimo_nome

    def get_lastname(self, row):
        nomes = row['Nome']
        lista_nomes = nomes.split(' ')
        primeiro_nome = lista_nomes[0]
        ultimo_nome = lista_nomes[-1]
        return primeiro_nome

    def handling_excel(self):
        # dataframe_user_list = pandas.read_excel('lista.xlsx')
        dataframe_user_list = pandas.read_csv('kb4.csv', usecols=['uid', 'mail', 'givenName', 'sn'])
        counter = 0
        try:
            for index, row in dataframe_user_list.iterrows():
                firstname = row['givenName']
                lastname = row['sn']
                email = row['mail']
                username = row['uid']
                new_user=User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username)
                new_user.save()
                counter += 1

            return f'total de usuarios criados: {counter}'
        except Exception as error:
            logging.debug(error)
    
class Root(BaseEndpoint):
    def __init__(self, api):
        super().__init__(api)

    def handle(self, request):
        return redirect('https://www.universidadecorporativa.celepar.pr.gov.br/')