from django.contrib.auth.models import User

def create_user(firstname, lastname, email, username):
    user = User.objects.create_user(firstname=firstname, lastname=lastname, email=email, username=username)
    user.save
    return user