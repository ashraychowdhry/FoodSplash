# Easy run command to setup and run Django server
# use sudo
pip install -r requirements.txt #
python manage.py makemigrations #
#python manage.py makemigrations APP_NAME #
python manage.py migrate #
python manage.py runserver 0.0.0.0:80 #
