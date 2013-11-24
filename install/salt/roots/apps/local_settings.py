from base import *

DEBUG = False
TEMPLATE_DEBUG = False
STATIC_URL = "/"
STATIC_ROOT = "{{ pillar['apps']['ode_frontend']['static_root'] }}"
SECRET_KEY = "{{ pillar['apps']['ode_frontend']['secret_key'] }}"

# Enable cache busting
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ode_frontend',
        'USER': 'ode_frontend',
        'PASSWORD': "{{ pillar['apps']['ode_frontend']['dbpassword'] }}",
        'HOST': 'localhost',
    }
}
