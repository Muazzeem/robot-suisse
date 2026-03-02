from .base import *

DEBUG = True
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://fifadesk.com",
    "https://www.fifadesk.com",
]

try:
    from .local import *
except ImportError:
    pass
