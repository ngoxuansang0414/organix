from django.shortcuts import render
from accounts.models import Address
from django.views import View
from django.http import JsonResponse
from vi_address.models import Ward, District, City
from django.contrib import messages
import traceback
import logging
from store.views.test_message import get_message_list
import re


def vietnamese_phone_number_check(phone_number):
    # Mẫu số điện thoại Việt Nam hợp lệ
    pattern = r"^(?:\+84|0)(3[2-9]|5[5|6|8|9]|7[0|6-9]|8[1-9]|9[0-9])[0-9]{7}$"
    
    # Kiểm tra số điện thoại có khớp với mẫu hay không
    return bool(re.match(pattern, phone_number))


class User(View):
    def get(self, request):
        try:
            user = request.user
            address = Address.objects.filter(account=user).first()
            ward = Ward.objects.get(pk=address.ward).name_with_type
            district = District.objects.get(pk=address.district).name_with_type
            city = City.objects.get(pk=address.city).name_with_type
            address = f"{address.specific_address}, {ward}, {district}, {city}"
        except BaseException:
            logging.error(traceback.format_exc())
        finally:
            return render(request, "user_dashboard.html", {"address": address})

    def post(self, request):
        email = request.POST.get("email")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        specific_address = request.POST.get("specific_address")
        tmp_ward = request.POST.get("ward")
        tmp_district = request.POST.get("district")
        tmp_city = request.POST.get("city")

        if (
            email
            and name
            and phone
            and gender
        ):
            user = request.user
            user.name = name
            if vietnamese_phone_number_check(phone):
                user.phone = phone
            else:
                messages.error(request, "Số điện thoại không hợp lệ")
                return JsonResponse({'messages': get_message_list(request)})
            user.gender = gender
            if specific_address and tmp_ward != '0':
                ward = Ward.objects.get(id=tmp_ward)
                district = District.objects.get(id=tmp_district)
                city = City.objects.get(id=tmp_city)
                address = Address.objects.get(account=request.user)
                address.specific_address = specific_address
                address.city = city.id
                address.district = district.id
                address.ward = ward.id
                address.save()
            user.save()
            messages.success(request, "Cập nhật thông tin thành công")
            return JsonResponse({'messages': get_message_list(request), "redirect": 1})
        elif not (
            email
            and name
            and phone
            and gender
        ):
            messages.error(request, "Vui lòng điền đầy đủ thông tin")
            return JsonResponse({'messages': get_message_list(request)})
        else:
            messages.error(request, "Đã xảy ra lỗi")
            return JsonResponse({'messages': get_message_list(request)})
