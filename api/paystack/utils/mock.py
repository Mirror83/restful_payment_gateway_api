import json
from datetime import datetime

import httpx

from api.paystack.utils.sample_responses import init_payment_200_OK, verify_200_OK


def mock_paystack_handler(request: httpx.Request) -> httpx.Response:
    """Mock handler for Paystack API requests"""

    # Handle payment initialisation
    if request.method == "POST" and request.url.path == "/transaction/initialize":
        request_data = json.loads(request.content.decode())
        response_data = init_payment_200_OK
        response_data["data"]["reference"] = \
            f"mock-ref-{request_data.get('email', 'test').replace('@', '-at-')}-{request_data.get('amount', 3000)}"
        response_data["data"]["authorization_url"] = f"https://checkout.paystack.com/mock-reference-123"

        return httpx.Response(200, json=response_data)

    # Handle payment status verification
    if request.method == "GET" and request.url.path.startswith("/transaction/verify/"):
        payment_id = request.url.path.split("/")[-1]

        # Mock different responses based on payment_id
        if payment_id == "invalid-payment-id" or payment_id == "test-payment-id":
            response_data = {
                "status": False,
                "message": "Transaction reference not found",
                "code": "transaction_not_found"
            }
            return httpx.Response(404, json=response_data)

        elif "failed" in payment_id.lower():
            response_data = verify_200_OK
            response_data["data"]["status"] = "failed"
            response_data["data"]["paid_at"] = None

            return httpx.Response(200, json=response_data)

        else:
            # Mock successful or pending payment
            paid_at = None if "mock-ref" in payment_id else datetime.now().isoformat()
            response_data = verify_200_OK
            response_data["data"]["status"] = "success" if paid_at else "abandoned"
            response_data["data"]["reference"] = payment_id
            response_data["data"]["paid_at"] = paid_at
            response_data["data"]["created_at"] = datetime.now().isoformat()

            return httpx.Response(200, json=response_data)

    # Default response for unknown endpoints
    return httpx.Response(404, json={"status": False, "message": "Endpoint not found"})


def get_mock_paystack_client(base_url: str, secret_key: str):
    """Factory function that returns httpx client with mock transport"""
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }
    mock_transport = httpx.MockTransport(mock_paystack_handler)
    return httpx.Client(base_url=base_url, headers=headers, transport=mock_transport)