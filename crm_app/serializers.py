from rest_framework import serializers
from .models import Client, Contact, Opportunite, Interaction

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class OpportuniteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunite
        fields = '__all__'

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'
