from json import JSONDecodeError
from typing import Callable

import httpx
from rest_framework import status

from api.paystack.paystack_serializers import PaystackTransactionInitResponseSerializer, \
    PaystackTransactionStatusResponseSerializer
from restful_payment_gateway_api.settings import \
    (PAYSTACK_TEST_SECRET_KEY, PAYSTACK_API_BASE_URL)


def get_paystack_client(base_url: str, secret_key: str) -> httpx.Client:
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }
    return httpx.Client(base_url=base_url, headers=headers)


class PaystackClientException(Exception):
    def __init__(
            self,
            *args,
            data=None,
            status_code=status.HTTP_400_BAD_REQUEST):
        super().__init__(*args)
        self.data: dict | None = data
        self.status_code = status_code


class PaystackClient:
    """
    A lightweight client for interacting with the Paystack API.
    """

    def __init__(
            self,
            http_client_fun: Callable[[str, str], httpx.Client] = get_paystack_client,
            secret_key: str = PAYSTACK_TEST_SECRET_KEY,
            base_url: str = PAYSTACK_API_BASE_URL
    ):
        """
        Creates a new `PaystackClient` instance.
        Parameters:
            http_client_fun: A function that returns an `httpx.Client` instance that accepts a
                with provided secret key and base URL to make requests to the Paystack API.
                This can be swapped with a mock implementation for testing purposes.
            secret_key: The secret key used to authenticate requests to the Paystack API.
            base_url: The base URL used to make requests to the Paystack API.
        """
        self._http_client_fun = http_client_fun
        self._secret_key = secret_key
        self._base_url = base_url

    def _get_client(self) -> httpx.Client:
        return self._http_client_fun(self._base_url, self._secret_key)

    def init_payment(self, email: str, amount: float):
        with self._get_client() as client:
            data = {
                "email": email,
                "amount": int(amount * 100)
            }
            response = client.post("/transaction/initialize", json=data)
            if not response.is_success:
                try:
                    raise PaystackClientException(data=response.json())
                except JSONDecodeError as e:
                    # In case the error is one without a JSON response body (e.g. 5xx)
                    print(e)
                    raise PaystackClientException(
                        data={"status": False, "message": "Server error", "data": {}},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            data = response.json()
            serializer = PaystackTransactionInitResponseSerializer(data=data)
            if not serializer.is_valid():
                raise PaystackClientException(serializer.errors)

            return serializer.validated_data

    def get_payment_status(self, payment_id: str):
        with self._get_client() as client:
            response = client.get(f"/transaction/verify/{payment_id}")
            data = response.json()
            if not response.is_success:
                if data["code"] == "transaction_not_found":
                    raise PaystackClientException(
                        data={
                            "payment_id": payment_id,
                            "status": "failed",
                            "message": "Payment with the given payment id not found"
                        },
                        status_code=status.HTTP_404_NOT_FOUND)

                print(data)
                raise PaystackClientException(
                    data={"payment_id": payment_id, "status": "failed"})

            serializer = PaystackTransactionStatusResponseSerializer(data=data)
            if not serializer.is_valid():
                return PaystackClientException(data=serializer.errors)

            return serializer.validated_data
