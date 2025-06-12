from django.db import models

class Payment(models.Model):
    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    reference = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=PAYMENT_STATUS, default=PAYMENT_STATUS[0][0], max_length=10)
    paid_at = models.DateTimeField(null=True, blank=True)
    initiated_at = models.DateTimeField(auto_now_add=True)

