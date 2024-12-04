from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crm_app.views import ClientViewSet, ContactViewSet, OpportuniteViewSet, InteractionViewSet


router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'opportunites', OpportuniteViewSet)
router.register(r'interactions', InteractionViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('crm_app.urls')),
    path('api/', include(router.urls)),
    path('textgen/', include('textgen.urls')),  # Ajoute cette ligne
]