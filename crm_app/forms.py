from django import forms
from .models import Contact, Opportunite

class OpportuniteForm(forms.ModelForm):
    class Meta:
        model = Opportunite
        fields = '__all__'
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['client']  # Exclude client, as it will be set in the view

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("L'email est obligatoire.")
        return email
