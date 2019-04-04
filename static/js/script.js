$(function() {
    let price = [];
    let cart = [];
    let totalPrice = 0
    const add = (a, b) => parseFloat(a) + parseFloat(b);

    count = (ary, classifier) => {
        classifier = classifier || String;
        return ary.reduce((counter, item) => {
            var p = classifier(item);
            counter[p] = counter.hasOwnProperty(p) ? counter[p] + 1 : 1;
            return counter;
        }, {})
    };

    const getPrice = (arr, name) => {
        let itemPrice = 0;
        let findPrince = arr.forEach(val => {
            if (val.name.localeCompare(name) == 0) {
                 itemPrice = val.price
             }
        });
        return itemPrice;
     }

    $('.productBtn').on('click', function() {
        cart.push($(this).data('product'));
        countByItem = count(cart, function(i) {
            return i.name;
        });

        const entries = Object.entries(countByItem);
        $('#listCheckout').empty();
        entries.forEach(val => {
            $('#listCheckout').append(`
                <tr>
                    <td>${val[0]}</td>
                    <td>$${getPrice(cart, val[0])} </td>
                    <td>${val[1]}</td>
                </tr>
            `);
        });

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

        $('.totalPrice').text(total());
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

    let arrModal = ['.modal-background', '.delete', '#shoppingCart', '#cancelBtn'];
    arrModal.forEach(val => $(val).on('click', () =>  $('.modal').toggleClass('is-active')));

    $.ajax({
        url: 'http://localhost:5000/api/products/all',
        headers: {
            'x-api-key': 'test',
            'Content-Type': 'application/json'
        },
        method: 'GET',
        success: data => console.log(data)
    })
});