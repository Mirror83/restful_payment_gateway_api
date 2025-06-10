import os

import httpx
from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from api.paystack_serializers import PaystackTransactionStatusResponse
from api.serializers import PaymentInfo, PaystackTransactionInitResponse

PAYSTACK_API_URL = "https://api.paystack.co"


def get_paystack_client():
    headers = {
        "Authorization": f"Bearer {os.environ.get('PAYSTACK_TEST_SECRET_KEY')}",
        "Content-Type": "application/json",
    }
    return httpx.Client(base_url=PAYSTACK_API_URL, headers=headers)

@extend_schema(request = PaymentInfo, responses = PaystackTransactionInitResponse)
class InitPaymentView(generics.GenericAPIView):
    def post(self, request: Request):
        """Initialize payment given the request data"""
        # Validate request body data
        data = request.data
        serializer = PaymentInfo(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with get_paystack_client() as client:
            request_data = {
                "email": data["customer_email"],
                # Multiply by 100 to convert into Paystack subunits
                "amount": int(data["amount"] * 100)
            }
            response = client.post("/transaction/initialize", json=request_data)

            data = response.json()

            if not response.is_success:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            # Validate Paystack API call response data
            paystack_response_serializer = PaystackTransactionInitResponse(data=data)
            if not paystack_response_serializer.is_valid():
                return Response(paystack_response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Everything went well, build response
            return Response(paystack_response_serializer.data, status=status.HTTP_200_OK)

@extend_schema(responses = PaystackTransactionStatusResponse)
class GetPaymentStatusView(generics.GenericAPIView):
    def get(self, request: Request, payment_id: str):
        """Handle POST request for payment status"""
        with get_paystack_client() as client:
            # Call Paystack API to retrieve payment status
            response = client.get(f"/transaction/verify/{payment_id}")
            print(f"{response.status_code=}")

            data = response.json()
            if not response.is_success:
                if data["code"] == "transaction_not_found":
                    return Response(
                        {
                            "payment_id": payment_id,
                            "status": "failed",
                            "message": "Payment with the given payment id not found"
                        },
                        status=status.HTTP_404_NOT_FOUND)
                return Response(
                    {"payment_id": payment_id, "status": "failed"},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer = PaystackTransactionStatusResponse(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)

