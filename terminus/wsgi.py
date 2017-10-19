"""
WSGI config for terminus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys
import site
#site.addsitedir('/home/salvor/pyenv/lib/python2.7')
from django.core.wsgi import get_wsgi_application
# Add the site-packages of the chosen virtualenv to work with
# site.addsitedir('/var/run/pyenv/lib/python2.7')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/run/mt01')
sys.path.append('/var/run/mt01/terminus')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "terminus.settings")
#activate_env = os.path.expanduser("/var/run/pyenv/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))
application = get_wsgi_application()
