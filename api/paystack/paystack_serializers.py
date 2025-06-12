from rest_framework import serializers

class BasePaystackResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    message = serializers.CharField()

class PaystackTransactionInitDataSerializer(serializers.Serializer):
    authorization_url = serializers.URLField()
    reference = serializers.CharField()

class PaystackTransactionInitResponseSerializer(BasePaystackResponseSerializer):
    data = PaystackTransactionInitDataSerializer()

class PaystackTransactionStatusDataSerializer(serializers.Serializer):
    domain = serializers.CharField()
    status = serializers.CharField()
    reference = serializers.CharField()
    # When querying the status of a payment that is yet to be made
    # has failed or has been abandoned, `paid_at` will be null.
    paid_at = serializers.DateTimeField(allow_null=True)
    created_at = serializers.DateTimeField()
    channel = serializers.CharField()
    currency = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class PaystackTransactionStatusResponseSerializer(BasePaystackResponseSerializer):
    data = PaystackTransactionStatusDataSerializer()
