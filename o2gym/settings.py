"""
Django settings for o2gym project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z1x7$-+ji55#m)z0o*-*a&j4jlw7_augg2%%5n)*ft^wk5#(-l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'rest_framework',
		'recommend',
		'usr',
		'weibo',
		'business',
		)


MIDDLEWARE_CLASSES = (
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
		'django.middleware.security.SecurityMiddleware',
		)

ROOT_URLCONF = 'o2gym.urls'

TEMPLATES = [
		{
			'BACKEND': 'django.template.backends.django.DjangoTemplates',
			'DIRS': [],
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

WSGI_APPLICATION = 'o2gym.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
'''
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}
'''
DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'o2gym',
			'USER': 'root',
			'PASSWORD': '435393055',
			'HOST': '127.0.0.1',
			'PORT': '3306',
			'OPTIONS': {
				'sql_mode': 'TRADITIONAL',
				'charset': 'utf8',
				'init_command': 'SET '
				'storage_engine=INNODB,'
				'character_set_connection=utf8,'
				'collation_connection=utf8_bin'
				}
			}
		}



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
		'PAGINATE_BY': 2,
		'PAGINATE_BY_PARAM': 'page_size',
	    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
	    'PAGE_SIZE': 10,
		'MAX_PAGINATE_BY': 100 
		}
QNACCESSKEY = '6skaNTW7Ja8B6tYX-3j9j588_jdRmgNWZV2NYJ0H'
QNSECRETKEY = 'QLtvaMzRthYDOcPHBYvax5hda2uu7oh4BpKjiMHk'
QNBUKET = 'gymgo'
