from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models import F, Sum, Case, When, IntegerField
from django.views import View
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from store.models.products import Product, Batch
from store.models.orders import Order, OrderItem
from vi_address.models import Ward, District, City
from store.models.carts import Cart as cart
from accounts.models import Address
from django.contrib import messages
from momo.MoMo import payWithMoMo
from store.views.test_message import get_message_list
from shipping.views import get_estimated_shipping_fee
import random
import traceback
import logging


class CheckOut(View):
    def get(self, request):
        try:
            user = request.user
            address = Address.objects.filter(account=user).first()
            ward = Ward.objects.get(pk=address.ward).name_with_type
            district = District.objects.get(pk=address.district).name_with_type
            city = City.objects.get(pk=address.city).name_with_type
            address = f"{address.specific_address}, {ward}, {district}, {city}"
            products = cart.objects.filter(account=request.user)
            estimated_shipping_fee = get_estimated_shipping_fee(request.user.pk)
            total = 0
            for product in products:
                sub_total = 1
                sub_total *= product.product.sell_price * product.product_qty
                product.sub_total = sub_total
                total += sub_total
            sub_total = total
            total += estimated_shipping_fee
        except BaseException:
            logging.error(traceback.format_exc())
            if not (
                cart.objects.filter(account=request.user)
                and Address.objects.filter(account=user)
            ):
                return redirect("cart")
        else:
            return render(
                request,
                "check_out.html",
                {"products": products, "total": total, "address": address, "estimated_shipping_fee": estimated_shipping_fee, "sub_total": sub_total},
            )

    def post(self, request):
        user = request.user
        get_infor_type = request.POST.get("get_infor_type")
        # Neu chon su dung thong tin mac dinh
        if get_infor_type == "defaultInfo":
            name = user.name
            phone = user.phone
            addr = Address.objects.get(account=user)
            ward = Ward.objects.get(pk=addr.ward)
            district = District.objects.get(pk=addr.district)
            city = City.objects.get(pk=addr.city)
            address = f"{addr.specific_address}, {ward.name_with_type}, {district.name_with_type}, {city.name_with_type}"
        elif get_infor_type == "manualInfo":
            specific_address = request.POST.get("specific_address")
            tmp_ward = request.POST.get("ward")
            tmp_district = request.POST.get("district")
            tmp_city = request.POST.get("city")
            if (
                tmp_city == 0 and tmp_district == 0 and tmp_ward == 0
            ) and not specific_address:
                messages.error(request, "Hãy điền đầy đủ thông tin")
                return JsonResponse({'messages': get_message_list(request)})
            ward = Ward.objects.get(id=tmp_ward)
            district = District.objects.get(id=tmp_district)
            city = City.objects.get(id=tmp_city)
            address = f"{specific_address}, {ward.name_with_type}, {district.name_with_type}, {city.name_with_type}"
            name = request.POST.get("name")
            phone = request.POST.get("phone")
        payment_method = request.POST.get("payment_method")
        note = request.POST.get("note")
        if not (get_infor_type and name and phone and address and payment_method):
            messages.error(request, "Hãy điền đầy đủ thông tin")
            return JsonResponse({'messages': get_message_list(request)})

        # tinh tong tien don hang
        products = cart.objects.filter(account=user)
        total_price = 0
        for product in products:
            total_price += product.product.sell_price * product.product_qty

        # tao ma van don
        d = datetime.now()
        current_date = d.strftime("%Y%m%d")
        trackno = current_date + str(random.randint(11111, 99999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = current_date + str(random.randint(11111, 99999))

        if payment_method == "momo":
            payUrl = payWithMoMo(request, trackno, total_price)
            self.placeOrder(
                user=user,
                name=name,
                phone=phone,
                address=address,
                city_name=city.name_with_type,
                district_name=district.name_with_type,
                ward_name=ward.name_with_type,
                payment_method=payment_method,
                note=note,
                total_price=total_price,
                trackno=trackno,
            )
            return JsonResponse({"Url": payUrl})
        elif payment_method == "cod":
            result = self.placeOrder(
                user=user,
                name=name,
                phone=phone,
                address=address,
                city_name=city.name_with_type,
                district_name=district.name_with_type,
                ward_name=ward.name_with_type,
                payment_method=payment_method,
                note=note,
                total_price=total_price,
                trackno=trackno,
            )
            if result:
                url = request.build_absolute_uri(f"/order/result/{trackno}")
                return JsonResponse({"Url": url})
            else:
                messages.error(request, "Đã xảy ra lỗi")
                return JsonResponse({'messages': get_message_list(request)})

    def placeOrder(
        self, user, name, phone, address, city_name, district_name, ward_name, payment_method, note, total_price, trackno
    ):
        new_order = Order()
        new_order.account = user
        new_order.name = name
        new_order.phone = phone
        new_order.address = address
        new_order.city_name = city_name
        new_order.district_name = district_name
        new_order.ward_name = ward_name
        new_order.payment_method = payment_method
        new_order.note = note
        new_order.total_price = total_price
        new_order.tracking_no = trackno
        if payment_method == "cod":
            new_order.processed = True
        elif payment_method == "momo":
            new_order.processed = False
        new_order.save()

        new_order_items = cart.objects.filter(account=user)
        for item in new_order_items:
            new_order_item = OrderItem()
            new_order_item.order = new_order
            new_order_item.product = item.product
            new_order_item.price = item.product.sell_price
            new_order_item.quantity = item.product_qty
            # giam so luong hang ton kho khi sp dat thanh cong
            ordered_product = item.product
            batchs = Batch.objects.filter(
                Product_id=ordered_product.id, status=1, quantity__gt=0
            ).order_by("expiry_date")
            if batchs is None:
                new_order.delete()
                return False
            i = 0
            item_id_dict = {}
            while i < len(batchs) and item.product_qty > 0:
                batch = batchs[i]
                if batch.quantity >= item.product_qty:
                    temp = batch.quantity - item.product_qty
                    Batch.objects.filter(id=batch.id).update(quantity=temp)
                    item_id_dict[batch.id] = item.product_qty
                    break
                else:
                    item.product_qty -= batch.quantity
                    item_id_dict[batch.id] = batch.quantity
                    Batch.objects.filter(id=batch.id).update(quantity=0)
                    i += 1
            new_order_item.batch = item_id_dict
            new_order_item.save()

        # xoa san pham trong gio
        cart.objects.filter(account=user).delete()
        return True
