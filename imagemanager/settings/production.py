from .base import *
import dj_database_url

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

#Configure this in prod!
ALLOWED_HOSTS += ['imagemanager-api.herokuapp.com']

