from django.urls import path
from api import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

app_name = "api"

urlpatterns = [
    path("v1/payments/", views.InitPaymentView.as_view(), name="initialize_payment"),
    path("v1/payments/<str:payment_id>/", views.GetPaymentStatusView.as_view(), name="get_payment_status"),
    path("v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger-ui"),
    path("v1/schema/redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"),
]