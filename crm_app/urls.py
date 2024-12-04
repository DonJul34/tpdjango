from django.urls import path
from django.conf.urls.i18n import set_language
from .views import (
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView,
    ClientDeleteView, ContactCreateView, SetLanguageView
)

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('new/', ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/<int:client_id>/new_contact/', ContactCreateView.as_view(), name='contact_create'),
    path('set_language/', SetLanguageView.as_view(), name='set_language'),
]
