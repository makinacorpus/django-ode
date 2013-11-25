from base import *

DEBUG = False
TEMPLATE_DEBUG = False
STATIC_URL = "/"
STATIC_ROOT = "{{ pillar['apps']['ode_frontend']['static_root'] }}"
SECRET_KEY = "{{ pillar['apps']['ode_frontend']['secret_key'] }}"
MEDIA_ROOT = os.path.join(STATIC_ROOT, "media")

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ADMINS = (
    ('Romain Garrigues', 'romain.garrigues@makina-corpus.com'),
    ('Alex Marandon', 'alex.marandon@makina-corpus.com'),
)

ACCOUNTS_MODERATOR_EMAILS = [
    'romain.garrigues@makina-corpus.com',
    'alex.marandon@makina-corpus.com',
]

ALLOWED_HOSTS = ['preprod-ode.makina-corpus.net']
