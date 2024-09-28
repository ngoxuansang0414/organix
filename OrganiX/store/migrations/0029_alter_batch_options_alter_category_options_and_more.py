# Generated by Django 4.2.7 on 2024-06-17 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import store.models.categories
import store.models.products
import store.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0028_alter_orderitem_batch"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="batch",
            options={"verbose_name_plural": "Lô sản phẩm"},
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Loại sản phẩm"},
        ),
        migrations.AlterModelOptions(
            name="description",
            options={"verbose_name_plural": "Mô tả sản phẩm"},
        ),
        migrations.AlterModelOptions(
            name="order",
            options={"verbose_name_plural": "Đơn hàng"},
        ),
        migrations.AlterModelOptions(
            name="orderitem",
            options={"verbose_name_plural": "Sản phẩm của đơn hàng"},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name_plural": "Sản phẩm"},
        ),
        migrations.AlterModelOptions(
            name="reviewrating",
            options={"verbose_name_plural": "Đánh giá"},
        ),
        migrations.AlterField(
            model_name="batch",
            name="Product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="store.product",
                verbose_name="Sản phẩm",
            ),
        ),
        migrations.AlterField(
            model_name="batch",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo"),
        ),
        migrations.AlterField(
            model_name="batch",
            name="expiry_date",
            field=models.DateTimeField(
                blank=True, help_text="Bỏ trống", verbose_name="Ngày hết hạn"
            ),
        ),
        migrations.AlterField(
            model_name="batch",
            name="quantity",
            field=models.IntegerField(default=0, verbose_name="Số lượng"),
        ),
        migrations.AlterField(
            model_name="batch",
            name="status",
            field=models.BooleanField(
                default=True,
                help_text="0=Hết hạn, 1=Còn hạn",
                verbose_name="Trạng thái",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.localtime, verbose_name="Ngày tạo"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=store.storage.StaticStorage,
                upload_to=store.models.categories.get_file_path,
                verbose_name="Ảnh sản phẩm",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=50, verbose_name="Tên loại sản phẩm"),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.CharField(default="", help_text="Bỏ trống", max_length=150),
        ),
        migrations.AlterField(
            model_name="category",
            name="status",
            field=models.BooleanField(
                default=False, help_text="0=Ẩn, 1=Hiện", verbose_name="Hiện sản phẩm"
            ),
        ),
        migrations.AlterField(
            model_name="description",
            name="certification",
            field=models.TextField(
                default="Không rõ", verbose_name="Chứng nhận/Canh tác"
            ),
        ),
        migrations.AlterField(
            model_name="description",
            name="expiry",
            field=models.TextField(default="Không rõ", verbose_name="Hạn sử dụng"),
        ),
        migrations.AlterField(
            model_name="description",
            name="instructions_for_use",
            field=models.TextField(
                default="Không rõ", verbose_name="Hướng dẫn sử dụng"
            ),
        ),
        migrations.AlterField(
            model_name="description",
            name="origin",
            field=models.TextField(default="Không rõ", verbose_name="Xuất xứ"),
        ),
        migrations.AlterField(
            model_name="description",
            name="preserving_instruction",
            field=models.TextField(
                default="Không rõ", verbose_name="Hướng dẫn bảo quản"
            ),
        ),
        migrations.AlterField(
            model_name="description",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.product",
                verbose_name="Sản phẩm",
            ),
        ),
        migrations.AlterField(
            model_name="description",
            name="uses",
            field=models.TextField(default="Không rõ", verbose_name="Công dụng"),
        ),
        migrations.AlterField(
            model_name="order",
            name="account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Tài khoản mua",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.CharField(max_length=200, verbose_name="Địa chỉ giao hàng"),
        ),
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo"),
        ),
        migrations.AlterField(
            model_name="order",
            name="name",
            field=models.CharField(max_length=50, verbose_name="Tên người nhận"),
        ),
        migrations.AlterField(
            model_name="order",
            name="note",
            field=models.TextField(blank=True, verbose_name="Ghi chú"),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                max_length=50, verbose_name="Phương thức thanh toán"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="phone",
            field=models.CharField(max_length=10, verbose_name="SĐT người nhận"),
        ),
        migrations.AlterField(
            model_name="order",
            name="processed",
            field=models.BooleanField(
                blank=True, verbose_name="Trạng thái xử lý thanh toán"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Đang chờ", "Pending"),
                    ("Đang giao hàng", "Out For Shipping"),
                    ("Hoàn thành", "Completed"),
                    ("Đã hủy", "Canceled"),
                ],
                default="Đang chờ",
                max_length=100,
                verbose_name="Trạng thái đơn hàng",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.IntegerField(verbose_name="Giá trị đơn hàng"),
        ),
        migrations.AlterField(
            model_name="order",
            name="tracking_no",
            field=models.CharField(
                max_length=150, null=True, verbose_name="Mã vận đơn"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Ngày chỉnh sửa"),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="batch",
            field=models.JSONField(default=dict, verbose_name="Lô hàng"),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="store.order",
                verbose_name="Đơn hàng",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="price",
            field=models.IntegerField(verbose_name="Giá"),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="store.product",
                verbose_name="Sản phẩm",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(verbose_name="Số lượng"),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="store.category",
                verbose_name="Loại sản phẩm",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo"),
        ),
        migrations.AlterField(
            model_name="product",
            name="expiry_period",
            field=models.IntegerField(
                default=0,
                help_text="Tính bằng 'ngày'",
                verbose_name="Hết hạn trong vòng",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=store.storage.StaticStorage,
                upload_to=store.models.products.get_file_path,
                verbose_name="Ảnh sản phẩm",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Ngày chỉnh sửa"),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=150, verbose_name="Tên sản phẩm"),
        ),
        migrations.AlterField(
            model_name="product",
            name="original_price",
            field=models.IntegerField(default=0, verbose_name="Giá nhập"),
        ),
        migrations.AlterField(
            model_name="product",
            name="sell_price",
            field=models.IntegerField(default=0, verbose_name="Giá bán"),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, help_text="Bỏ trống", max_length=150),
        ),
        migrations.AlterField(
            model_name="product",
            name="status",
            field=models.BooleanField(
                default=True, help_text="0=Ẩn, 1=Hiện", verbose_name="Hiện sản phẩm"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="unit",
            field=models.CharField(
                default="sản phẩm", max_length=30, verbose_name="Khối lượng"
            ),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo"),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="store.order",
                verbose_name="Đơn hàng",
            ),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="store.product",
                verbose_name="Sản phẩm",
            ),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="rating",
            field=models.FloatField(verbose_name="Số sao"),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="review",
            field=models.TextField(blank=True, max_length=500, verbose_name="Đánh giá"),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="status",
            field=models.BooleanField(default=True, verbose_name="Trạng thái"),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="subject",
            field=models.CharField(blank=True, max_length=100, verbose_name="Chủ đề"),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Ngày chỉnh sửa"),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Tài khoản mua",
            ),
        ),
    ]
