from django.urls import path
from api import views

urlpatterns = [
    path("v1/payments/", views.initialize_payment),
    path("v1/payments/<str:payment_id>", views.get_payment_status),
]