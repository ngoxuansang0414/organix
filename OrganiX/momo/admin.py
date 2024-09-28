from django.contrib import admin
from momo.models import PaymentInfo, resultcode


class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "orderId", "transId", "resultCode")


class resultcodeAdmin(admin.ModelAdmin):
    list_display = ("data",)


admin.site.register(PaymentInfo, PaymentInfoAdmin)
admin.site.register(resultcode, resultcodeAdmin)
