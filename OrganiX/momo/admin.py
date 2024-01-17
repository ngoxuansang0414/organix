from django.contrib import admin
from momo.models import PaymentInfo

class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('order', 'resultCode')

admin.site.register(PaymentInfo, PaymentInfoAdmin)