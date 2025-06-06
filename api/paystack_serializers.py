from rest_framework import serializers


class BasePaystackResponse(serializers.Serializer):
    status = serializers.BooleanField()
    message = serializers.CharField()

class PaystackTransactionInitData(serializers.Serializer):
    authorization_url = serializers.URLField()
    reference = serializers.CharField()

class PaystackTransactionInitResponse(BasePaystackResponse):
    data = PaystackTransactionInitData()

class PaystackTransactionStatusData(serializers.Serializer):
    domain = serializers.CharField()
    status = serializers.CharField()
    reference = serializers.CharField()
    paid_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    channel = serializers.CharField()
    currency = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class PaystackTransactionStatusResponse(BasePaystackResponse):
    data = PaystackTransactionStatusData()