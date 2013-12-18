# -*- encoding: utf-8 -*-
"""
Django settings for django_ode project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6aq+(bcqqgsy+*g4$15idh5+5^5-k8=h0%g0c4e0^3j()@-w&n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'django_extensions',
    'pipeline',
    'frontend',
    'accounts',
    'easy_thumbnails',
    'rest_framework.authtoken',
    'tagging',
    'mptt',
    'zinnia',
    'ckeditor',
)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'django_ode.urls'

WSGI_APPLICATION = 'django_ode.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGES = (
    ('fr', u'Français'),
)

LANGUAGE_CODE = 'fr'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.i18n",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "zinnia.context_processors.version",
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

SITE_ID = 1

ALLOWED_HOSTS = ['*']  # FIXME

AUTH_USER_MODEL = 'accounts.User'
DEFAULT_FROM_EMAIL = 'ode@example.com'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/django.log',
            'maxBytes': 100000,
            'backupCount': 5,
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
        },
    },
}

# Third-party apps settings
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)
PIPELINE_CSS = {
    'style': {
        'source_filenames': (
            'css/bootstrap.css',
            'css/style.less',
            'css/ode.datatable.less',
            'css/daterangepicker-bs3.css'
        ),
        'output_filename': 'css/style.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}


PIPELINE_JS = {
    'scripts': {
        'source_filenames': (
            'js/jquery.js',
            'js/bootstrap.js',
            'js/moment.js',
            'js/langs.js',
            'js/daterangepicker.js',
            'js/csrf.js',
            'js/jquery.dataTables.js',
            'js/ode.dataTables.js',
            'js/ode.signup.js',
            'js/ode.events.js'
        ),
        'output_filename': 'js/scripts.js',
    }
}

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

CKEDITOR_UPLOAD_PATH = "flatpages/"
CKEDITOR_IMAGE_BACKEND = 'pillow'

# Project-specific settings
EVENT_API_BASE_URL = 'http://localhost:6543'
SOURCES_ENDPOINT = EVENT_API_BASE_URL + '/v1/sources'
EVENTS_ENDPOINT = EVENT_API_BASE_URL + '/v1/events'
ACCOUNTS_MODERATOR_EMAILS = ['moderator@example.com']
