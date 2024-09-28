from django.db import models
import os
from datetime import datetime
from django.utils import timezone
from store.storage import StaticStorage
from PIL import Image as Img
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from slugify import slugify


def get_file_path(request, filename):
    return os.path.join("image/categories/", filename)


class Category(models.Model):
    slug = models.SlugField(
        default="", max_length=150, null=False, blank=False, help_text="Bỏ trống"
    )
    name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name="Tên loại sản phẩm"
    )
    image = models.ImageField(
        storage=StaticStorage,
        upload_to=get_file_path,
        null=True,
        blank=True,
        verbose_name="Ảnh sản phẩm",
    )
    status = models.BooleanField(
        default=False, help_text="0=Ẩn, 1=Hiện", verbose_name="Hiện sản phẩm"
    )
    created_at = models.DateTimeField(
        default=timezone.localtime, verbose_name="Ngày tạo"
    )

    class Meta:
        verbose_name_plural = "Loại sản phẩm"

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
            self.image = InMemoryUploadedFile(output, "ImageField", "%s.jpg" % self.image.name.split(".")[0], "image/jpeg", "Content-Type: charset=utf-8", None)  # type: ignore
        super(Category, self).save()

    def __str__(self):
        return self.name
