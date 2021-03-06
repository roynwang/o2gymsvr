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
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIRS = (
		os.path.join(BASE_DIR, 'templates'),
		)


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
		'traincategory',
		'recommend',
		'usr',
		'weibo',
		'order',
		'business',
		'sms',
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
			'DIRS': TEMPLATE_DIRS,
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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Chongqing'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
		#'PAGINATE_BY': 2,
		#'PAGINATE_BY_PARAM': 'page_size',
		'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
		'PAGE_SIZE': 12,
		#'MAX_PAGINATE_BY': 100 ,

		'DEFAULT_PERMISSION_CLASSES': (
			'rest_framework.permissions.AllowAny',
			#'rest_framework.permissions.IsAuthenticated',
			#'rest_framework.permissions.IsAuthenticatedOrReadOnly',
			),
		'DEFAULT_AUTHENTICATION_CLASSES': (
			'rest_framework.authentication.SessionAuthentication',
			'rest_framework.authentication.BasicAuthentication',
			'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
			),
		}
JWT_AUTH = {
		#'JWT_VERIFY_EXPIRATION': False,
		'JWT_ALLOW_REFRESH': True,
		'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
		'JWT_EXPIRATION_DELTA':datetime.timedelta(days=30),
		}
QNACCESSKEY = '6skaNTW7Ja8B6tYX-3j9j588_jdRmgNWZV2NYJ0H'
QNSECRETKEY = 'QLtvaMzRthYDOcPHBYvax5hda2uu7oh4BpKjiMHk'
QNBUKET = 'gymgo'

UCPAASHOST = "https://api.ucpaas.com"
UCPAASPORT = ""
UCPAASSOFTVER = "2014-06-30"
UCPAASJSON = "json"
UCPAASXML = "xml"
UCPAASSID = "f52a037bfe68d879caa7aa88681b32ca"
UCPAASTOKEN = "6115f06113d62abe266fccc9af07cf22"
UCPAASAPPID = "6645449487fa4105bdfa2487ba88d2cf"
UCPAASTEMPLATE = 13286

DEFAULT_AVATAR = "http://7xiwfp.com1.z0.glb.clouddn.com/default_avatar.png"

GAODE_KEY = "a2be60fd9e30425d8e7c003ba81a1f12"
GAODE_TABLEID = "560353bae4b0fe6c79f8f0d0"
GAODE_URL = "http://yuntuapi.amap.com/datasearch/around"

