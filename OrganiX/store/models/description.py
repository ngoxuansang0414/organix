from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .products import Product


class Description(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, verbose_name="Sản phẩm"
    )
    certification = models.TextField(
        default="Không rõ", verbose_name="Chứng nhận/Canh tác"
    )
    origin = models.TextField(default="Không rõ", verbose_name="Xuất xứ")
    uses = models.TextField(default="Không rõ", verbose_name="Công dụng")
    instructions_for_use = models.TextField(
        default="Không rõ", verbose_name="Hướng dẫn sử dụng"
    )
    preserving_instruction = models.TextField(
        default="Không rõ", verbose_name="Hướng dẫn bảo quản"
    )
    expiry = models.TextField(default="Không rõ", verbose_name="Hạn sử dụng")

    class Meta:
        verbose_name_plural = "Mô tả sản phẩm"

    @receiver(post_save, sender=Product)
    def create_description(sender, instance, created, **kwargs):
        if created:
            Description.objects.create(product=instance)

    def __str__(self):
        return self.product.name
