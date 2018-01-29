import os


if os.environ.get('WEB_MODE', None) == 'production' :
   from .production import *
else :
   from .local import *