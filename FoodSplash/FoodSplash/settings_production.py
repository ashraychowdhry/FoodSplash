# Production Settings
# Google App Engine using Djangae


INSTALLED_APPS = [
    'djangae',
    'djangae.contrib.security',

    'django.contrib.admin',

    'django.contrib.auth',
    'djangae.contrib.gauth_datastore',

    'django.contrib.contenttypes',

    'djangae.contrib.contenttypes',

    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
]


MIDDLEWARE = [
    'djangae.contrib.security.middleware.AppEngineSecurityMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'djangae.contrib.gauth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

AUTH_USER_MODEL = 'gauth_datastore.GaeDatastoreUser'

AUTHENTICATION_BACKENDS = (
    'djangae.contrib.gauth_datastore.backends.AppEngineUserAPIBackend',
    'django.contrib.auth.backends.ModelBackend',
)


DATABASES = {
    'default': {
        'ENGINE': 'djangae.db.backends.appengine'
    }
}



# Load production keys from datastore
# Keeps the production keys private if source code is made public

from google.appengine.ext import ndb


class ApplicationSettings(ndb.Model):
    name = ndb.StringProperty(required=True)
    value = ndb.StringProperty(required=True)


SECRET_KEY = ApplicationSettings.query(ApplicationSettings.name == 'SECRET_KEY').get()
