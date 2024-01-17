from django.db import models
from .products import Product
from accounts.models import Account
from django.utils import timezone

class Cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.localtime)

    @staticmethod
    def get_cart_by_customer(customer_id):
        return Cart.objects.filter(customer=customer_id)