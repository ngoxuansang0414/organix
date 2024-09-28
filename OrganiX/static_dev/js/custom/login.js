$(document).on('submit', '#login', function (e) {
    e.preventDefault();
    $.ajax({
        method: 'POST',
        url: 'login',
        data: {
            email: $('#email').val(),
            password: $('#password').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
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
            if (response.redirect) {
                window.location.replace("/store")
            }

        },
        error: function () {
            alertify.error('Có lỗi xảy ra!')
        }
    });
});