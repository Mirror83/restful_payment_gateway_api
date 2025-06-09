from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path("v1/payments/", views.InitPaymentView.as_view(), name="initialize_payment"),
    path("v1/payments/<str:payment_id>/", views.GetPaymentStatusView.as_view(), name="get_payment_status"),
]