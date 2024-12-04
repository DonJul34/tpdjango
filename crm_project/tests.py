from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from crm_app.models import Client, Contact, Opportunite, Interaction
import logging
import colorlog

# Configure logger with colors
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
))

logger = logging.getLogger("tests")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
# Create a logger for the tests


if __name__ == "__main__":
    try:
        # Set up Django
        django.setup()

        # Run tests for the whole application
        logger.info("🔍 Running tests for the entire application...")
        call_command("test")  # Runs tests for all installed apps

        logger.info("🎉 All tests passed! Ready to push to GitHub.")
    except Exception as e:
        logger.error("❌ Some tests failed. Check the logs above for details.")
        logger.exception(e)
        sys.exit(1)

        
class ClientViewTests(TestCase):
    def setUp(self):
        logger.info("Setting up test data for ClientViewTests")
        self.client_instance = Client.objects.create(
            nom="Test Client",
            adresse="123 Test Street",
            telephone="123456789",
            email="test@example.com",
            secteur_activite="IT",
            preferred_language="en"
        )

    def test_client_create_view(self):
        logger.info("Testing client create view")
        response = self.client.post(reverse('client_create'), {
            'nom': 'New Client',
            'adresse': '456 New Avenue',
            'telephone': '987654321',
            'email': 'newclient@example.com',
            'secteur_activite': 'Finance',
            'preferred_language': 'en'  # Include the required field
        })
        logger.debug(f"Response status code: {response.status_code}")
        if response.status_code != 302:
            logger.error(f"Form errors: {response.context.get('form').errors if 'form' in response.context else 'No form context'}")
        self.assertEqual(response.status_code, 302)

    def test_client_update_view(self):
        logger.info("Testing client update view")
        response = self.client.post(reverse('client_update', args=[self.client_instance.id]), {
            'nom': 'Updated Client',
            'adresse': 'Updated Street',
            'telephone': '987654321',
            'email': 'updated@example.com',
            'secteur_activite': 'Updated IT',
            'preferred_language': 'fr'  # Include the required field
        })
        logger.debug(f"Response status code: {response.status_code}")
        if response.status_code != 302:
            logger.error(f"Form errors: {response.context.get('form').errors if 'form' in response.context else 'No form context'}")
        self.assertEqual(response.status_code, 302)


    def test_client_delete_view(self):
        logger.info("Testing client delete view")
        response = self.client.post(reverse('client_delete', args=[self.client_instance.id]))
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Client.objects.filter(id=self.client_instance.id).exists())


class APIClientTests(TestCase):
    def setUp(self):
        logger.info("Setting up test data for APIClientTests")
        self.api_client = APIClient()
        self.client_instance = Client.objects.create(
            nom="Test API Client",
            adresse="123 API Test Street",
            telephone="123456789",
            email="api_client@example.com",
            secteur_activite="IT"
        )

    def test_api_get_clients(self):
        logger.info("Testing API GET /clients/")
        response = self.api_client.get('/api/clients/')
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test API Client", str(response.data))

    def test_api_post_client(self):
        logger.info("Testing API POST /clients/")
        response = self.api_client.post('/api/clients/', {
            'nom': 'API New Client',
            'adresse': '789 API Street',
            'telephone': '987654321',
            'email': 'api_new_client@example.com',
            'secteur_activite': 'Finance'
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Client.objects.filter(email="api_new_client@example.com").exists())

    def test_api_put_client(self):
        logger.info("Testing API PUT /clients/{id}/")
        response = self.api_client.put(f'/api/clients/{self.client_instance.id}/', {
            'nom': 'Updated API Client',
            'adresse': 'Updated API Address',
            'telephone': '987654321',
            'email': 'updated_api_client@example.com',
            'secteur_activite': 'Updated IT'
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_instance.refresh_from_db()
        self.assertEqual(self.client_instance.nom, "Updated API Client")

    def test_api_delete_client(self):
        logger.info("Testing API DELETE /clients/{id}/")
        response = self.api_client.delete(f'/api/clients/{self.client_instance.id}/')
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client_instance.id).exists())


class ContactAPITests(TestCase):
    def setUp(self):
        logger.info("Setting up test data for ContactAPITests")
        self.api_client = APIClient()
        self.client_instance = Client.objects.create(
            nom="Test API Client",
            adresse="123 API Test Street",
            telephone="123456789",
            email="api_contact@example.com",
            secteur_activite="IT"
        )
        self.contact_instance = Contact.objects.create(
            client=self.client_instance,
            nom="Contact",
            prenom="Test",
            telephone="123456789",
            email="contact@example.com",
            poste="Manager"
        )

    def test_api_get_contacts(self):
        logger.info("Testing API GET /contacts/")
        response = self.api_client.get('/api/contacts/')
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test", str(response.data))

    def test_api_post_contact(self):
        logger.info("Testing API POST /contacts/")
        response = self.api_client.post('/api/contacts/', {
            'client': self.client_instance.id,
            'nom': 'New Contact',
            'prenom': 'API',
            'telephone': '987654321',
            'email': 'new_contact@example.com',
            'poste': 'Developer'
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Contact.objects.filter(email="new_contact@example.com").exists())
if __name__ == "__main__":
    try:
        unittest.main()
        logger.info("🎉 All tests passed! Ready to push to GitHub.")
    except Exception as e:
        logger.error("❌ Some tests failed. Check the logs above for details.")
