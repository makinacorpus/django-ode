from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ode',
        'USER': 'ode',
        'PASSWORD': 'ode',
        'HOST': 'localhost',
    }
}
