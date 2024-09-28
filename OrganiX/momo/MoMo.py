import json
import urllib.request
import urllib
import uuid
import requests
import hmac
import hashlib
from momo.models import PaymentInfo
from django.contrib.sites.shortcuts import get_current_site


def payWithMoMo(request, orderId, amount):
    # parameters send to MoMo get get payUrl
    current_site = get_current_site(request=request)
    print(current_site)
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = f"Thanh toan don hang #{orderId}"
    # redirectUrl = request.build_absolute_uri('/momo/thanks')
    # ipnUrl = request.build_absolute_uri('/momo/ipn')
    redirectUrl = f"http://ngoxuansang0414.mercusysddns.com/order/result/{orderId}"
    ipnUrl = "http://ngoxuansang0414.mercusysddns.com/momo/ipn"
    amount = str(amount)
    # orderId = str(uuid.uuid4())
    # requestId = str(uuid.uuid4())
    orderId = orderId
    requestId = orderId
    requestType = "captureWallet"
    extraData = ""  # pass empty value or Encode base64 JsonString

    # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
    # &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
    # &requestType=$requestType
    rawSignature = (
        "accessKey="
        + accessKey
        + "&amount="
        + amount
        + "&extraData="
        + extraData
        + "&ipnUrl="
        + ipnUrl
        + "&orderId="
        + orderId
        + "&orderInfo="
        + orderInfo
        + "&partnerCode="
        + partnerCode
        + "&redirectUrl="
        + redirectUrl
        + "&requestId="
        + requestId
        + "&requestType="
        + requestType
    )

    # puts raw signature
    # print("--------------------RAW SIGNATURE----------------")

    h = hmac.new(
        bytes(secretKey, "ascii"), bytes(rawSignature, "ascii"), hashlib.sha256
    )
    signature = h.hexdigest()
    # print("--------------------SIGNATURE----------------")
    # json object send to MoMo endpoint

    data = {
        "partnerCode": partnerCode,
        "partnerName": "Test",
        "storeId": "MomoTestStore",
        "requestId": requestId,
        "amount": amount,
        "orderId": orderId,
        "orderInfo": orderInfo,
        "redirectUrl": redirectUrl,
        "ipnUrl": ipnUrl,
        "lang": "vi",
        "extraData": extraData,
        "requestType": requestType,
        "signature": signature,
    }

    new_momo_payment = PaymentInfo()
    new_momo_payment.orderId = orderId
    new_momo_payment.save()
    # print("--------------------JSON REQUEST----------------\n")
    data = json.dumps(data)

    clen = len(data)
    response = requests.post(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json", "Content-Length": str(clen)},
    )

    # f.close()
    # print("--------------------JSON response----------------\n")

    return response.json()["payUrl"]
