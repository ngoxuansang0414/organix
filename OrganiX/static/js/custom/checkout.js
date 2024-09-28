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
                if (response.Url) {
                    window.location.replace(response.Url)
                }
                else if (response.error) {
                    alertify.error(response.error)
                }
                else {
                    alertify.success(response);
                    setTimeout(function () {
                        window.location.replace("/momo/thanks")
                    }, 2000);
                }

            },
            error: function (response) {

            }
        })
    });

})