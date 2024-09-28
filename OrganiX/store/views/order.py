from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from accounts.models import Account, Address
from django.views import View
from store.models.products import Product
from store.models.orders import Order, OrderItem
from django.http import HttpResponse, JsonResponse
from momo.models import PaymentInfo
from momo.views import refund, thanks


class OrderView(View):
    def get(self, request):
        status = request.GET.get("status")
        user = request.user
        if status:
            orders = Order.objects.filter(account=user, status=status).order_by(
                "-created_at"
            )
        else:
            orders = Order.objects.filter(account=user).order_by("-created_at")
        for order in orders:
            orderItems = OrderItem.objects.filter(order=order)
            order.orderItems = []
            for orderItem in orderItems:
                orderItem.sub_total = orderItem.price * orderItem.quantity
                order.orderItems.append(orderItem)

        return render(request, "orders.html", {"orders": orders})

    def post(self, request):
        order_id = request.POST.get("order_id")
        canceled_order = Order.objects.filter(
            account=request.user, tracking_no=order_id
        ).first()
        if canceled_order and canceled_order.status == "Đang chờ":
            if canceled_order.payment_method == "momo":
                refund_status = refund(order_id)
                if refund_status != 0:
                    return JsonResponse({"error": "1"})
            Order.return_stock(canceled_order.id, "huy")
            canceled_order.status = "Đã hủy"
            canceled_order.save()
        else:
            return JsonResponse({"error": "1"})

        return redirect("orders")


def orderResult(request, orderId):
    order = Order.objects.filter(tracking_no=orderId).first()
    if request.user.id != order.account_id:
        return redirect("homepage")
    if order.payment_method == "cod":
        return render(request, "thankyou.html")
    elif order.payment_method == "momo":
        data = thanks(orderId)
        return render(request, "thankyou.html", {"data": data})

    return HttpResponse()
