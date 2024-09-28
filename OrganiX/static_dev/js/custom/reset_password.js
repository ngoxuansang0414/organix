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
        success: function (response) {
            response.messages.forEach(function(msg) {
              if (msg.level === 'success') {
                alertify.success(msg.message);
                setTimeout(function () {
                  $.ajax({
                    type: "GET",
                    url: "/accounts/logout"
                  });
                  window.location.replace("/accounts/login")
                }, 2000);
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
            alertify.error('Có lỗi xảy ra')
        }
    });
});