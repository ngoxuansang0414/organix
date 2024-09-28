$(document).on('submit', '#signup', function (e) {
    e.preventDefault();

    var gender_radio = document.getElementsByName('gender');
    for (i = 0; i < gender_radio.length; i++) {
        if (gender_radio[i].checked) {
            var gender = gender_radio[i].value;
        }
    }
    
    var email = document.getElementsByName("email")[0].value;
    var phone = document.getElementsByName("phone")[0].value;
    var name = document.getElementsByName("name")[0].value;
    var password = document.getElementsByName("password")[0].value;
    var specific_address = document.getElementsByName("specific_address")[0].value;
    var ward = document.getElementsByName("ward")[0].value;
    var district = document.getElementsByName("district")[0].value;
    var city = document.getElementsByName("city")[0].value;
    var token = $('input[name=csrfmiddlewaretoken]').val();



    $.ajax({
        method: 'POST',
        url: "signup",
        data: {
            'email': email,
            'phone': phone,
            'name': name,
            'password': password,
            'gender': gender,
            'specific_address': specific_address,
            'ward': ward,
            'district': district,
            'city': city,
            csrfmiddlewaretoken: token
        },
        success: function (data) {
            if (data == 'Tạo tài khoản thành công!') {
                alertify.success(data);

                setTimeout(function () {
                    window.location.replace("/accounts/login")
                }, 2000);
            }
            else {
                alertify.error(data)
            };
        },
        error: function (data) {
            alertify.error('Có lỗi xảy ra!')
        }
    });
});


$(document).ready(function(){
    var canDismiss = false;
    
    var notification = alertify.warning('Mật khẩu phải dài từ 8 ký tự, trong đó có: ít nhất 1 chữ viết hoa, 1 ký tự số và 1 ký tự đặc biệt')
    notification.ondismiss = function(){
        return canDismiss;
    };
    setTimeout(function(){ canDismiss = true;}, 5000);
})