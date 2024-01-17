from django.shortcuts import render , redirect ,HttpResponse, HttpResponseRedirect
from store.models.products import Product
from store.models.categories import Category
from django.views import View
from store.models.description import Description
from store.models.orders import Order, OrderItem
from django.contrib import messages
from store.views.rating import ReviewRating


# Create your views here.
class Index(View):

    def post(self , request):
        return render(request, 'index.html')

    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    categories = Category.objects.filter(status = 0)
    data = {'categories': categories}
    return render(request, 'index.html', data)

def product(request, slug):
    if(Category.objects.filter(slug = slug, status = 0)):
        products = Product.objects.filter(category__slug = slug)
        category_name = Category.objects.filter(slug = slug).first()
        data = {'products': products, 'category_name': category_name}
        return render(request, 'products.html', data)
    else:
        messages.warning(request, 'Không tìm thấy loại mặt hàng')
        return redirect('store')

def product_detail(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug = cate_slug, status = 0)):
        if(Product.objects.filter(slug = prod_slug, status = 0)):
            product = Product.objects.filter(slug = prod_slug, status = 0).first()
            ordered = OrderItem.objects.filter(product = product)
            ordered_quantity = 0
            for i in ordered:
                if i.order.status == 'Hoàn thành':
                    ordered_quantity += i.quantity
            description = Description.objects.filter(product = product).first()
            reviews = ReviewRating.objects.filter(product = product, status = True)
            data = {'product': product, 'ordered_quantity': ordered_quantity, 'description': description, 'reviews': reviews}
        else:
            HttpResponse('Không tìm thấy sản phẩm')
            return redirect('store')
    else:
        HttpResponse('Không tìm thấy loại mặt hàng')
        return redirect('store')
    return render(request, 'product_detail.html', data)

