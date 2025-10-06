from .base import *

DEBUG = True

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
BACKEND_HOST = "https://breakdownrecoveryservice.marketize.biz"
try:
    from .local import *
except ImportError:
    pass
