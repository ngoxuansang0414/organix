from django.contrib import admin
from django.urls import path, include
from store.views.home import Index , store, product, product_detail
from .views.cart import Cart
from .views.checkout import CheckOut
from momo.views import thanks
from .views.order import OrderView
from store.views.search import SearchView
from store.views.rating import submit_review

from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views.address import select_city, select_district, select_ward


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('store/<str:slug>', product, name='product'),
    path('store/<str:cate_slug>/<str:prod_slug>', product_detail, name='product_detail'),

    path('cart', login_required(Cart.as_view(), login_url='/accounts/login?next=/store') , name='cart'),
    path('checkout', login_required(CheckOut.as_view(), login_url='/accounts/login?next=/store') , name='checkout'),
    path('orders', login_required(OrderView.as_view(), login_url='/accounts/login?next=/store'), name='orders'),
    path('thankyou', login_required(thanks, login_url='/accounts/login?next=/store'), name='thankyou'),
    path('submit_review/<int:order_id>/<int:product_id>', login_required(submit_review, login_url='/accounts/login?next=/store'), name='submit_review'),

    #chon dia diem giao hang
    path('api/address/', include('vi_address.urls')),
    path('address/city', select_city, name='city'),
    path('address/<str:city>/districts/', select_district, name='district'),
    path('address/<str:district>/wards', select_ward, name='ward'),

    #tim kiem san pham
    path('search', SearchView.as_view(), name='search')


]