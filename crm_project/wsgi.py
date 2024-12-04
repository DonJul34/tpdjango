import os
from django.core.wsgi import get_wsgi_application

# Set default settings module to dev or prod based on the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings.dev')  # or crm_project.settings.prod

application = get_wsgi_application()
