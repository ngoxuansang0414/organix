from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password

from django.views import  View
from store.models.products import Product
from store.models.carts import Cart as cart
from django.http.response import JsonResponse


class Cart(View):
    def get(self , request):
        products = cart.objects.filter(account = request.user)
        total = 0
        for product in products:
            sub_total = 1
            sub_total *= product.product.sale_price * product.product_qty
            product.sub_total = sub_total
            total += sub_total
        return render(request , 'cart.html' , {'products' : products, 'total': total})
    
    def post(self, request):
        user = request.user
        if (request.POST.get('add-to-cart')):
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            prod_qty = int(request.POST.get('product_qty'))
            if(product_check):
                #SP da co trong gio
                if(cart.objects.filter (account=user, product=prod_id)):
                    new_cart = cart.objects.get (account=user, product=prod_id)
                    if product_check.stock - (prod_qty + new_cart.product_qty) >= 0:
                        new_cart = cart.objects.get (account=user, product=prod_id)
                        new_cart.product_qty += prod_qty
                        new_cart.save()
                        return JsonResponse({'status':'Thêm sản phẩm vào giỏ thành công'})
                    else:
                        return JsonResponse({'status': f'Chỉ còn lại {str(product_check.stock)} sản phẩm'})
                else:
                    #SP chua co trong gio
                    if product_check.stock - prod_qty >= 0:
                        cart.objects.create(account=user, product=product_check, product_qty = prod_qty)
                        return JsonResponse({'status':'Thêm sản phẩm vào giỏ thành công'})
                    else:
                        return JsonResponse({'status': f'Chỉ còn lại {str(product_check.stock)} sản phẩm'})
            else:
                return JsonResponse({'status': 'Không tìm thấy sản phẩm'})
            
        elif (request.POST.get('update-cart')):
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            prod_qty = int(request.POST.get('product_qty'))
            if(product_check):
                new_cart = cart.objects.get (account=user, product=prod_id)
                new_cart.product_qty = prod_qty
                new_cart.save()
                if(product_check.stock == prod_qty):
                    return JsonResponse({'status': f'Chỉ còn lại {str(product_check.stock)} sản phẩm', 'flag': 1})
                return JsonResponse({'status':'Thay đổi giỏ hàng thành công'})

        elif(request.POST.get('remove-item')):
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                new_cart = cart.objects.get (account=user, product=prod_id)
                if(new_cart):
                    new_cart.delete()
                    return JsonResponse({'status':'Xóa sản phẩm khỏi giỏ thành công'})
            else:
                return JsonResponse({'status': 'Không tìm thấy sản phẩm'})
        else:
            return JsonResponse({'status': 'Đăng nhập để tiếp tục'})
        

        

    
    