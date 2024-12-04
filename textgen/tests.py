from rest_framework.test import APIClient, APITestCase

class APITest(APITestCase):
    def test_api_endpoint(self):
        client = APIClient()
        response = client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
