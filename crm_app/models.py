from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    nom = models.CharField(max_length=200)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    secteur_activite = models.CharField(max_length=100)
    preferred_language = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('fr', 'Français')],
        default='en'
    )

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('client_detail', args=[str(self.id)])


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contacts")
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    poste = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Opportunite(models.Model):
    STATUTS = [
        ('nouveau', 'Nouveau'),
        ('en_cours', 'En cours'),
        ('gagne', 'Gagné'),
        ('perdu', 'Perdu'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="opportunites")
    titre = models.CharField(max_length=200)
    description = models.TextField()
    montant_estime = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS)

    def __str__(self):
        return self.titre
    
    
class Interaction(models.Model):
    opportunite = models.ForeignKey(Opportunite, on_delete=models.CASCADE, related_name="interactions")
    date = models.DateField()
    compte_rendu = models.TextField()

    def __str__(self):
        return f"Interaction le {self.date}"
