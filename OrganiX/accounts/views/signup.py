from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from accounts.models import Gender, Account, Address
from store.models.carts import Cart
from django.views import View
from django.http import HttpResponse, JsonResponse
from vi_address.models import Ward, District, City
from store.views.test_message import get_message_list
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import re
from string import punctuation
from email.mime.multipart import MIMEMultipart


class Signup(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        email = request.POST.get("email")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        gender = request.POST.get("gender")
        specific_address = request.POST.get("specific_address")
        tmp_ward = request.POST.get("ward")
        tmp_district = request.POST.get("district")
        tmp_city = request.POST.get("city")
        if not (
            email
            and name
            and phone
            and password
            and confirm_password
            and gender
            and specific_address
            and (tmp_ward != '0')
        ):
            messages.error(request, "Hãy điền đầy đủ thông tin")
            return JsonResponse({'messages': get_message_list(request)})
        
        if password != confirm_password:
            messages.error(request, "Mật khẩu xác nhận không khớp")
            return JsonResponse({'messages': get_message_list(request)})
        ward = Ward.objects.get(id=tmp_ward)
        district = District.objects.get(id=tmp_district)
        city = City.objects.get(id=tmp_city)
        # validation

        user = Account(email=email, phone=phone, password=password)
        error_message = self.validateCustomer(user)
        if error_message:
            messages.error(request, error_message)
            return JsonResponse({'messages': get_message_list(request)})
        else:
            user = Account.objects.create_user(
                email=email, name=name, phone=phone, password=password, gender=gender
            )
            user.save()
            address = Address(
                account=user,
                specific_address=specific_address,
                ward=ward.id,
                district=district.id,
                city=city.id,
            )
            address.save()
            current_site = get_current_site(request=request)
            mail_subject = "Kích hoạt tài khoản Organix của bạn"
            message = render_to_string(
                "active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            header = MIMEMultipart()
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()
            messages.error(request, "Tạo tài khoản thành công")
            return JsonResponse({'messages': get_message_list(request)})

    def validateCustomer(self, customer):
        error_message = None

        if Account.objects.filter(email=customer.email):
            error_message = "Email này đã được sử dụng"
        elif self.vietnamese_phone_number_check(customer.phone) == False:
            error_message = "Số điện thoại không hợp lệ"
        elif len(customer.password) < 8:
            error_message = "Mật khẩu phải chứa nhiều hơn 8 ký tự"
        elif self.email_check(customer.email) is False:
            error_message = "Email không đúng định dạng"
        elif self.password_check(customer.password) is False:
            error_message = "Mật khẩu không đủ phức tạp"
            if re.search(" ", customer.password):
                error_message = "Mật khẩu không được chứa khoảng trắng"

        return error_message

    def email_check(self, email):
        pat = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if re.match(pat, email):
            return True
        else:
            return False

    def password_check(self, password):
        spcharacters = set(punctuation)
        while True:
            if len(password) <= 8:
                return False
            elif not re.search("[a-z]", password):
                return False
            elif not re.search("[A-Z]", password):
                return False
            elif not re.search("[0-9]", password):
                return False
            elif not any(char in spcharacters for char in password):
                return False
            elif re.search(" ", password):
                return False
            else:
                return True
            
    def vietnamese_phone_number_check(phone_number):
        # Mẫu số điện thoại Việt Nam hợp lệ
        pattern = r"^(?:\+84|0)(3[2-9]|5[5|6|8|9]|7[0|6-9]|8[1-9]|9[0-9])[0-9]{7}$"
        
        # Kiểm tra số điện thoại có khớp với mẫu hay không
        return bool(re.match(pattern, phone_number))
