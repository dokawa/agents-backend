# Debug Toolbar
from .settings import *  # noqa

INSTALLED_APPS.remove("debug_toolbar")
MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")
DEBUG_TOOLBAR_CONFIG = {}
