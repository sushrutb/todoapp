'''
Created on Aug 7, 2012

@author: sushrut
'''
DEBUG = False
SITE_ROOT = '/app/'
TEMPLATE_DIRS = (
                 '/app/templates/',
)


SITE_DOMAIN_NAME = 'simplycious.com'
SITE_DOMAIN = 'simplycious.com'

STATIC_URL = 'http://s3.amazonaws.com/prod.todoapp.sushrutbidwai.com/'
AWS_STORAGE_BUCKET_NAME = 'prod.todoapp.sushrutbidwai.com'

STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
AWS_HEADERS = {
'Expires': 'Wed, 22 Aug 2012 20:00:00 GMT',
'Cache-Control': 'max-age=86400',
}
AWS_S3_SECURE_URLS = False
GZIP_CONTENT_TYPES =  (
    'text/css',
    'application/javascript',
    'application/x-javascript',
)
