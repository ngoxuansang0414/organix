from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from django.db.models import Sum
from django.views import View
from store.models.products import Product
from store.models.carts import Cart as cart
from django.http.response import JsonResponse
from django.contrib import auth, messages
from store.views.test_message import get_message_list

from shipping.views import get_estimated_shipping_fee


class Cart(View):
    def get(self, request):
        products = cart.objects.filter(account=request.user)
        total = 0
        index = 0
        shipping_fee = get_estimated_shipping_fee(request.user.pk)
        # shipping_fee = 0
        for product in products:
            sub_total = 1
            sub_total *= product.product.sell_price * product.product_qty
            product.sub_total = sub_total
            total += sub_total
            product.stock = Product.get_stock_quantity(product.product)
            index += 1
        total += shipping_fee
        return render(request, "cart.html", {"products": products, "total": total, "shipping_fee": shipping_fee})

    def post(self, request):
        user = request.user
        if request.POST.get("add-to-cart"):
            prod_id = int(request.POST.get("product_id"))
            product_check = Product.objects.get(id=prod_id)
            product_check.stock = Product.get_stock_quantity(product_check)
            prod_qty = int(request.POST.get("product_qty"))
            if product_check:
                # SP da co trong gio
                if cart.objects.filter(account=user, product=prod_id):
                    new_cart = cart.objects.get(account=user, product=prod_id)
                    if product_check.stock - (prod_qty + new_cart.product_qty) >= 0:
                        new_cart = cart.objects.get(account=user, product=prod_id)
                        new_cart.product_qty += prod_qty
                        new_cart.save()
                        messages.success(request, "Thêm sản phẩm vào giỏ thành công")
                        return JsonResponse({'messages': get_message_list(request)})
                    else:
                        messages.error(request, f"Chỉ còn lại {str(product_check.stock)} sản phẩm")
                        return JsonResponse({'messages': get_message_list(request)})

                else:
                    # SP chua co trong gio
                    if product_check.stock - prod_qty >= 0:
                        cart.objects.create(
                            account=user, product=product_check, product_qty=prod_qty
                        )
                        messages.success(request, "Thêm sản phẩm vào giỏ thành công")
                        return JsonResponse({'messages': get_message_list(request)})

                    else:
                        messages.error(request, f"Chỉ còn lại {str(product_check.stock)} sản phẩm")
                        print(get_message_list(request))
                        return JsonResponse({'messages': get_message_list(request)})
            else:
                messages.error(request, "Không tìm thấy sản phẩm")
                return JsonResponse({'messages': get_message_list(request)})

        elif request.POST.get("update-cart"):
            prod_id = int(request.POST.get("product_id"))
            product_check = Product.objects.get(id=prod_id)
            product_check.stock = Product.get_stock_quantity(product_check)
            prod_qty = int(request.POST.get("product_qty"))
            if product_check:
                new_cart = cart.objects.get(account=user, product=prod_id)
                new_cart.product_qty = prod_qty

                if product_check.stock < prod_qty:
                    messages.error(request, f"Chỉ còn lại {str(product_check.stock)} sản phẩm")
                    return JsonResponse({'messages': get_message_list(request)})
                elif product_check.stock == prod_qty:
                    messages.error(request, f"Chỉ còn lại {str(product_check.stock)} sản phẩm")
                    new_cart.save()
                    return JsonResponse({'messages': get_message_list(request)})
                new_cart.save()
                return JsonResponse({'messages': get_message_list(request)})

        elif request.POST.get("remove-item"):
            prod_id = int(request.POST.get("product_id"))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                new_cart = cart.objects.get(account=user, product=prod_id)
                if new_cart:
                    new_cart.delete()
                    messages.success(request, "Xóa sản phẩm khỏi giỏ thành công")
                    return JsonResponse({'messages': get_message_list(request)})
            else:
                messages.error(request, "Không tìm thấy sản phẩm")
                return JsonResponse({'messages': get_message_list(request)})
        else:
            messages.error(request, "Đăng nhập để tiếp tục")
            return JsonResponse({'messages': get_message_list(request)})
