$(document).on('submit', '#submitEmail', function (e) {
    e.preventDefault();

    $.ajax({
        method: 'POST',
        url: "resetpassword",
        data: {
            email: $('#email').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
                alertify.success(data);
        },
        error: function (data) {
            alertify.error(data)
        }
    });
});