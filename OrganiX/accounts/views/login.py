from django.shortcuts import render , redirect , HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import  check_password

from django.views import View
from django.contrib import auth, messages
from accounts.models import Account


class Login(View):
    def get(self, request):
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        user_check = Account.objects.filter(email = email).first()
        if user_check and user_check.is_active == False:
            return HttpResponse("Hãy kích hoạt tài khoản của bạn bằng đường dẫn đã gửi vào email")
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request=request, user=user)
            return HttpResponse('Đăng nhập thành công')
        else:
            return HttpResponse('Đăng nhập thất bại')