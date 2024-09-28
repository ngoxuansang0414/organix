const forms = document.querySelectorAll('#addtocart');
forms.forEach(form => {
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const input = event.target.querySelector('input');
        const value = input.value;
        $.ajax({
            type: 'POST',
            url: "/",
            data: {
                product: value,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                $('.badge').html(data)
            }
        });
    });
});
