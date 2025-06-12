import json
from datetime import datetime

import httpx


def mock_paystack_handler(request: httpx.Request) -> httpx.Response:
    """Mock handler for Paystack API requests"""

    # Handle payment initialisation
    if request.method == "POST" and request.url.path == "/transaction/initialize":
        request_data = json.loads(request.content.decode())
        response_data = {
            "status": True,
            "message": "Authorization URL created",
            "data": {
                "authorization_url": "https://checkout.paystack.com/mock-reference-123",
                "reference": f"mock-ref-{request_data.get('email', 'test').replace('@', '-at-')}-{request_data.get('amount', 3000)}"
            }
        }
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
            response_data = {
                "status": True,
                "message": "Verification successful",
                "data": {
                    "domain": "test",
                    "status": "failed",
                    "reference": payment_id,
                    "paid_at": None,
                    "created_at": datetime.now().isoformat(),
                    "channel": "card",
                    "currency": "KES",
                    "amount": "3000.00"
                }
            }
            return httpx.Response(200, json=response_data)

        else:
            # Mock successful or pending payment
            paid_at = None if "mock-ref" in payment_id else datetime.now().isoformat()
            response_data = {
                "status": True,
                "message": "Verification successful",
                "data": {
                    "domain": "test",
                    "status": "success" if paid_at else "pending",
                    "reference": payment_id,
                    "paid_at": paid_at,
                    "created_at": datetime.now().isoformat(),
                    "channel": "card",
                    "currency": "KES",
                    "amount": "3000.00"
                }
            }
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