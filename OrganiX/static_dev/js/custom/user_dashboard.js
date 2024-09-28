  $(document).ready(function () {
    $(document).on('click', '.save-btn', function (e) {
      e.preventDefault();

      var email = document.getElementsByName('email')[0].value;
      var name = document.getElementsByName('name')[0].value;
      var phone = document.getElementsByName('phone')[0].value;
      var gender = document.getElementsByName('gender')[0].value;
      var specific_address = document.getElementsByName('specific_address')[0].value;
      var ward = document.getElementsByName('ward')[0].value;
      var district = document.getElementsByName('district')[0].value;
      var city = document.getElementsByName('city')[0].value;
      var token = $('input[name=csrfmiddlewaretoken]').val();

      $.ajax({
        method: 'POST',
        url: "/accounts/profile",
        data: {
          'email': email,
          'name': name,
          'phone': phone,
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
          if (response.redirect) {
            setTimeout(function () {
              window.location.replace("/accounts/profile")
            }, 2000);
          }
        },
        error: function () {
          alertify.error('Có lỗi xảy ra!')
        }
      })
    });

    $(document).on('click', '.edit-btn', function () {

      $('.editable').prop('disabled', false);
      $('#specific_address').prop('hidden', false);
      $('#wards-data-box').prop('hidden', false);
      $('#districts-data-box').prop('hidden', false);
      $('#cities-data-box').prop('hidden', false);
      $('#address').prop('hidden', true);
    });
  })


  $(document).on('submit', '#change_password', function (e) {
    e.preventDefault();
    $.ajax({
      method: 'POST',
      url: "/accounts/change_password",
      data: {
        old_password: $('#old_password').val(),
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
      error: function () {
        alertify.error('Có lỗi xảy ra!')
      }
    });
  });


