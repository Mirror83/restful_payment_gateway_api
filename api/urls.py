from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path("v1/payments/", views.initialize_payment, name="initialize_payment"),
    path("v1/payments/<str:payment_id>", views.get_payment_status, name="get_payment_status"),
]