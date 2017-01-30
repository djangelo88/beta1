"""
Django settings for caterfull project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
# import sys



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.urlresolvers import reverse


# import sys
# sys.path.insert(0, '/home/amado/widget-tweaks/django-widget-tweaks-1.3/widget_tweaks')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sys.path.insert(0, os.path.join(BASE_DIR,'dependencies/django_wkhtmltopdf-3.1.0-py3.4.egg'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kis9so8w%ag3(qk$-&1wx2ys(wtl7hop(mmc)hkrd1p!9&*as3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'stripe_cater',
    'base.apps.BaseConfig',
    # 'base.apps.BaseConfig',
    #'wkhtmltopdf'
    'business_site',
    'beta',
    # 'sqlserver'
    #'easy_pdf',
    # 'xhtml2pdf',
    #'reportlab',
    #'html5lib',
    'django_excel',
    'corsheaders',


]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'caterfull.middelware.SubdomainURLRoutingMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'caterfull.urls'
DEFAULT_SITE_DOMAIN = 'app.caterfull.com'
# DEFAULT_SITE_DOMAIN = 'localhost'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'base.context_processors.subscription_status',
                'base.context_processors.business_data',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'caterfull.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

    # 'default': {
    #     'ENGINE': 'sqlserver_ado',
    #     'NAME': 'caterfull',
    #     'HOST': '192.168.202.1\\ss2012',
    #     'USER': 'sa',
    #     'PASSWORD': 'caterfull',
    # }

}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT =  os.path.join(BASE_DIR,'D:/Desarrollo/caterfull/base/static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
#MEDIA_ROOT = os.path.join(BASE_DIR,'D:/Desarrollo/caterfull/base/media')


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOGIN_REDIRECT_URL = '/'
# LOGIN_REDIRECT_URL = '/beta/home'

# ADMIN_EMAIL="amado@caterfull.com"
EMAIL_HOST = "192.168.0.98"
# EMAIL_USE_TLS = True
ADMIN_EMAIL = "amado@caterfull.com"
EMAIL_HOST_USER = "amado@caterfull.com"
EMAIL_HOST_PASSWORD = "amado"

#GROUPS' NAMES
BUSINESS_BASIC = 'Business_Basic'
BUSINESS_MEMBER = 'Business_Member'
BUSINESS_TRIAL = 'Business_Trial'
BUSINESS_GROUPS = [BUSINESS_BASIC, BUSINESS_MEMBER, BUSINESS_TRIAL]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CATERFULL_BASE_URL = 'localhost:8000'
# CATERFULL_BASE_URL = 'localhost'

DAYS_TO_CONFIRM_EMAIL = 5
DAYS_TO_NOTIFY_EXPIRE_DATE = 7

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'base.backends.CaterBackend']
APPEND_SLASH=True

STRIPE_API_KEY = "sk_test_VqXkPGUwoq2vgyHMVWFcIP3Q"
STRIPE_CLIENTE_ID = "ca_9ifH4knT4raQw67FMfANBJr1W46n24om"
STRIPE_PUBLISHABLE_KEY = "pk_test_EoZD1BMOPtF96Jx6aYJmnmaZ"
STRIPE_PLAN_ID = "2"
STRIPE_URL_REDIRECT = {"webhooks": CATERFULL_BASE_URL + '/stripe/webhooks/',
                       'building_account': CATERFULL_BASE_URL + '/business/stripe/callback/'}
STRIPE_URL_WH_NAME = "webhooks"
STRIPE_URL_WH_NAME = 'building_account'
STRIPE_MAX_PAYMENT_ATTEMPTS = 3
STRIPE_DEFAULT_CURRENCY = 'usd'

STRIPE_OAUTH_SITE = 'https://connect.stripe.com/oauth/'
STRIPE_AUTHORIZE_URI = 'authorize'
STRIPE_TOKEN_URI = 'token'
STRIPE_TRIAL_DAYS = 30
CHECK_SUBSCRIPTION_STATUS_ON_LOGIN = False

# WKHTMLTOPDF_CMD = "C:/Python34/Lib/site-packages/wkhtmltopdf"
# WKHTMLTOPDF_CMD = os.path.join(BASE_DIR, 'dependencies/django_wkhtmltopdf-3.1.0-py3.4.egg/wkhtmltopdf')

PROFILE_DIR_NAME = 'profile'
PROFILE_DIR = MEDIA_ROOT + '/' + PROFILE_DIR_NAME

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
"django_excel.TemporaryExcelFileUploadHandler")

CORS_ORIGIN_ALLOW_ALL = True