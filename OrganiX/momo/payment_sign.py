import hmac
import hashlib

def paymennt_sign(amount, extraData, orderId, partnerCode, payType, requestId, responseTime, resultCode, transId, orderType):
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    if resultCode == '0':
        message = 'Thành công.'
    elif resultCode == '1006':
        message = 'Giao dịch bị từ chối bởi người dùng.'
    orderInfo = f"Thanh toan don hang #{orderId}"
    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&message=" + message + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&orderType=" + orderType + "&partnerCode=" + partnerCode +  "&payType=" + payType + "&requestId=" + requestId + "&responseTime=" + responseTime + "&resultCode=" + resultCode + "&transId=" + transId
    rawSignature.encode(encoding='utf-8', errors='strict')
    h = hmac.new(bytes(secretKey, 'utf-8'), bytes(rawSignature, 'utf-8'), hashlib.sha256)
    signature = h.hexdigest()
    #print("--------------------SIGNATURE----------------")
    print(signature)
    return signature