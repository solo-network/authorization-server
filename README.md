# authorization-server
OAuth Server

# running
docker-compose up -d
pip install -r requirements.txt
export Djangoenv=True
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser