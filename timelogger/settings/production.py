"""
Django settings for timelogger project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# stuff needed to compute holidays
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, \
    USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay, Easter, \
    USLaborDay, USThanksgivingDay,Day
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from pandas import DateOffset
import pandas as pd
import datetime as dt

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ADMINS = [('John', os.environ.get('ADMIN_EMAIL', None))]

MANAGERS = ADMINS
SEND_BROKEN_LINK_EMAILS=True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ALLOWED_HOSTS = ['*']

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 31557600 # expire in a year

EMAIL_HOST = os.environ.get('EMAIL_HOST',None)
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', None)
EMAIL_USE_TLS = True
EMAIL_NO_REPLY = True
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER', None)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'timelog',
    'work_type',
    'reasons',
    'crispy_forms',
    'datetimewidget',
    'facilities',
    'related_admin',
    'import_export',
    'rangefilter',
    'constance',
    'constance.backends.database',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'timelogger.urls'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

WSGI_APPLICATION = 'timelogger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':os.environ.get('APP_DB', None),
        'USER':os.environ.get('APP_DB_USER', None),
        'PASSWORD':os.environ.get('APP_DB_PWD', None),
        'PORT': os.environ.get('APP_DB_PORT', None),
    'OPTIONS': {
         "init_command": "SET foreign_key_checks = 0;",
    },
    }
}

# In the flexible environment, you connect to CloudSQL using a unix socket.
# Locally, you can use the CloudSQL proxy to proxy a localhost connection
# to the instance
# cloud_sql_proxy -instances=sps-productivity:us-central1:sps-productivity=tcp:3306 -credential_file=/Users/jnorton/Dropbox/Projects/sps-productivity/CloudDB_SSL/SPS\ Productivity-3bc097bf5ad5.json
#DATABASES['default']['HOST'] = '/cloudsql/sps-productivity:us-central1:sps-productivity'
#if os.getenv('GAE_INSTANCE'):
#    pass
#else:
#    DATABASES['default']['HOST'] = '127.0.0.1'
# [END dbconfig]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Certs
CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

#STATIC_URL = 'https://storage.googleapis.com/staging.sps-productivity.appspot.com/static/'
#STATIC_ROOT = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_SUPERUSER_ONLY =  False

CONSTANCE_CONFIG = {
    'DAY_RATE': (3400.00, 'Radiologist Day Rate',float),
    'QGENDA_EMAIL': ('','Email for Qgenda Account Login', str),
    'QGENDA_PASSWORD': ('','Password for Qgenda Account', str),
    'QGENDA_COMPANY_KEY':('c7649103-dab1-4787-81aa-78873b77733a','Qgenda Company Key', str),
    'QGENDA_LOGIN_ENDPOINT':('https://api.qgenda.com/v2/login','URL for Qgenda API Login', str),
    'QGENDA_GET_ENDPOINT':('https://api.qgenda.com/v2/schedule','URL for Qgenda Schedule API', str),
    'ADMIN_CONTACT_EMAIL':('','Email for sending application errors', str),
}

#Holiday Rules
class SPS_Holiday_Calendar(AbstractHolidayCalendar):
    rules = [\
                Holiday('New Years Day', month=1, day=1, observance=nearest_workday),\
                USMartinLutherKingJr,\
                USPresidentsDay,\
                Holiday("Easter Monday", month=1, day=1,offset=[Easter(), Day(1)]),\
                USMemorialDay,\
                Holiday('US Independence Day', month=7, day=4, observance=nearest_workday),\
                Holiday('Utah Pioneer Day', month=7, day=24, observance=nearest_workday),\
                USLaborDay,\
                USThanksgivingDay,\
                Holiday('Black Friday', month=11, day=1, offset=pd.DateOffset(weekday=FR(4))),\
                Holiday('Christmas Eve', month=12, day=24),\
                Holiday('Christmas', month=12, day=25)\
    ]
# Calculate this year and last year's holidays
SPS_HOLIDAYS = list(SPS_Holiday_Calendar().holidays(dt.datetime(dt.date.today().year-2, 12, 31), dt.datetime(dt.date.today().year, 12, 31)))
