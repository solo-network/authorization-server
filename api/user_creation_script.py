import requests
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
import pandas
from user_creation import create_user as int_create_user

# Goal: Get an access token using client credentials
#
# returns: JSON response containing the access token
def get_token():
    url = 'https://solo-identity.azurewebsites.net/realms/master/protocol/openid-connect/token'
    myobj = {
                'grant_type': 'client_credentials', 
                'client_id': 'admin-cli',
                'client_secret': 'nRf1tOzHGl12Bh0ZupKsVG181LGFFsir'
             }
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    requested_token = requests.post(url, data=myobj, headers=header)
    return requested_token.json()

# Goal: Create a user using the obtained token and provided data
#
# params:
#     token (str) - Access token obtained from Keycloak
#     firstname (str) - First name of the user
#     lastname (str) - Last name of the user
#     email (str) - Email of the user
#     username (str) - Username of the user
#
# returns: Response text from the user creation request
def create_user(token, firstname, lastname, email, username):
    url = 'https://solo-identity.azurewebsites.net/admin/realms/Celepar/users'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token}
    myobj = {
                "firstName":firstname,
                "lastName":lastname,
                "email":email,
                "enabled":True,
                "username": username
            }
    user_create = requests.post(url=url, json=myobj, headers=headers)
    return user_create.text

# Goal: Extract the last name from a given row
#
# params:
#     row (pandas.Series) - Row containing user data
#
# returns: Last name extracted from the row
def get_first(row):
    nomes = row['Nome']
    lista_nomes = nomes.split(' ')
    primeiro_nome = lista_nomes[0]
    ultimo_nome = lista_nomes[-1]
    return ultimo_nome

# Goal: Extract the first name from a given row
#
# params:
#     row (pandas.Series) - Row containing user data
#
# returns: First name extracted from the row
def get_lastname(row):
    nomes = row['Nome']
    lista_nomes = nomes.split(' ')
    primeiro_nome = lista_nomes[0]
    ultimo_nome = lista_nomes[-1]
    return primeiro_nome

# Goal: Read and process an Excel file to create users
#
# params: None
#
# returns: String indicating the total number of users created
def handling_excel():
    dataframe_user_list = pandas.read_excel('lista.xlsx')
    counter = 0
    for index, row in dataframe_user_list.iterrows():
        firstname = get_first(row)
        lastname = get_lastname(row)
        email = row['E-mail']
        username = row['Login']

        token=get_token()
        
        new_user=int_create_user(firstname=firstname, lastname=lastname, email=email, username=username)
        counter += 1

    return f'total de usuarios criados: {counter}'


# if __name__ == "__main__":
    # tk = get_token()
    # # print(tk['access_token'])

    # # users = get_all_users(tk['access_token'])
    # # print(users)
    # user = create_user(tk['access_token'])
    # print(user)

    # print(handling_excel())