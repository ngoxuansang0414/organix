$(document).ready(function () {
    $('#increment-btn').click(function (e) {
        e.preventDefault();

        var inc_value = $(this).closest('.product_data').find('#qty-input').val();
        var value = parseInt(inc_value, 10);
        var product_stock = document.getElementById("product_stock").value
        value = isNaN(value) ? 0 : value;
        if (value < product_stock) {
            value++;
            $(this).closest('.product_data').find('#qty-input').val(value);
        }
    });

    $('#decrement-btn').click(function (e) {
        e.preventDefault();

        var dec_value = $(this).closest('.product_data').find('#qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            $(this).closest('.product_data').find('#qty-input').val(value);
        }
    });

    $('#addToCart-btn').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('#prod_id').val();
        var product_qty = $(this).closest('.product_data').find('#qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: 'POST',
            url: '/cart',
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                'add-to-cart': 1,
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
            error: function () {
                alertify.error('Có lỗi xảy ra!')
            }
        })
    });
});
