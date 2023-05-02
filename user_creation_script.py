import requests
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection


def get_token():
    url = 'https://solo-identity.azurewebsites.net/realms/master/protocol/openid-connect/token'
    myobj = {'grant_type': 'client_credentials', 'client_id': 'admin-cli', 'client_secret': 'e3dOzxVcATg3q82pD9WSRhic7fUvSa9z'}
    requested_token = requests.post(url, data=myobj, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    return requested_token.json()


def create_user(token):
    url = 'https://solo-identity.azurewebsites.net/admin/realms/master/users'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token}
    print(headers)
    myobj = {"firstName":"Sergey","lastName":"Kargopolov", "email":"test@test.com", "enabled":"true", "username":"app-user"}
    user_create = requests.post(url=url, data=myobj, headers=headers)
    return user_create.json()


if __name__ == "__main__":
    tk = get_token()
    print(tk['access_token'])
    user = create_user(tk['access_token'])
    print(user)