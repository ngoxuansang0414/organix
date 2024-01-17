from django.db import models
from .products import Product
from accounts.models import Account
from django.utils import timezone

class Order(models.Model):
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=50, null=False)
	phone = models.CharField(max_length=10, null=False)
	address = models.CharField(max_length=200, null=False)
	total_price = models.IntegerField(null=False)
	payment_method = models.CharField(max_length=50, null=False)
	order_status = (
		('Đang chờ', 'Pending'),
		('Đang giao hàng', 'Out For Shipping'),
		('Hoàn thành', 'Completed'),
		('Đã hủy', 'Canceled')	
	)
	status = models.CharField(max_length=100, choices=order_status, default='Đang chờ')
	note = models.TextField(null=True)
	tracking_no = models.CharField(max_length=150, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	
	def __str__(self):
		return f'{self.id} - {self.tracking_no}'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	price = models.IntegerField(null=False)
	quantity = models.IntegerField(null=False)



