$(document).on('submit', '#reset_password', function (e) {
    e.preventDefault();

    $.ajax({
        method: 'POST',
        url: "reset_password",
        data: {
            password: $('#password').val(),
            confirm_password: $('#confirm_password').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            if (data.status == true) {
                alertify.success(data.msg);
                setTimeout(function () {
                    window.location.replace("/accounts/login")
                }, 2000);
            }
            else{
                alertify.error(data)
            }

        },
        error: function (data) {
            alertify.error(data)
        }
    });
});