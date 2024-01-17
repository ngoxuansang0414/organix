from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from accounts.models import Account
from django.http import HttpResponse

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        #HttpResponse("Tài khoản của bạn đã được kích hoạt thành công, hãy đăng nhập!")
        return redirect('login')
    else:
        messages.error(request=request, message="Đường dẫn kích hoạt không hợp lệ!")
        return redirect('homepage')