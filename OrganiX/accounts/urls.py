from django.urls import path
from .views.signup import Signup
from .views.login import Login
from .views.dashboard import User
from .views.logout import logout
from .views.activate import activate
from .views.password import  send_email_reset, reset_password_validate, reset_password, change_password
from .views.address import select_city, select_district, select_ward
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('change_password', change_password, name='change_password'),
    path('resetpassword', send_email_reset, name='sendEmailReset'),
    path('reset_password_validate/<uidb64>/<token>', reset_password_validate, name='reset_password_validate'),
    path('reset_password/', reset_password, name='reset_password'),
    path('profile',login_required(User.as_view(), login_url='/accounts/login?next=/store') , name='profile'),
    path('activate/<uidb64>/<token>', activate, name='activate'),

    path('address/city', select_city, name='city'),
    path('address/<str:city>/districts/', select_district, name='district'),
    path('address/<str:district>/wards', select_ward, name='ward'),

]