from .base import *

DEBUG = True
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = ["breakdownrecoveryservice.marketize.biz"]

CSRF_TRUSTED_ORIGINS = [
    "https://breakdownrecoveryservice.marketize.biz",
]
BACKEND_HOST = "https://breakdownrecoveryservice.marketize.biz"

try:
    from .local import *
except ImportError:
    pass
