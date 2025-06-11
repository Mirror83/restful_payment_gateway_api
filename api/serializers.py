from dataclasses import dataclass
from decimal import Decimal

from rest_framework import serializers

from api.paystack_serializers import (
    PaystackTransactionStatusDataSerializer,
    PaystackTransactionInitResponseSerializer)


@dataclass
class PaymentInfo:
    customer_name: str
    customer_email: str
    amount: Decimal

class PaymentInfoSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def to_data_class(self):
        return PaymentInfo(**self.validated_data)

class BaseResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    data = serializers.JSONField()  # `data` should be overridden

class InitiatePaymentResponseSerializer(BaseResponseSerializer):
    data = PaystackTransactionInitResponseSerializer()

class GetPaymentStatusResponseSerializer(BaseResponseSerializer):
    data = PaystackTransactionStatusDataSerializer()