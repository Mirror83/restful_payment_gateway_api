from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

from api.serializers import PaymentInfo

@csrf_exempt
def initialize_payment(request: HttpRequest):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = PaymentInfo(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            return JsonResponse(validated_data)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_payment_status(request: HttpRequest, payment_id: str):
    if request.method == "GET":
        return JsonResponse({"payment_id": payment_id,"status": "success"})

    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)