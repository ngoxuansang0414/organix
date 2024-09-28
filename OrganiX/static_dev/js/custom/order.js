
$(document).ready(function () {
    cancel_order_btn = document.querySelectorAll('.cancel_order_btn');
    cancel_order_btn.forEach(btn => {
        btn.addEventListener('click', function () {
            alertify.confirm('Hủy đơn hàng', 'Bạn chắc chắn muốn hủy đơn hàng?', function () {
                var order_id = document.getElementById('canceled_order_id').value;
                var token = $('input[name=csrfmiddlewaretoken]').val()
                $.ajax({
                    method: 'POST',
                    url: "orders",
                    data: {
                        'order_id': order_id,
                        csrfmiddlewaretoken: token
                    },
                    success: function (response) {
                        if (response.error) {
                            alertify.error('Đã xảy ra lỗi')
                        }
                        else {
                            window.location.replace("/orders")
                        }
                    }
                })
            },
                function () {
                });
        })
    })
})
