import os
from json import JSONDecodeError

import httpx
from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from api.paystack_serializers import PaystackTransactionStatusResponseSerializer
from api.serializers import PaymentInfoSerializer, PaystackTransactionInitResponseSerializer

PAYSTACK_API_URL = "https://api.paystack.co"


def get_paystack_client():
    headers = {
        "Authorization": f"Bearer {os.environ.get('PAYSTACK_TEST_SECRET_KEY')}",
        "Content-Type": "application/json",
    }
    return httpx.Client(base_url=PAYSTACK_API_URL, headers=headers)

@extend_schema(request = PaymentInfoSerializer, responses = PaystackTransactionInitResponseSerializer)
class InitPaymentView(generics.GenericAPIView):
    def post(self, request: Request):
        """Initialize payment given the request data"""
        # Validate request body data
        request_serializer = PaymentInfoSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = request_serializer.to_data_class()

        with get_paystack_client() as client:
            paystack_request_data = {
                "email": data.customer_email,
                # Multiply by 100 to convert into Paystack subunits
                "amount": int(data.amount * 100)
            }
            paystack_response = client.post("/transaction/initialize", json=paystack_request_data)

            if not paystack_response.is_success:
                try:
                    return Response(paystack_response.json(), status=status.HTTP_400_BAD_REQUEST)
                except JSONDecodeError as e:
                    # In case the error is one without a JSON response body (e.g. 5xx)
                    print(e)
                    return Response(
                        {"status": False, "message": "Server error", "data": {}},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )


            data = paystack_response.json()
            # Validate Paystack API call response data
            paystack_response_serializer = PaystackTransactionInitResponseSerializer(data=data)
            if not paystack_response_serializer.is_valid():
                return Response(
                    paystack_response_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

            # Everything is OK, save payment and send response
            return Response(paystack_response_serializer.data, status=status.HTTP_200_OK)

@extend_schema(responses = PaystackTransactionStatusResponseSerializer)
class GetPaymentStatusView(generics.GenericAPIView):
    def get(self, request: Request, payment_id: str):
        """Handle POST request for payment status"""
        with get_paystack_client() as client:
            # Call Paystack API to retrieve payment status
            response = client.get(f"/transaction/verify/{payment_id}")
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

            serializer = PaystackTransactionStatusResponseSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)

