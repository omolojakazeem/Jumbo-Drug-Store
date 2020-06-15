from .base import *

DEBUG = False

ALLOWED_HOSTS = ['jumbo-ds.herokuapp.com', ]


import django_heroku

django_heroku.settings(locals())

