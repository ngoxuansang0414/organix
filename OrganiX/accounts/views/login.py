from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views import View
from django.contrib import auth, messages
from accounts.models import Account
from store.views.test_message import get_message_list


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("email")
        user_check = Account.objects.filter(email=email).first()
        if user_check and user_check.is_active is False:
            messages.info(
                "Hãy kích hoạt tài khoản của bạn bằng đường dẫn đã gửi vào email"
            )
            return JsonResponse({'messages': get_message_list(request)})
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request=request, user=user)
            messages.success(
                request, "Đăng nhập thành công! Đang chuyển hướng tới trang chủ...",
            )
            return JsonResponse({'messages': get_message_list(request), "redirect": 1})
        else:
            messages.error(
                request, "Đăng nhập thất bại! Tài khoản hoặc mật khẩu không đúng",
            )
            return JsonResponse({'messages': get_message_list(request)})