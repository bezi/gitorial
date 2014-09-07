"""
Django settings for gitorial project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# TODO handle errors here
try:
  SOCIAL_AUTH_GITHUB_KEY = os.environ['SOCIAL_AUTH_GITHUB_KEY']
  SOCIAL_AUTH_GITHUB_SECRET = os.environ['SOCIAL_AUTH_GITHUB_SECRET']
except:
  pass


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6=o8h-+6vt*7bwhn!wvj@+nan&p*hduv4*a)0-rt2%e09jgma_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['.gitorial.com', 'localhost', 'gitorial.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # OAuth library
    'social.apps.django_app.default',

    # gitorial app
    'gitorial',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {}

if not DEBUG:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ----- Static files (CSS, JavaScript, Images) --------------------------------
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# where collectstatic will collect files
STATIC_ROOT = 'assets'

# URL at which files collected to STATIC_ROOT can be access
STATIC_URL = '/assets/'

# Extra directories to check for staticfiles
STATICFILES_DIR = (os.path.join(BASE_DIR, 'assets'))
# -----------------------------------------------------------------------------

# Use GitHub for logging in users
AUTHENTICATION_BACKENDS = (
  'social.backends.github.GithubOAuth2',
  'django.contrib.auth.backends.ModelBackend',
)

# Use social template context processors
TEMPLATE_CONTEXT_PROCESSORS = (
  # Default setting for TEMPLATE_CONTEXT_PROCESSORS
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  'django.core.context_processors.tz',
  'django.contrib.messages.context_processors.messages',

  # Add social data to the template context
  'social.apps.django_app.context_processors.backends',
  'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username']
LOGIN_REDIRECT_URL = '/'
