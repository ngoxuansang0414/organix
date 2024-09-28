from django.db import models
from store.models.products import Product
from accounts.models import Account
from store.models.orders import Order


class ReviewRating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Sản phẩm"
    )
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name="Tài khoản mua"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Đơn hàng")
    subject = models.CharField(max_length=100, blank=True, verbose_name="Chủ đề")
    review = models.TextField(max_length=500, blank=True, verbose_name="Đánh giá")
    rating = models.FloatField(verbose_name="Số sao")
    status = models.BooleanField(default=True, verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày chỉnh sửa")

    class Meta:
        verbose_name_plural = "Đánh giá"

    def __str__(self):
        return self.subject
