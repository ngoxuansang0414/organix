from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Address


class AccountAdmin(UserAdmin):
    list_display = ('email', 'name', 'phone', 'gender', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'name')   # Các trường có gắn link dẫn đến trang detail
    readonly_fields = ('last_login', 'date_joined')     # Chỉ cho phép đọc
    ordering = ('-date_joined',)     # Sắp xếp theo chiều ngược

    # Bắt buộc phải khai báo
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class AddressAdmin(admin.ModelAdmin):
    list_display = ('account', 'specific_address', 'ward', 'district', 'city')
    


admin.site.register(Account, AccountAdmin)
admin.site.register(Address, AddressAdmin)
