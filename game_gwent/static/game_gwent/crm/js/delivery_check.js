document.addEventListener("DOMContentLoaded", function() {
    const freeShippingCheckbox = document.getElementById('free_shipping');
    const addressFields = document.getElementById('address_fields');
    const commentSection = document.getElementById('comment_section');
    const buyButton = document.getElementById('buy_button');
    const checkoutButton = document.getElementById('checkout_button');
    const formAction = document.getElementById('form_action');

    freeShippingCheckbox.addEventListener('change', function() {
        if (this.checked) {
            addressFields.style.display = 'block';
            commentSection.style.display = 'block';
            buyButton.style.display = 'block';
            checkoutButton.style.display = 'none';
        } else {
            addressFields.style.display = 'none';
            commentSection.style.display = 'none';
            buyButton.style.display = 'none';
            checkoutButton.style.display = 'block';
        }
    });

    // Инициализация начального состояния
    if (freeShippingCheckbox.checked) {
        addressFields.style.display = 'block';
        commentSection.style.display = 'block';
        buyButton.style.display = 'block';
        checkoutButton.style.display = 'none';
    } else {
        addressFields.style.display = 'none';
        commentSection.style.display = 'none';
        buyButton.style.display = 'none';
        checkoutButton.style.display = 'block';
    }

    // Обработчик кнопки "Оформить заказ"
    checkoutButton.addEventListener('click', function() {
        formAction.value = 'checkout';
        document.getElementById('order_form').submit();
    });

    // Обработчик кнопки "Купить"
    buyButton.addEventListener('click', function() {
        formAction.value = 'buy';
    });
});
