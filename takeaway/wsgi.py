
import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, "/var/www/takeaway/")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeaway.settings')
try:
	application = get_wsgi_application()
except Exception as e:
	print("**********************************",e)