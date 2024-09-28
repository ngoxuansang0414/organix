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
    var confirm_password = document.getElementsByName("confirm_password")[0].value;
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
            'confirm_password': confirm_password,
            'gender': gender,
            'specific_address': specific_address,
            'ward': ward,
            'district': district,
            'city': city,
            csrfmiddlewaretoken: token
        },
        success: function (response) {
            response.messages.forEach(function(msg) {
                if (msg.level === 'success') {
                    alertify.success(msg.message);
                } else if (msg.level === 'error') {
                    alertify.error(msg.message);
                } else if (msg.level === 'warning') {
                    alertify.warning(msg.message);
                } else {
                    alertify.message(msg.message);  
                }
              });
        },
        error: function (data) {
            alertify.error('Có lỗi xảy ra!')
        }
    });
});


function showTooltip() {
    const tooltip = document.getElementById('tooltip');
    tooltip.style.display = 'block';
}

function hideTooltip() {
    const tooltip = document.getElementById('tooltip');
    tooltip.style.display = 'none';
}