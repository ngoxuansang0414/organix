from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from store.models.products import Product, Batch
from store.models.categories import Category
from django.views import View
from store.models.description import Description
from store.models.orders import Order, OrderItem
from django.contrib import messages
from store.views.rating import ReviewRating
from store.models.carts import Cart as cart
from django.http import JsonResponse
from django.core.paginator import Paginator
import random
from django.contrib import messages



# Create your views here.
class Index(View):

    def post(self, request):
        return render(request, "index.html")

    def get(self, request):
        # print()
        return HttpResponseRedirect(f"/store{request.get_full_path()[1:]}")


def store(request):
    categories = Category.objects.filter(status=1)
    products = Product.objects.all()
    random_products= random.sample(list(products), 8)
    data = { "products": random_products}
    return render(request, "index.html", data)

    
def products(request, slug):
    if slug == 'all':
        products = Product.objects.filter(status=1)
        title = 'Tất cả sản phẩm'
    else:
        products = Product.objects.filter(category__slug=slug, status=1)
        title = Category.objects.filter(slug=slug).first().name
    all_products = Product.objects.filter(status=1).count()
    categories = Category.objects.filter(status=1)
    for category in categories:
        category.prod_count = Product.product_count(category.pk)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'page_obj': page_obj, "categories": categories, "all_products": all_products, "title": title}
    return render(request, "products.html", data)
    
    
def product_detail(request, cate_slug, prod_slug):
    if Category.objects.filter(slug=cate_slug, status=1):
        if Product.objects.filter(slug=prod_slug, status=1):
            product = Product.objects.filter(slug=prod_slug, status=1).first()
            product.stock = Product.get_stock_quantity(product)
            ordered = OrderItem.objects.filter(product=product)
            ordered_quantity = 0
            for i in ordered:
                if i.order.status == "Hoàn thành":
                    ordered_quantity += i.quantity
            description = Description.objects.filter(product=product).first()
            reviews = ReviewRating.objects.filter(product=product, status=True)

            products = Product.objects.all()
            related_products = random.sample(list(products), 8)
            data = {
                "product": product,
                "ordered_quantity": ordered_quantity,
                "description": description,
                "reviews": reviews,
                "related_products": related_products
            }
        else:
            return HttpResponse("Không tìm thấy sản phẩm 123")
            # return redirect("store")
    else:
        HttpResponse("Không tìm thấy loại mặt hàng")
        return redirect("store")
    return render(request, "product_detail.html", data)
