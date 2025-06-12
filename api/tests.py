from django.test import Client, SimpleTestCase
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
import json

from api.paystack.utils.mock import mock_paystack_client_factory

init_payment_url = reverse("api:initialize_payment")
payment_status_url_view_name = "api:get_payment_status"


class InitPaymentViewTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.valid_data = {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "amount": 30.00
        }
        self.invalid_data = {
            "amount": "invalid_amount"
        }

    @patch('api.views.paystack_client._http_client_fun', side_effect=mock_paystack_client_factory)
    def test_valid_data(self, _mock_http_client_fun):
        """Test initialize_payment with valid data"""
        response = self.client.post(
            init_payment_url,
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        print(response_data)
        self.assertTrue(response_data['status'])
        self.assertIn('data', response_data)
        self.assertIn('authorization_url', response_data['data'])
        self.assertIn('reference', response_data['data'])

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
        response = self.client.post(
            init_payment_url,
            data=json.dumps(self.invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('api.views.paystack_client._http_client_fun', side_effect=mock_paystack_client_factory)
    def test_initialized_but_incomplete_payment(self, _mock_http_client_fun):
        init_payment_response = self.client.post(
            init_payment_url,
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(init_payment_response.status_code, status.HTTP_200_OK)
        response_data = init_payment_response.json()
        self.assertTrue(response_data["status"])
        reference = response_data["data"]["reference"]

        get_status_url = reverse(payment_status_url_view_name, kwargs={"payment_id": reference})
        get_status_response = self.client.get(get_status_url)
        response_data = get_status_response.json()
        self.assertTrue(response_data['status'])
        self.assertIsNone(response_data["data"]["paid_at"])

    def test_get_method(self):
        """Test initialize_payment with the GET method (should fail)"""
        response = self.client.get(init_payment_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetPaymentStatusViewTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        # Using mock payment IDs instead of real ones
        self.valid_payment_id = "mock-valid-payment-123"
        self.failed_payment_id = "mock-failed-payment-456"
        self.invalid_payment_id = "test-payment-id"

    @patch('api.views.paystack_client._http_client_fun', side_effect=mock_paystack_client_factory)
    def test_valid_id(self, _mock_http_client_fun):
        """Test get_payment_status with valid payment ID"""
        url = reverse(payment_status_url_view_name, kwargs={"payment_id": self.valid_payment_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["data"]["reference"], self.valid_payment_id)
        self.assertEqual(response_data["status"], True)

    @patch('api.views.paystack_client._http_client_fun', side_effect=mock_paystack_client_factory)
    def test_invalid_id(self, _mock_http_client_fun):
        """Test get_payment_status with invalid payment ID"""
        url = reverse(payment_status_url_view_name, kwargs={"payment_id": self.invalid_payment_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('api.views.paystack_client._http_client_fun', side_effect=mock_paystack_client_factory)
    def test_failed_payment(self, _mock_http_client_fun):
        get_status_url = reverse(payment_status_url_view_name, kwargs={"payment_id": self.failed_payment_id})
        get_status_response = self.client.get(get_status_url)
        response_data = get_status_response.json()
        self.assertTrue(response_data["status"])
        self.assertEqual(response_data["data"]["status"], "failed")

    def test_post_method(self):
        """Test get_payment_status with the POST method (should fail)"""
        url = reverse(payment_status_url_view_name, kwargs={"payment_id": "mock-payment-123"})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)