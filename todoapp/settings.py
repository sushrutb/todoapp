# Django settings for todoapp project.
import os
import dj_database_url
#import social_auth

DEBUG = True
TEMPLATE_DEBUG = DEBUG
try:
    from local_settings import *
except ImportError:
    if os.environ.get('MACHINE') == 'staging':
        from staging_settings import *
    else:
        from production_settings import *

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
DATABASES = {'default': dj_database_url.config(default='mysql://root:sushrut123@localhost:3306/todoapp')}
MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
                    os.path.join(SITE_ROOT, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')k6aw+wtdr_m^b+jw@195*#xcjnv0hy1=!13)8vf#*s&amp;@cg%t2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'todoapp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'todoapp.wsgi.application'

SITE_ID = 1

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'todo',
    'project',
    'social_auth',
    'registration',
    'django.contrib.sites',
    'storages',
    'django_forms_bootstrap',
    'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

TEMPLATE_CONTEXT_PROCESSORS = (
    #'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
)


TWITTER_CONSUMER_KEY = 'L3JjG962LiuzxHkoQRilA'
TWITTER_CONSUMER_SECRET = 'luqlhUfERJMBnRP7rQjDfUrf6rNjBYki5gwykSVFU'
FACEBOOK_APP_ID = '253040264810160'
FACEBOOK_API_SECRET = 'a46357a0cf79fc17d3a74d15947a29f1'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sb@simplycious.com'
EMAIL_HOST_PASSWORD = 'sushnups'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'no-reply@simplycious.com'
ACCOUNT_ACTIVATION_DAYS = 7

AWS_ACCESS_KEY_ID = 'AKIAJOTC7XECHF2LD2NQ'
AWS_SECRET_ACCESS_KEY = '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'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
AWS_QUERYSTRING_AUTH = False
AWS_GZIP = True
#AWS_IS_GZIPPED = True


try:
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("UPDATE django_site set domain=\'" + SITE_DOMAIN + "\', name=\'" + SITE_DOMAIN_NAME + "\'")
    transaction.commit_unless_managed()
except Exception, e:
    pass

system_tags = {
                "#expenses": ('reported', 'reimbursed'), 
                "#buy":('bought',), 
                "#bookmark":None,
                "#readlater":('done',),
                "#wishlist":('bought',),
                "#readlater":('done',),
                "#todo":('completed',),
#                "#invoice": ('sent','received'),
#                "diary":None,
                }
page_length = 5