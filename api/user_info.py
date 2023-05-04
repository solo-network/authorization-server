import logging
from .base_endpoint                                                 import BaseEndpoint
from authlete.django.handler.userinfo_request_handler               import UserInfoRequestHandler
from authlete.django.handler.spi.userinfo_request_handler_spi       import UserInfoRequestHandlerSpi
from django.contrib.auth.models import User
from django.http import JsonResponse
import pandas

class UserInfoObject(UserInfoRequestHandlerSpi):
    def getSub(self, response):
        user = User.objects.get(id=response.subject)
        userinfo = {'sub': user.id, 'firstname': user.first_name, 'lastaname': user.last_name, 'username': user.username, 'email': user.email}
        return userinfo

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


    def handle(self, request):
        res = {
                "sub"         : "1",
                "name"        : "",
                "given_name"  : "KB4_03",
                "family_name" : "",
                "email"       : "",
                "picture"     : ""
            }
        # userinfo = UserInfoRequestHandler(self.api, UserInfoObject())
        # return userinfo.handle(request)
        return JsonResponse(res)
    

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
        dataframe_user_list = pandas.read_excel('lista.xlsx')
        counter = 0
        for index, row in dataframe_user_list.iterrows():
            firstname = self.get_first(row)
            lastname = self.get_lastname(row)
            email = row['E-mail']
            username = row['Login']
            new_user=User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username)
            new_user.save()
            counter += 1

        return f'total de usuarios criados: {counter}'