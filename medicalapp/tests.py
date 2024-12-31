from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class ChatbotTests(APITestCase):
    
    def test_chatbot_response(self):
        url = reverse('chatbot_response')  # Ensure the correct URL is used.
        data = {"user_message": "hello"}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bot_response', response.data)
