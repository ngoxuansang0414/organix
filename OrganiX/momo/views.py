from django.shortcuts import render
from django.http.response import HttpResponse
from momo.models import PaymentInfo
from store.models.carts import Cart
from store.models.orders import Order, OrderItem
from store.models.products import Product
from momo.payment_sign import paymennt_sign
from momo.refund_sign import refund_sign
import json
import requests

def thanks(request):
    amount = request.GET.get('amount')
    extraData = request.GET.get('extraData')
    orderId = request.GET.get('orderId')
    orderType = request.GET.get('orderType')
    partnerCode = request.GET.get('partnerCode')
    payType = request.GET.get('payType')
    requestId = request.GET.get('requestId')
    responseTime = request.GET.get('responseTime')
    resultCode = request.GET.get('resultCode')
    transId = request.GET.get('transId')
    
    signature = request.GET.get('signature')
    
    
    
    if resultCode:
        resign = paymennt_sign(amount, extraData, orderId, partnerCode, payType, requestId, responseTime, resultCode, transId, orderType)
        signature_check = (signature == resign)
        check_payment = PaymentInfo.objects.get(order = orderId)
        if not check_payment:
            resultCode = "99"
            print("truong hop bi loi khong tim thay giao dich")
        #truong hop thanh toan bi loi khong xac dinh
        elif check_payment and (resultCode != '0' and resultCode != '1006'):
            failed_order = Order.objects.get(tracking_no = orderId)       
            canceledItems = OrderItem.objects.filter(order = failed_order)
            for canceledItem in canceledItems:
                canceledProduct = Product.objects.get(pk = canceledItem.product.id)
                canceledProduct.stock += canceledItem.quantity
                canceledProduct.save()
                if Cart.objects.get(account = request.user, product = canceledProduct.pk):
                    oldCart = Cart.objects.get(account = request.user, product = canceledProduct.pk)
                    if oldCart.product_qty + canceledItem.quantity <= canceledProduct.stock:
                        oldCart.product_qty += canceledItem.quantity
                        oldCart.save()
                elif canceledItem.product.stock > canceledItem.quantity:
                    oldCart = Cart.objects.get(account = request.user)
                    oldCart.create(product = canceledItem.product.pk, product_qty = canceledItem.quantity)
                    oldCart.save()
            failed_order.delete()
            check_payment.resultCode = resultCode
            check_payment.save()
            print("truong hop thanh toan bi loi khong xac dinh")
        #truong hop thanh toan bi tu choi boi nguoi dung
        elif check_payment and resultCode == '1006' and signature_check:
            if Order.objects.get(tracking_no = orderId):
                failed_order = Order.objects.get(tracking_no = orderId)
                print('Tim thay don hang')  
                canceledItems = OrderItem.objects.filter(order = failed_order)
                for canceledItem in canceledItems:
                    canceledProduct = Product.objects.get(pk = canceledItem.product.id)
                    canceledProduct.stock += canceledItem.quantity
                    canceledProduct.save()
                    print('Them lai vao kho hang thanh cong')
                    canceledItem.delete()
                    print('xoa order item thanh cong')
                failed_order.delete()
                print('xoa don hang bi tu choi thanh toan thanh cong')
                check_payment.resultCode = resultCode
                check_payment.save()
                print('truong hop thanh toan bi tu choi boi nguoi dung')
        
        #truong hop thanh cong
        check_payment.transId = transId
        check_payment.save()
    
    return render (request, 'thankyou.html', {'resultCode': resultCode})


def refund(orderId, amount, transId):
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/refund"
    partnerCode = "MOMO"
    amount = str(amount)
    description = f"Hoan tien don hang #{orderId}"
    orderId = f"refund_{orderId}"
    requestId = orderId
    lang = "vi"
    
    signature = refund_sign(amount, description, orderId, partnerCode, requestId, transId)

    data = {
        "partnerCode": partnerCode,
        "orderId": orderId,
        "requestId": requestId,
        "amount": amount,
        "transId": transId,
        "lang": lang,
        "description": description,
        "signature": signature
    }

    data = json.dumps(data)

    clen = len(data)
    response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})
    return (response.json()['resultCode'])