$(document).ready(function() {
  $(document).on('click', '.increment-btn', function(e) {
    e.preventDefault();

    var inc_value = $(this).closest('.product_data').find('#qty-input').val();
    var product_avail = $(this).closest('.product_data').find('#product_avail').val();
    var value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;
    if (value < product_avail) {
      value++;
      $(this).closest('.product_data').find('#qty-input').val(value);
    }

    var product_qty = $(this).closest('.product_data').find('#qty-input').val();     
  });

  $(document).on('click', '.decrement-btn', function(e) {
    e.preventDefault();

    var dec_value = $(this).closest('.product_data').find('#qty-input').val();
    var value = parseInt(dec_value, 10);
    value = isNaN(value) ? 0 : value;
    if (value > 1) {
      value--;
      $(this).closest('.product_data').find('#qty-input').val(value);
    }
  });

  $(document).on('click', '.changeQuantity', function(e){
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var product_qty = $(this).closest('.product_data').find('#qty-input').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
      method: 'POST',
      url: "cart",
      data: {
        'product_id': product_id,
        'product_qty': product_qty,
        'update-cart' : 1,
        csrfmiddlewaretoken: token
      },
      success: function(response){
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
        $('.cart-data').load(location.href + ' .cart-data')
      },
      error: function(){
        alertify.error('Có lỗi xảy ra!')
      }
    })
  });
  
  $(document).on('click','.remove-btn', function(e){
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
      method: 'POST',
      url: "cart",
      data: {
        'product_id': product_id,
        'remove-item' : 1,
        csrfmiddlewaretoken: token
      },
      success: function(response){
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
        $('.cart-data').load(location.href + ' .cart-data')
      },
      error: function(){
        alertify.error('Có lỗi xảy ra!')
      }
    })
  })
});