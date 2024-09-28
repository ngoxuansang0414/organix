from django.db import models
from .categories import Category
import os
from datetime import datetime, timedelta
from django.utils import timezone
from PIL import Image as Img
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from slugify import slugify
import random
from django.db.models import Sum, Q
from store.storage import StaticStorage


def get_file_path(request, filename):
    return os.path.join("image/products/", filename)


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Loại sản phẩm"
    )
    slug = models.SlugField(
        max_length=150, null=False, blank=True, help_text="Bỏ trống"
    )
    name = models.CharField(
        max_length=150, null=False, blank=False, verbose_name="Tên sản phẩm"
    )
    unit = models.IntegerField(
        null=False,
        blank=False,
        verbose_name="Khối lượng (gram)",
    )
    original_price = models.IntegerField(
        default=0, null=False, blank=False, verbose_name="Giá nhập"
    )
    sell_price = models.IntegerField(
        default=0, null=False, blank=False, verbose_name="Giá bán"
    )
    expiry_period = models.IntegerField(
        default=0,
        null=False,
        help_text="Tính bằng 'ngày'",
        verbose_name="Hết hạn trong vòng",
    )
    image = models.ImageField(
        storage=StaticStorage,
        upload_to=get_file_path,
        null=True,
        blank=True,
        verbose_name="Ảnh sản phẩm",
    )
    status = models.BooleanField(
        default=True, help_text="0=Ẩn, 1=Hiện", verbose_name="Hiện sản phẩm"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Ngày chỉnh sửa")

    class Meta:
        verbose_name_plural = "Sản phẩm"

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name, only_ascii=True)
        if self.image:
            img = Img.open(io.BytesIO(self.image.read()))
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.thumbnail((400, 420), Img.Resampling.LANCZOS)  # (width,height)
            output = io.BytesIO()
            img.save(output, format="JPEG")
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output,
                "ImageField",
                "%s.jpg" % self.image.name.split(".")[0],
                "image/jpeg",
                "Content-Type: charset=utf-8",
                None,
            )
        super(Product, self).save()

    @staticmethod
    def get_stock_quantity(product):
        # stock = Product.objects.filter(Q(id=product.id) & Q(batch__expiry_date__gt=datetime.now())).aggregate(stock=Sum("batch__stock__quantity", default=0))
        stock = Product.objects.filter(
            Q(id=product.id) & Q(batch__status=True)
        ).aggregate(stock=Sum("batch__quantity", default=0))
        return stock["stock"]
    
    def product_count(category_id):
        count = Product.objects.filter(category=category_id, status=1).count()
        return count


class Batch(models.Model):
    id = models.CharField(primary_key=True, max_length=20, editable=False)
    Product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Sản phẩm"
    )
    quantity = models.IntegerField(default=0, null=False, verbose_name="Số lượng")
    expiry_date = models.DateTimeField(
        blank=True, help_text="Bỏ trống", verbose_name="Ngày hết hạn"
    )
    status = models.BooleanField(
        default=True, help_text="0=Hết hạn, 1=Còn hạn", verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name_plural = "Lô sản phẩm"

    def save(self):
        current_date = datetime.now()
        batch = Batch.objects.filter(pk=self.id).first()
        if batch:
            super().save()
        else:
            id = f"{current_date.strftime('%d%m%y')}_{self.Product.pk}_{str(random.randint(000, 999))}"
            while Batch.objects.filter(pk=id) is None:
                id = f"{current_date.strftime('%d%m%y')}_{self.Product.pk}_{str(random.randint(000, 999))}"
            self.id = id
            self.expiry_date = current_date + timedelta(days=self.Product.expiry_period)
            print(f"{id}, {self.id}, {self.expiry_date}")
            super().save()

    def __str__(self):
        return f"{self.Product.name} - Lô {self.id}"
