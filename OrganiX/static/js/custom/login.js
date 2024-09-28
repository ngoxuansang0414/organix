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
            $('.messages').load(location.href + ' .messages')
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            if (response.redirect == true) {
                setTimeout(function () {
                    window.location.replace("/store")
                }, 2000);
            }

        },
        error: function (response) {
        }
    });
});