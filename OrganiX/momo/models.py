from django.db import models
from store.models.orders import Order

class PaymentInfo(models.Model):
    order = models.CharField(max_length=50)
    resultCode = models.IntegerField(default=0)
    transId = models.CharField(max_length=50)
    refund_status = models.BooleanField(default=False) 

    def __str__(self):
        return self.order

