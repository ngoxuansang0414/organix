$(document).ready(function () {
    $(document).on('click', '.checkout-btn', function (e) {
        e.preventDefault();

        var name = document.getElementsByName('name')[0].value;
        var phone = document.getElementsByName('phone')[0].value;
        var specific_address = document.getElementsByName('specific_address')[0].value;
        var ward = document.getElementsByName('ward')[0].value;
        var district = document.getElementsByName('district')[0].value;
        var city = document.getElementsByName('city')[0].value;
        var note = document.getElementsByName('note')[0].value;
        var payment_method = document.getElementsByName('checked_radio')[0].value;
        var token = $('input[name=csrfmiddlewaretoken]').val();
        var getInforType = document.getElementById("get_infor_type").value;

        $.ajax({
            method: 'POST',
            url: "checkout",
            data: {
                'name': name,
                'phone': phone,
                'specific_address': specific_address,
                'ward': ward,
                'district': district,
                'city': city,
                'note': note,
                'payment_method': payment_method,
                'get_infor_type': getInforType,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                response.messages.forEach(function (msg) {
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
                if (response.Url) {
                    window.location.replace(response.Url)
                }
            },
            error: function (response) {

            }
        })
    });


    $(document).on('click', '.checkout-btn', function (e) {
        e.preventDefault();

    });

    const cityInput = document.getElementById('cities')
    const districtInput = document.getElementById('districts')
    const wardInput = document.getElementById('wards')

    var token = $('input[name=csrfmiddlewaretoken]').val();

    wardInput.addEventListener('change', e => {
        var ward = document.getElementsByName('ward')[0].value;
        var district = document.getElementsByName('district')[0].value;
        var city = document.getElementsByName('city')[0].value;
        $.ajax({
            type: 'POST',
            url: `shipping/fee`,
            data: {
                'ward': ward,
                'district': district,
                'city': city,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response)
            },
            error: function (error) {
                console.log(error)
            }
        })
    })

})