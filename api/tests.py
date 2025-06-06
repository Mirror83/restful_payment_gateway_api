from django.test import Client, SimpleTestCase

from django.urls import reverse
from rest_framework import status
import json

init_payment_url = reverse("api:initialize_payment")
payment_status_url = reverse("api:get_payment_status", kwargs={"payment_id": "test-payment-123"})


class InitPaymentViewTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_data(self):
        """Test initialize_payment with valid data"""
        valid_data = {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "amount": 50.00
        }
        response = self.client.post(
            init_payment_url,
            data=json.dumps(valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('amount', response_data)

    def test_empty_data(self):
        """Test initialize_payment with empty data"""
        response = self.client.post(
            init_payment_url,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data(self):
        """Test initialize_payment with invalid data"""
        invalid_data = {
            "amount": "invalid_amount"
        }
        response = self.client.post(
            init_payment_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_method(self):
        """Test initialize_payment with GET method (should fail)"""
        response = self.client.get(init_payment_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetPaymentStatusViewTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_id(self):
        """Test get_payment_status with valid payment ID"""
        payment_id = "m392r2dbbn"
        response = self.client.get(payment_status_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['payment_id'], payment_id)
        self.assertEqual(response_data['status'], 'success')

    def test_post_method(self):
        """Test get_payment_status with POST method (should fail)"""
        response = self.client.post(payment_status_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
