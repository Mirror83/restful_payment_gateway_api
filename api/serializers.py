from rest_framework import serializers

from api.paystack_serializers import PaystackTransactionInitResponse, PaystackTransactionStatusData

class PaymentInfo(serializers.Serializer):
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class BaseResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    data = serializers.JSONField()  # `data` should be overridden

class InitiatePaymentResponse(BaseResponseSerializer):
    data = PaystackTransactionInitResponse()

class GetPaymentStatusResponse(BaseResponseSerializer):
    data = PaystackTransactionStatusData()