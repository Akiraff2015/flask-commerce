$(function() {
    let price = [];
    let cart = [];
    let totalPrice = 0
    const add = (a, b) => parseFloat(a) + parseFloat(b);

    $('#listCheckout').css({'display': 'none'});

    $('.productBtn').on('click', function() {
        cart.push($(this).data('product'));
        $('#listCheckout').empty();
        cart.forEach(val => {
            $('#listCheckout').append(`<p>${val.currency} ${val.price} - ${val.name}</p>`);
        });
        $('#listCheckout').append('<input id="confirmBtn" type="submit" value="Confirm" />');

        let total = () => {
            if (cart.length == 1) return cart[0].price;

            if (cart.length > 1) {
                price = [];
                for (let i = 0; i < cart.length; i++) price.push(cart[i].price);
                return price.reduce(add).toFixed(2);
            }
            return 0.00;
        };
        totalPrice = total();

        $('#totalPrice').text(total());
    });

    $('#checkout').click(function(e) {
        e.preventDefault();
        $('#listCheckout').css({'display': 'block'});
    });

    $(document).on('click', '#confirmBtn', function(e) {
        console.log(cart);
        $.ajax({
            url: '/checkout',
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({cart: cart, price: totalPrice})
        }).done(function() {
            console.log("Data been sent!")
        });
    });
});