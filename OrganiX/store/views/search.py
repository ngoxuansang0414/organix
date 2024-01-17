from store.models.products import Product
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
class SearchView(View):
    def get(self, request):
        products = Product.objects.filter(status=0).values_list('name', flat=True)
        productsList = list(products)
        return JsonResponse(productsList, safe=False)
    
    def post(self, request):
        searchedterm = request.POST.get('product-searched')
        if searchedterm == '':
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searchedterm).first()
            if product:
                return redirect("store/"+product.category.slug+"/"+product.slug)
            else:
                return redirect(request.META.get('HTTP_REFERER'))