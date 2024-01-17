from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

from django.views import View
from django.http import HttpResponse, JsonResponse

from store.models.products import Product
from store.models.orders import Order, OrderItem
from vi_address.models import Ward, District, City
from store.models.carts import Cart as cart
from accounts.models import Address
from momo.MoMo import payWithMoMo
import datetime
import random

class CheckOut(View):
    def get(self , request):
        user = request.user
        address = Address.objects.filter(account = user).first()
        ward = Ward.objects.get(pk=address.ward).name_with_type
        district = District.objects.get(pk=address.district).name_with_type
        city = City.objects.get(pk=address.city).name_with_type
        address = f"{address.specific_address}, {ward}, {district}, {city}"
        products = cart.objects.filter(account = request.user)
        if not products:
            return redirect('cart')
        total = 0
        for product in products:
            sub_total = 1
            sub_total *= product.product.sale_price * product.product_qty
            product.sub_total = sub_total
            total += sub_total
        return render(request , 'check_out.html', {'products' : products, 'total': total, 'address': address})
    
    def post(self, request):
        user = request.user
        get_infor_type = request.POST.get('get_infor_type')
        #Neu chon su dung thong tin mac dinh
        if get_infor_type == 'defaultInfo':
            name = user.name
            phone = user.phone
            addr = Address.objects.get(account = user)
            ward = Ward.objects.get(pk=addr.ward).name_with_type
            district = District.objects.get(pk=addr.district).name_with_type
            city = City.objects.get(pk=addr.city).name_with_type
            address = f"{addr.specific_address}, {ward}, {district}, {city}"
        elif get_infor_type == 'manualInfo':
            specific_address = request.POST.get('specific_address')
            tmp_ward = request.POST.get('ward')
            tmp_district = request.POST.get('district')
            tmp_city = request.POST.get('city')
            if (tmp_city==0 and tmp_district==0 and tmp_ward==0) and not specific_address:
                return JsonResponse({'error':"Hãy điền đầy đủ thông tin"})
            ward = Ward.objects.get(id = tmp_ward)
            district = District.objects.get(id = tmp_district)
            city = City.objects.get(id = tmp_city)   
            address = f"{specific_address}, {ward.name_with_type}, {district.name_with_type}, {city.name_with_type}"
            name = request.POST.get('name')
            phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        note = request.POST.get('note')
        if not(get_infor_type and name and phone and address and payment_method):
            return JsonResponse({'error':"Hãy điền đầy đủ thông tin"})
        
        

        


        #tinh tong tien don hang
        products = cart.objects.filter(account=user)
        total_price = 0
        for product in products:
            total_price += product.product.sale_price * product.product_qty

        #tao ma van don
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        trackno = current_date+str(random.randint(11111,99999))
        while Order.objects.filter(tracking_no = trackno) is None:
            trackno = current_date+str(random.randint(11111,99999))

        if(payment_method == 'momo'):
            payUrl = payWithMoMo(trackno, total_price)
            self.placeOrder(user = user, name = name, phone = phone, 
                            address = address, payment_method = payment_method, 
                            note = note, total_price = total_price, trackno = trackno)
            return JsonResponse({"Url": payUrl})
        elif(payment_method == 'cod'):
            self.placeOrder(user = user, name = name, phone = phone, 
                            address = address, payment_method = payment_method, 
                            note = note, total_price = total_price, trackno = trackno)
            return HttpResponse('Đặt hàng thành công')
        
    def placeOrder(self, user, name, phone, address, payment_method, note, total_price, trackno):
        new_order = Order()
        new_order.account = user
        new_order.name = name
        new_order.phone = phone
        new_order.address = address
        new_order.payment_method = payment_method
        new_order.note = note     
        new_order.total_price = total_price
        new_order.tracking_no = trackno
        new_order.save()

        new_order_items = cart.objects.filter(account = user)
        for item in new_order_items:
            OrderItem.objects.create(
                order = new_order,
                product = item.product,
                price = item.product.sale_price,
                quantity = item.product_qty
            )
            #giam so luong hang ton kho khi sp dat thanh cong
            order_product = Product.objects.filter(id = item.product.id).first()
            order_product.stock = order_product.stock - item.product_qty
            order_product.save()

        #xoa san pham trong gio
        cart.objects.filter(account=user).delete()
        return True