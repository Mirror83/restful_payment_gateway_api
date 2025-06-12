from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from api.paystack.paystack_client import PaystackClient, PaystackClientException
from api.paystack.paystack_serializers import PaystackTransactionStatusResponseSerializer
from api.serializers import PaymentInfoSerializer, PaystackTransactionInitResponseSerializer

paystack_client = PaystackClient()

@extend_schema(
    request = PaymentInfoSerializer,
    responses = PaystackTransactionInitResponseSerializer)
class InitPaymentView(generics.GenericAPIView):
    def post(self, request: Request):
        """Initialize payment given the request data"""
        # Validate request body data
        request_serializer = PaymentInfoSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        payment_info = request_serializer.to_data_class()
        try:
            data = paystack_client.init_payment(
                email=payment_info.customer_email,
                amount=int(payment_info.amount * 100))
        except PaystackClientException as e:
            if e.data is not None:
                return Response(e.data, status=e.status_code)
            else:
                return Response("Unknown error", status=e.status_code)

        return Response(data, status=status.HTTP_200_OK)

@extend_schema(
    responses = PaystackTransactionStatusResponseSerializer
)
class GetPaymentStatusView(generics.GenericAPIView):
    def get(self, request: Request, payment_id: str):
        """Handle POST request for payment status"""
        try:
            data = paystack_client.get_payment_status(payment_id)
        except PaystackClientException as e:
            if e.data is not None:
                return Response(e.data, status=e.status_code)
            else:
                return Response("Unknown error", status=e.status_code)

        return Response(data, status=status.HTTP_200_OK)
