from django.db import models
from .products import Product
from accounts.models import Account
from django.utils import timezone
from store.models.products import Batch


class Order(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name="Tài khoản mua"
    )
    name = models.CharField(max_length=50, null=False, verbose_name="Tên người nhận")
    phone = models.CharField(max_length=10, null=False, verbose_name="SĐT người nhận")
    address = models.CharField(
        max_length=200, null=False, verbose_name="Địa chỉ giao hàng"
    )
    city_name = models.CharField(max_length=100, null=False, verbose_name="Tỉnh/Thành phố")
    district_name = models.CharField(max_length=100, null=False, verbose_name="Quận/Huyện")
    ward_name = models.CharField(max_length=100, null=False, verbose_name="Xã/Phường")
    total_price = models.IntegerField(null=False, verbose_name="Giá trị đơn hàng")
    payment_method = models.CharField(
        max_length=50, null=False, verbose_name="Phương thức thanh toán"
    )
    order_status = (
        ("Đang chờ", "Pending"),
        ("Đang giao hàng", "Out For Shipping"),
        ("Hoàn thành", "Completed"),
        ("Đã hủy", "Canceled"),
    )
    status = models.CharField(
        max_length=100,
        choices=order_status,
        default="Đang chờ",
        verbose_name="Trạng thái đơn hàng",
    )
    note = models.TextField(blank=True, verbose_name="Ghi chú")
    tracking_no = models.CharField(max_length=150, null=True, verbose_name="Mã vận đơn")
    processed = models.BooleanField(
        blank=True, verbose_name="Trạng thái xử lý thanh toán"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày chỉnh sửa")

    class Meta:
        verbose_name_plural = "Đơn hàng"

    def __str__(self):
        return f"{self.id} - {self.tracking_no}"

    @staticmethod
    def return_stock(order_id, return_type):
        canceledItems = OrderItem.objects.filter(order=order_id)
        if return_type == "huy":
            for canceledItem in canceledItems:
                for key, value in canceledItem.batch.items():
                    canceled_batch = Batch.objects.filter(id=key).first()
                    temp = canceled_batch.quantity + value
                    canceled_batch = Batch.objects.filter(id=key).update(quantity=temp)
                    print("Them lai san pham huy vao kho hang thanh cong")
        elif return_type == "loi":
            for canceledItem in canceledItems:
                for key, value in canceledItem.batch.items():
                    canceled_batch = Batch.objects.filter(id=key).first()
                    temp = canceled_batch.quantity + value
                    canceled_batch = Batch.objects.filter(id=key).update(quantity=temp)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Đơn hàng")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Sản phẩm"
    )
    batch = models.JSONField(default=dict, verbose_name="Lô hàng")
    price = models.IntegerField(null=False, verbose_name="Giá")
    quantity = models.IntegerField(null=False, verbose_name="Số lượng")

    class Meta:
        verbose_name_plural = "Sản phẩm của đơn hàng"
