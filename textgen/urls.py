from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('generate/', views.generate_text, name='generate_text'),
    path('generate_html/', views.generate_poetry, name='generate_poetry'),
    path('my_poems/', views.view_poems, name='view_poems'),  # New URL to view poems
]

# settings.py
# crm_app/urls.py
# crm_project/urls.py

# settings.py
# settings.py
# crm_app/views.py
# crm_project/urls.py

# settings.py

# Exemple dans views.py
