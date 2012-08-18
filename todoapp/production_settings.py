'''
Created on Aug 7, 2012

@author: sushrut
'''
DEBUG = False
SITE_ROOT = '/app/'
TEMPLATE_DIRS = (
                 '/app/templates/',
)


SITE_DOMAIN_NAME = 'todoapp.sushrutbidwai.com'
SITE_DOMAIN = 'todoapp.sushrutbidwai.com'

STATIC_URL = 'https://s3.amazonaws.com/prod.todoapp.sushrutbidwai.com/'
AWS_STORAGE_BUCKET_NAME = 'prod.todoapp.sushrutbidwai.com'

STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME + 'docs/assets/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
