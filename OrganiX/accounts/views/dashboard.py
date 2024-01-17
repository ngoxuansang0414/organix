from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from accounts.models import Address
from django.views import  View
from django.http import HttpResponse
from vi_address.models import Ward, District, City

class User(View):
    def get(self, request):
        user = request.user
        address = Address.objects.filter(account = user).first()
        ward = Ward.objects.get(pk=address.ward).name_with_type
        district = District.objects.get(pk=address.district).name_with_type
        city = City.objects.get(pk=address.city).name_with_type
        address = f"{address.specific_address}, {ward}, {district}, {city}"
        return render(request, 'user_dashboard.html', {'address': address})
    
    def post(self, request):
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        specific_address = request.POST.get('specific_address')
        tmp_ward = request.POST.get('ward')
        tmp_district = request.POST.get('district')
        tmp_city = request.POST.get('city')
        print(tmp_ward, tmp_district,tmp_city)
        
        ward = Ward.objects.get(id = tmp_ward)
        district = District.objects.get(id = tmp_district)
        city = City.objects.get(id = tmp_city)
        user = request.user

        address = Address.objects.get(account = user)

        if email and name and phone and gender and specific_address and tmp_city and tmp_district and tmp_ward:
            user.name = name
            user.phone = phone
            user.gender = gender
            user.save()
            address.specific_address = specific_address
            address.city = city.id
            address.district = district.id
            address.ward = ward.id
            address.save()
            return HttpResponse('Cập nhật thông tin thành công!')
        elif email or name or phone or gender or specific_address or tmp_city or tmp_district or tmp_ward:
            return HttpResponse('Không được để trống thông tin')
        else:
            return HttpResponse('Đã xảy ra lỗi!')