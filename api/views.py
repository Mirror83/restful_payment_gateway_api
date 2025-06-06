import os

import httpx
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

from api.paystack_serializers import PaystackTransactionStatusResponse
from api.serializers import PaymentInfo, PaystackTransactionInitResponse

PAYSTACK_API_URL = "https://api.paystack.co"

def get_paystack_client():
    headers = {
        "Authorization": f"Bearer {os.environ.get('PAYSTACK_TEST_SECRET_KEY')}",
        "Content-Type": "application/json",
    }
    return httpx.Client(base_url=PAYSTACK_API_URL, headers=headers)

@csrf_exempt
def initialize_payment(request: HttpRequest):
    if request.method != "POST":
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Validate request body data
    data = JSONParser().parse(request)
    serializer = PaymentInfo(data=data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    with get_paystack_client() as client:
        request_data = {
            "email": data["customer_email"],
            # Multiply by 100 to convert into Paystack subunits
            "amount": int(data["amount"] * 100)
        }
        response = client.post("/transaction/initialize", json=request_data)

        if not response.is_success:
            return JsonResponse(response.json(), status=status.HTTP_400_BAD_REQUEST)
        data = response.json()

        # Validate Paystack API call response data
        paystack_response_serializer = PaystackTransactionInitResponse(data=data)
        if not paystack_response_serializer.is_valid():
            return JsonResponse(paystack_response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Everything went well, build response
        return JsonResponse(paystack_response_serializer.data, status=status.HTTP_200_OK)


def get_payment_status(request: HttpRequest, payment_id: str):
    if request.method != "GET":
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    with get_paystack_client() as client:
        # Call Paystack API to retrieve payment status
        response = client.get(f"/transaction/verify/{payment_id}")
        if not response.is_success:
            return JsonResponse(
                {"payment_id": payment_id,"status": "failed"},
                status=status.HTTP_400_BAD_REQUEST)

        data = response.json()
        serializer = PaystackTransactionStatusResponse(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
