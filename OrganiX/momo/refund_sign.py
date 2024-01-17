import hmac
import hashlib

def refund_sign( amount, description, orderId, partnerCode, requestId, transId):
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"

    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&description=" + description +  "&orderId=" + orderId + "&partnerCode=" + partnerCode + "&requestId=" + requestId + "&transId=" + transId
    rawSignature.encode(encoding='utf-8', errors='strict')
    h = hmac.new(bytes(secretKey, 'utf-8'), bytes(rawSignature, 'utf-8'), hashlib.sha256)
    signature = h.hexdigest()
    #print("--------------------SIGNATURE----------------")
    print(signature)
    return signature