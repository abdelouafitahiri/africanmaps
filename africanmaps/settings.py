import os
from pathlib import Path
import environ


BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))  # Point to the .env file

# Load secret key from .env file
SECRET_KEY = env('SECRET_KEY')

# Load debug mode from .env file
DEBUG = env.bool('DEBUG', default=False)

# Load allowed hosts from .env file
ALLOWED_HOSTS = ['*']

CSRFCSRF_TRUSTED_ORIGINS = ['https://africanmaps-7yxuy.ondigitalocean.app']

# Installed apps and middleware configuration remain the same
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authenticate.apps.AuthenticateConfig',
    'dashboard_app',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'africanmaps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "authenticate/templates",
            BASE_DIR / "dashboard_app/templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard_app.context_processors.user_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'africanmaps.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation remains the same
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

# Internationalization remains the same
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# DigitalOcean Spaces Configuration
AWS_ACCESS_KEY_ID = env('DO_SPACES_KEY')
AWS_SECRET_ACCESS_KEY = env('DO_SPACES_SECRET')
AWS_STORAGE_BUCKET_NAME = 'africanmaps'

AWS_S3_ENDPOINT_URL = 'https://africanmaps.lon1.digitaloceanspaces.com'
AWS_S3_CUSTOM_DOMAIN = 'africanmaps.lon1.cdn.digitaloceanspaces.com'

AWS_LOCATION = 'media'
AWS_DEFAULT_ACL = 'public-read'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
AWS_DEFAULT_ACL = 'public-read'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Maximum file upload size
FILE_UPLOAD_MAX_MEMORY_SIZE = 41943040  # 40 MB

# Default primary key field type remains the same
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration using environment variables
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

LOGIN_REDIRECT_URL = '/dashboard/'