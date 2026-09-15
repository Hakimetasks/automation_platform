from django.test import TestCase, Client
from django.urls import reverse
from .models import User, ReferenceCheck
import json

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.phone_number = "+251911223344"
        self.request_login_url = reverse('request_login')
        self.verify_login_url = reverse('verify_login')

    def test_request_login_creates_user_and_reference(self):
        response = self.client.post(
            self.request_login_url,
            data=json.dumps({'phone_number': self.phone_number}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_verify_login_successful(self):
        user = User.objects.create_user(phone_number=self.phone_number)
        ReferenceCheck.objects.create(user=user, reference_number="REF-123456")
        response = self.client.post(
            self.verify_login_url,
            data=json.dumps({
                'phone_number': self.phone_number,
                'reference_number': 'REF-123456'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
