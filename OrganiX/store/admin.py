from django.contrib import admin
from store.models.categories import Category
from store.models.orders import Order, OrderItem
from store.models.products import Product
from store.models.description import Description
from store.models.carts import Cart
from store.models.reviewrating import ReviewRating
from datetime import datetime, timedelta

from django.db.models import Count, Sum, F, Q
from django.shortcuts import render


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "tracking_no",
        "name",
        "total_price",
        "payment_method",
        "created_at",
        "updated_at",
        "status",
    ]
    list_filter = ["account", "status"]
    search_fields = ["account", "address", "phone"]

    def analytics(self, request):
        order_count = Order.objects.count()

        order_status_percentage_data = list(
            Order.objects.values_list("status")
            .annotate(percentage=100 * Count("status") / float(order_count))
            .order_by("-percentage")
        )
        status = [x[0] for x in order_status_percentage_data]
        status_percentage = [round(x[1], 2) for x in order_status_percentage_data]

        now = datetime.now()
        month_list = []
        profit_list = []
        cost_list = []
        for i in range(60, -30, -30):
            time = now - timedelta(days=i)
            month_time = time.month
            year_time = time.year

            completed_order = Order.objects.filter(
                Q(created_at__year=year_time) & Q(created_at__month=month_time),
                status="Hoàn thành",
            )
            revenue = completed_order.aggregate(revenue=Sum("total_price"))
            profit = completed_order.aggregate(
                profit=Sum(
                    F("orderitem__quantity") * F("orderitem__product__sale_price")
                    - F("orderitem__quantity") * F("orderitem__product__original_price")
                )
            )
            if revenue["revenue"] is None:
                # profit_percentage = 0
                revenue = 0
                profit = 0
            else:
                # profit_percentage = round(100*float(profit['profit'])/float(revenue['revenue']), 2)
                revenue = revenue["revenue"]
                profit = profit["profit"]

            month_list.append(f"Tháng {month_time}")
            profit_list.append(profit)
            cost_list.append(revenue - profit)
        print(cost_list)
        return render(
            request,
            "analytics/orders.html",
            {
                "status": status,
                "percentage": status_percentage,
                "profit_list": profit_list,
                "cost_list": cost_list,
                "month_list": month_list,
                "title": "Thống kê đơn hàng",
            },
        )

    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path

        custom_urls = [
            path("analytics/", self.analytics),
        ]
        return custom_urls + urls


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "price", "quantity"]
    search_fields = ["order__tracking_no"]
    list_filter = ["order__status"]


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "original_price",
        "sale_price",
        "category",
        "created_at",
        "modified_at",
    ]
    list_filter = ["category"]
    search_fields = ["name"]
    readonly_fields = ("modified_at", "created_at")

    def analytics(self, request):
        hot_product = Product.objects.filter(orderitem__order__status="Hoàn thành")
        hot_product = list(
            hot_product.values_list("name")
            .annotate(product_selled=Sum("orderitem__quantity"))
            .order_by("-product_selled")
        )
        products = [x[0] for x in hot_product[:5]]
        data = [x[1] for x in hot_product[:5]]
        return render(
            request,
            "analytics/products.html",
            {"products": products, "data": data, "title": "Sản phẩm bán chạy"},
        )

    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path

        custom_urls = [
            path("analytics/", self.analytics),
        ]
        return custom_urls + urls


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ["product"]
    search_fields = ["product__name"]


class CartAdmin(admin.ModelAdmin):
    list_display = ("account", "product", "product_qty", "created_at")
    readonly_fields = ["created_at"]
    search_fields = ["account__email", "account__name"]
    list_filter = ["account"]


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "rating", "status"]
    list_filter = ["rating", "user__email", "product__category__name"]
    search_fields = ["user__email"]

    def analytics(self, request):
        rating_data = []
        for i in range(1, 6):
            rating_count = ReviewRating.objects.filter(rating=i).count()
            rating_data.append(rating_count)

        return render(
            request,
            "analytics/rating.html",
            {"rating_data": rating_data, "title": "Thống kê tỉ lệ đánh giá"},
        )

    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path

        custom_urls = [
            path("analytics/", self.analytics),
        ]
        return custom_urls + urls


admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Description, DescriptionAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
