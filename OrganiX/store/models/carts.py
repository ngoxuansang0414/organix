from django.db import models
from .products import Product
from accounts.models import Account
from django.utils import timezone


class Cart(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name="Tài khoản"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Sản phẩm"
    )
    product_qty = models.IntegerField(null=False, blank=False, verbose_name="Số lượng")
    created_at = models.DateTimeField(
        default=timezone.localtime, verbose_name="Ngày tạo"
    )

    class Meta:
        verbose_name_plural = "Giỏ hàng"

    @staticmethod
    def get_cart_by_customer(customer_id):
        return Cart.objects.filter(customer=customer_id)
