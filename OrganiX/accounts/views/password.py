from accounts.models import Account
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
import re
from string import punctuation

def send_email_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Account.objects.get(email=email)
        if not user:
            return HttpResponse("Tài khoản không tồn tại!")
        current_site = get_current_site(request=request)
        mail_subject = 'Đặt lại mật khẩu tài khoản Organix'
        message = render_to_string('reset_password_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })
        send_email = EmailMessage(mail_subject, message, to=[email])
        send_email.send()

        return HttpResponse("Yêu cầu đặt lại mật khẩu đã được gửi đến địa chỉ email của bạn")

        
    if request.method == 'GET':
        context = {
            'email': email if 'email' in locals() else '',
        }
        return render(request, "forgotPassword.html", context=context)
    

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('reset_password')
    else:
        return HttpResponse("Liên kết đã hết hạn!")

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password and confirm_password and (password == confirm_password):
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            if password_check(password) is False:
                error_message = 'Mật khẩu không đủ phức tạp'
                if re.search("\s" , password):
                    error_message = 'Mật khẩu không được chứa khoảng trắng'
                return HttpResponse(error_message)
            user.set_password(password)
            user.save()
            return JsonResponse({'msg': "Đặt lại mật khẩu thành công!", 'status': True})
        else:
            return HttpResponse("Mật khẩu không khớp!")
    return render(request, 'reset_password.html')

@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user = request.user
    if (not user.check_password(old_password)):
        return HttpResponse("Sai mật khẩu hiện tại!")
    elif (password != confirm_password):
        return HttpResponse("Mật khẩu mới không khớp!")
    elif (old_password == password) and (password == confirm_password):
        return HttpResponse("Mật khẩu mới không được trùng với mật khẩu hiện tại!")
    else:
        if password_check(password) is False:
            error_message = 'Mật khẩu không đủ phức tạp'
            if re.search("\s" , password):
                error_message = 'Mật khẩu không được chứa khoảng trắng'
            return HttpResponse(error_message)
        user.set_password(password)
        user.save()
        return JsonResponse({'msg': "Đổi mật khẩu thành công!", 'status': True})
    
def password_check(password):
    spcharacters = set(punctuation)
    while True:
        if (len(password)<=8):
            return False
        elif not re.search("[a-z]", password):
            return False
        elif not re.search("[A-Z]", password):
            return False
        elif not re.search("[0-9]", password):
            return False
        elif not any(char in spcharacters for char in password):
            return False
        elif re.search("\s" , password):
            return False
        else:
            return True