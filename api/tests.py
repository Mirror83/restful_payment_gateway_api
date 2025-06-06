from django.test import Client, SimpleTestCase

from django.urls import reverse
from rest_framework import status
import json

init_payment_url = reverse("api:initialize_payment")
payment_status_url_view_name = "api:get_payment_status"


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
        self.assertTrue(response_data['status'])

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
        """Test initialize_payment with the GET method (should fail)"""
        response = self.client.get(init_payment_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetPaymentStatusViewTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.valid_payment_id = "m392r2dbbn"
        self.invalid_payment_id = "test-payment-id"

    def test_valid_id(self):
        """Test get_payment_status with valid payment ID"""
        url = reverse(payment_status_url_view_name, kwargs={"payment_id": self.valid_payment_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["data"]["reference"], self.valid_payment_id)
        self.assertEqual(response_data["status"], True)

    def test_post_method(self):
        """Test get_payment_status with the POST method (should fail)"""
        url = reverse(payment_status_url_view_name, kwargs={"payment_id": "m392r2dbbn"})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
