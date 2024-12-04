from django.contrib import admin
from .models import Client, Contact, Opportunite, Interaction

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'secteur_activite')
    search_fields = ('nom', 'secteur_activite')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'client', 'poste')
    search_fields = ('nom', 'prenom', 'client__nom')

@admin.register(Opportunite)
class OpportuniteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'client', 'statut', 'montant_estime')
    list_filter = ('statut',)
    actions = ['marquer_comme_gagne']

    @admin.action(description="Marquer les opportunités sélectionnées comme gagnées")
    def marquer_comme_gagne(self, request, queryset):
        queryset.update(statut='gagne')

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('date', 'opportunite')
