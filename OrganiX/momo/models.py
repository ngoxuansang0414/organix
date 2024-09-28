from django.db import models
from store.models.orders import Order


class PaymentInfo(models.Model):
    partnerCode = models.TextField(blank=True)
    orderId = models.TextField(blank=True, verbose_name="Mã vận đơn")
    requestId = models.TextField(blank=True)
    amount = models.TextField(blank=True)
    orderInfo = models.TextField(blank=True)
    orderType = models.TextField(blank=True)
    transId = models.TextField(blank=True)
    resultCode = models.TextField(blank=True)
    message = models.TextField(blank=True)
    payType = models.TextField(blank=True)
    responseTime = models.TextField(blank=True)
    extraData = models.TextField(blank=True)
    signature = models.TextField(blank=True)

    def __str__(self):
        return self.orderId


class resultcode(models.Model):
    data = models.JSONField(default=dict)
