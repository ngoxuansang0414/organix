from django.urls import path
from .views import thanks, ipn

urlpatterns = [
    path("thanks", thanks, name="thanks"),
    path("ipn", ipn, name="paymentResult"),
]
