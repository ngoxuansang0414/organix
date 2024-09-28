from django.urls import path
from .views import get_shipping_order_fee, get_available_services, get_addr, get_estimated_shipping_fee

urlpatterns = [
    # path("getcode/province/<str:province_name>/<str:district_name>/<str:ward_name>", get_order_address_id, name="province"),
    path("fee", get_shipping_order_fee),
    path("available-services/<str:from_district_name>/<str:from_province_name>/<str:to_district_name>/<str:to_province_name>", get_available_services),
    path("getaddr/<str:ward_name>/<str:district_name>/<str:province_name>", get_addr),
    path("estimated/fee", get_estimated_shipping_fee),
]