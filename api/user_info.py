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
import json
from .decorators import allow_specific_origin
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage

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
    
    def get_user_by_username(self, username):
        try:
            user = User.objects.get(username=username)
            user_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                # Add other fields as needed
            }
            logging.debug(user_data)
            return JsonResponse(user_data)
        except ObjectDoesNotExist:
            response_data = {'error': f"User with username {username} does not exist."}
            return JsonResponse(response_data, status=404)

    def get_users_by_page(self, page=0):
        users_list = []
        users = User.objects.all().order_by('id')

        if page == 0:
            for user in users:
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_active': user.is_active,
                }
                users_list.append(user_data)
        else:
            paginator = Paginator(users, 20)

            try:
                users_page = paginator.page(page)
            except EmptyPage:
                # If the page is out of range, return an empty result
                return JsonResponse({'error': 'Page out of range'}, status=404)

            for user in users_page:
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_active': user.is_active,
                }
                users_list.append(user_data)

        return JsonResponse({'users': users_list})

    def deactivate_users(self):
        User.objects.update(is_active=False)
        return JsonResponse({'message': 'All users have been deactivated'})

    def activate_user(request, username):
        try:
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            return JsonResponse({'message': f'User {username} activated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': f'User with username {username} does not exist.'}, status=404)
    
    def deactivate_user(request, username):
        try:
            user = User.objects.get(username=username)
            user.is_active = False
            user.save()
            return JsonResponse({'message': f'User {username} deactivated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': f'User with username {username} does not exist.'}, status=404)
        
    def remove_user(request, username):
        try:
            user = User.objects.get(username=username)
            user.delete()
            return JsonResponse({'message': f'User {username} deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': f'User with username {username} does not exist.'}, status=404)

    def handle_user_updates(self, user_list):
        try:
            user_list = json.loads(user_list)

            # Iterate through the user list and update or create users
            for user_data in user_list:
                username = user_data['username']
                existing_user = User.objects.filter(username=username).first()

                if existing_user:
                    # Update user attributes
                    for attr, value in user_data.items():
                        if attr != 'username':
                            setattr(existing_user, attr, value)
                    existing_user.save()
                else:
                    # Create a new user
                    User.objects.create_user(**user_data)

            # Users to always keep active
            always_active_users = ["root", "kb4_04", "Sivirmond", "kb4_cel_001"]
            
            # Deactivate users not in the provided list in a batch operation
            User.objects.filter(is_active=True).exclude(username__in=[user_data['username'] for user_data in user_list] + always_active_users).update(is_active=False)

            # Count total number of users and active users
            total_users = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.debug(f"Start of update: {current_time}")
            logging.debug(f"Processed users: {len(user_list)}")
            logging.debug(f"Total number of users: {total_users}")
            logging.debug(f"Number of active users: {active_users}")

            return 'User updates handled successfully'
        except Exception as error:
            logging.debug(error)
            return 'Error handling user updates'

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
        return redirect('https://training.knowbe4.com/auth/saml/5a6d8defa9be6')