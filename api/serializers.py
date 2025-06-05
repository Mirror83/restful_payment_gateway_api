from rest_framework import serializers

class PaymentInfo(serializers.Serializer):
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)