from .base import *

DEBUG = True

ALLOWED_HOSTS = ['jumbo-ds.herokuapp.com', ]


import django_heroku

django_heroku.settings(locals())

