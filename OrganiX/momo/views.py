from django.shortcuts import render
from django.http.response import HttpResponse
from momo.models import PaymentInfo, resultcode
from store.models.carts import Cart
from store.models.orders import Order, OrderItem
from store.models.products import Product
from momo.payment_sign import paymennt_sign, check_paymennt
from momo.refund_sign import refund_sign
import json
import requests
from django.views.decorators.csrf import csrf_exempt
import urllib.parse


def thanks(orderId):
    # amount = request.GET.get("amount")
    # extraData = request.GET.get("extraData")
    # orderId = request.GET.get("orderId")
    # orderType = request.GET.get("orderType")
    # partnerCode = request.GET.get("partnerCode")
    # payType = request.GET.get("payType")
    # requestId = request.GET.get("requestId")
    # responseTime = request.GET.get("responseTime")
    # resultCode = request.GET.get("resultCode")
    # transId = request.GET.get("transId")
    # signature = request.GET.get("signature")
    # # orderInfo
    # # message
    check_payment = PaymentInfo.objects.filter(orderId=orderId).first()
    resultCode = str(check_payment.resultCode)
    errorCodeTable = resultcode.objects.filter(id=1).first().data
    # truong hop bi loi phia doi tac
    message = errorCodeTable[resultCode]
    order_processed = Order.objects.filter(tracking_no=orderId).first()
    if order_processed.processed:
        data = {"resultCode": resultCode, "message": message}
        print("don online da xu ly")
        return data
    else:
        if not check_payment:
            resultCode = "99"
            print("truong hop bi loi khong tim thay giao dich phia cua hang")
        # truong hop thanh toan that bai
        elif check_payment and resultCode != "0":
            # truong hop thanh toan bi tu choi boi nguoi dung
            if resultCode == "1006":
                Order.return_stock(order_processed.id, "huy")
                order_processed.status = "Đã hủy"
            elif resultCode == "9000":
                pass
        order_processed.processed = True
        order_processed.save()
        data = {"resultCode": resultCode, "message": message}

    return data


@csrf_exempt
def ipn(request):
    if request.method == "POST":
        data = json.loads(request.body)
        partnerCode = data["partnerCode"]
        orderId = data["orderId"]
        requestId = data["requestId"]
        amount = str(data["amount"])
        orderInfo = data["orderInfo"]
        orderType = data["orderType"]
        transId = str(data["transId"])
        resultCode = str(data["resultCode"])
        message = data["message"]
        payType = data["payType"]
        responseTime = str(data["responseTime"])
        extraData = data["extraData"]
        signature = data["signature"]
        resign = check_paymennt(
            amount,
            extraData,
            message,
            orderId,
            orderInfo,
            orderType,
            partnerCode,
            payType,
            requestId,
            responseTime,
            resultCode,
            transId,
        )
        if resign == signature:
            PaymentInfo.objects.filter(orderId=orderId).update(
                amount=amount,
                extraData=extraData,
                message=message,
                orderInfo=orderInfo,
                orderType=orderType,
                partnerCode=partnerCode,
                payType=payType,
                requestId=requestId,
                responseTime=responseTime,
                resultCode=resultCode,
                transId=transId,
                signature=signature,
            )
            thanks(orderId)
    return HttpResponse(status=200)


def refund(orderId):
    info = PaymentInfo.objects.filter(orderId=orderId).first()
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/refund"
    partnerCode = "MOMO"
    description = f"Hoan tien don hang #{orderId}"
    orderId = f"refund_{orderId}"
    requestId = orderId
    lang = "vi"
    amount = info.amount
    transId = info.transId
    signature = refund_sign(
        amount, description, orderId, partnerCode, requestId, transId
    )

    data = {
        "partnerCode": partnerCode,
        "orderId": orderId,
        "requestId": requestId,
        "amount": amount,
        "transId": transId,
        "lang": lang,
        "description": description,
        "signature": signature,
    }

    data = json.dumps(data)

    clen = len(data)
    response = requests.post(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json", "Content-Length": str(clen)},
    )
    return response.json()["resultCode"]
