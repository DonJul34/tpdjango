from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Client
from django.contrib import messages
from rest_framework.viewsets import ModelViewSet
from .models import Client, Contact, Opportunite, Interaction
from .serializers import ClientSerializer, ContactSerializer, OpportuniteSerializer, InteractionSerializer
from .forms import ContactForm
from django.http import JsonResponse
from django.utils.translation import activate, get_language
from django.views import View

class ClientListView(ListView):
    model = Client
    template_name = "crm_app/client_list.html"

class ClientDetailView(DetailView):
    model = Client
    template_name = "crm_app/client_detail.html"

class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'  # Adjust fields as needed
    template_name = "crm_app/client_form.html"
    success_url = reverse_lazy('client_list')

    def form_valid(self, form):
        messages.success(self.request, "Le client a été créé avec succès.")
        return super().form_valid(form)


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "crm_app/contact_form.html"
    success_url = reverse_lazy('client_list')

    def form_valid(self, form):
        # Assign a client to the contact
        client = Client.objects.get(pk=self.kwargs['client_id'])
        form.instance.client = client  # Set the client for the contact
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'
    template_name = "crm_app/client_form.html"

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client_list')
    template_name = "crm_app/client_confirm_delete.html"


class SetLanguageView(View):
    def post(self, request, *args, **kwargs):
        language = request.POST.get('language')
        if language not in ['en', 'fr','es']:
            return JsonResponse({'error': 'Invalid language'}, status=400)

        activate(language)  # Set the active language
        request.session['django_language'] = language  # Save it to the session
        request.session.save()  # Ensure the session persists
        return JsonResponse({'message': 'Language updated successfully', 'language': language})
        
class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class OpportuniteViewSet(ModelViewSet):
    queryset = Opportunite.objects.all()
    serializer_class = OpportuniteSerializer

class InteractionViewSet(ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer