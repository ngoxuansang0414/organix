from store.models.orders import Order, OrderItem
import requests
from django.http import HttpResponse, JsonResponse
import json
from accounts.models import Address
from vi_address.models import Ward, District, City


# token = '2b6feb98-73fd-11ef-8e53-0a00184fe694'
# shop_id = 194607

token = 'f3629d47-7cc5-11ef-b260-d22cded7e2d0'
shop_id = 5351270

def get_order_province_id(province_name):
    # province_endpoint = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/province"
    province_endpoint = "https://online-gateway.ghn.vn/shiip/public-api/master-data/province"
    response = requests.get(
        province_endpoint,
        headers={"Content-Type": "application/json", "token": token},
    )
    province_name = province_name.replace("-","")
    for i in response.json()["data"]:
        name_ext_list = i.get("NameExtension")
        if name_ext_list:
            if province_name in name_ext_list:
                province_id = i["ProvinceID"]
                break
    # for i in response.json()["data"]:
    #     if province_name == i["ProvinceName"]:
    #         province_id = i["ProvinceID"]
    #         break
    print(province_id)
    return province_id

def get_order_district_id(province_name, district_name):
    province_id = get_order_province_id(province_name.replace("-",""))
    # district_endpoint = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/district"
    district_endpoint = "https://online-gateway.ghn.vn/shiip/public-api/master-data/district"
    data = json.dumps({"province_id": province_id})
    response = requests.get(
        district_endpoint,
        headers={"Content-Type": "application/json", "token": token},
        data=data,
    )

    district_name = district_name.replace("-","")

    for i in response.json()["data"]:
        name_ext_list = i.get("NameExtension")
        if name_ext_list:
            if district_name in name_ext_list:
                district_id = i["DistrictID"]
                break

    # for i in response.json()["data"]:
    #     if district_name == i["DistrictName"]:
    #         district_id = i["DistrictID"]
    #         break
    return district_id

def get_order_ward_id(province_name, district_name, ward_name):
    district_id = get_order_district_id(province_name.replace("-",""), district_name.replace("-",""))
    # ward_endpoint = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/ward?district_id"
    ward_endpoint = "https://online-gateway.ghn.vn/shiip/public-api/master-data/ward?district_id"
    data = json.dumps({"district_id": district_id})
    response = requests.get(
        ward_endpoint,
        headers={"Content-Type": "application/json", "token": token},
        data=data,
    )

    ward_name = ward_name.replace("-","")
    for i in response.json()["data"]:
        name_ext_list = i.get("NameExtension")
        if name_ext_list:
            if ward_name in name_ext_list:
                ward_id = i["WardCode"]
                break

    

    # for i in response.json()["data"]:
    #     if district_name == i["WardName"]:
    #         ward_id = i["WardCode"]
    #         break
    return ward_id

def get_addr(ward_name, district_name, province_name):
    print (f"get_addr: {ward_name}, {district_name}, {province_name}")
    district_id = get_order_district_id(province_name, district_name)
    ward_id = get_order_ward_id(province_name, district_name, ward_name)
    addr_id_list = [district_id, ward_id]
    return addr_id_list

# Tạm tính tiền vận chuyển bằng địa chỉ mặc định của người dùng
def get_estimated_shipping_fee(user_id):
    # endpoint = "https://dev-online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee"
    endpoint = "https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee"
    print(get_available_services("Gia Lâm", "Hà Nội", "Từ Sơn", "Bắc Ninh"))
    service_type_id = 2 # 2 với hàng nhẹ, 5 với hàng nặng
    addr = Address.objects.filter(account=user_id).first()

    tmp = get_addr(Ward.objects.get(pk=addr.ward).name_with_type,
                   District.objects.get(pk=addr.district).name_with_type, 
                   City.objects.get(pk=addr.city).name_with_type)
    to_district_id = tmp[0]
    to_ward_code = tmp[1]
    print(tmp)
    data = {
        
        "service_type_id": 2,
        "to_district_id":to_district_id,
        "to_ward_code":to_ward_code,
        "height":20,
        "length":30,
        "weight":3000,
        "width":40,
        "insurance_value":0,
        "items": [
                {
                    "name": "TEST1",
                    "quantity": 3,
                    "height": 20,
                    "weight": 1000,
                    "length": 30,
                    "width": 40
                }
                    ]
    }

    data = json.dumps(data)

    response = requests.get(
        endpoint,
        headers={"Content-Type": "application/json", "token": token, "shop_id": str(shop_id)},
        data=data,
    )
    print(response.json())
    return response.json()["data"]["total"]


# Tính tiền vận chuyển từ kho mặc định tới địa phương bất kỳ
def get_shipping_order_fee(request):
    # endpoint = "https://dev-online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee"
    endpoint = "https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee"
    ward_id = request.POST.get("ward")
    district_id = request.POST.get("district")
    city_id = request.POST.get("city")
    print(city_id, district_id, ward_id)
    tmp = get_addr(Ward.objects.get(pk=ward_id).slug,
                   District.objects.get(pk=district_id).slug, 
                   City.objects.get(pk=city_id).slug)
    to_district_id = tmp[0]
    to_ward_code = tmp[1]
    print(tmp)
    print(get_available_services("Gia Lâm", "Hà Nội", 
                                 District.objects.get(pk=district_id).slug, 
                                 City.objects.get(pk=city_id).slug))

    data = {
        "service_type_id":2,
        "from_district_id":1703,
        "to_district_id": to_district_id,
        "to_ward_code": to_ward_code,
        "height":20,
        "length":30,
        "weight":3000,
        "width":40,
        "insurance_value":0,
        "items": [
                {
                    "name": "TEST1",
                    "quantity": 3,
                    "height": 20,
                    "weight": 1000,
                    "length": 30,
                    "width": 40
                }
                    ]
    }

    data = json.dumps(data)

    response = requests.get(
        endpoint,
        headers={"Content-Type": "application/json", "token": token, "shop_id": str(shop_id)},
        data=data,
    )

    print(response.json())
    # response.json()["data"]["total"]
    context = response.json()["data"]["total"]

    return JsonResponse({"context": context})


def get_available_services(from_district_name, from_province_name, to_district_name, to_province_name):
    # endpoint = "https://dev-online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/available-services"
    endpoint = "https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/available-services"
    from_district = get_order_district_id(from_province_name, from_district_name)
    to_district = get_order_district_id(to_province_name, to_district_name)
    data = {
        "from_district": from_district,
        "to_district": to_district,
        "shop_id": shop_id
    }

    data = json.dumps(data)
    response = requests.get(
        endpoint,
        headers={"Content-Type": "application/json", "token": token},
        data=data,
    )
    return response.json()["data"]

def update_order(trackno):
    order = Order.objects.filter(trackno=trackno).first()
    preview_endpoint = "https://dev-online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/preview"
    update_order_endpoint = "https://dev-online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/create"
    if order.payment_method == 'cod':
        payment_type_id = 2
    elif order.payment_method == 'momo':
        payment_type_id = 1
    note = order.note
    required_note = 'CHOXEMHANGKHONGTHU'
    return_phone = '0946769390'
    return_address = "Học viện Nông Nghiệp Việt Nam, Thị Trấn Trâu Quỳ, Gia Lâm, Hà Nội"
    from_name = "Ngô Xuân Sáng"
    from_phone = return_phone
    from_address = return_address
    client_order_code = trackno
    from_ward_name = "Thị trấn Trâu Quỳ"
    from_district_name = "Huyện Gia Lâm"
    from_provice_name = "HN"
    to_name = order.name
    to_phone = order.phone
    to_address = order.address
    to_ward_name = order.ward_name
    to_district_name = order.district_name
    to_province_name = order.city_name
    cod_amount = int("tiền thu hộ cho người gửi")
    weight = order.unit
    length = 200
    width = 200
    height = 200
    cod_failed_amount = 2000
    insurance_value = order.total_price
    service_type_id = int(api)
    pick_shift = "Dùng để truyền ca lấy hàng , Sử dụng API Lấy danh sách ca lấy"
    items = [
                {
                    "name":"Áo Polo",
                    "code":"Polo123",
                    "quantity": 1,
                    "price": 200000,
                    "length": 12,
                    "width": 12,
                    "weight": 1200,
                    "height": 12,
                    "category": 
                    {
                        "level1":"Áo"
                    }
                }
                
            ]
    


