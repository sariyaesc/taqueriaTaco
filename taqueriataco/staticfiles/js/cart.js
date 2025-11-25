function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function addToCart(productId) {
    const qtyField = document.getElementById('qty-' + productId);
    const qty = qtyField ? parseInt(qtyField.value) : 1;
    const csrftoken = getCookie('csrftoken');

    const form = new FormData();
    form.append('product_id', productId);
    form.append('quantity', qty);

    const res = await fetch('/cart/add/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        body: form
    });
    if (res.ok) {
        const data = await res.json();
        const el = document.getElementById('cart-count');
        if (el) el.textContent = data.cart_count;
    } else {
        console.error('addToCart failed', res.status, await res.text());
        alert('No se pudo agregar el producto al carrito (ver consola)');
    }
}

async function updateCart(productId, quantity) {
    const csrftoken = getCookie('csrftoken');
    const form = new FormData();
    form.append('product_id', productId);
    form.append('quantity', quantity);

    const res = await fetch('/cart/update/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        body: form
    });
    if (res.ok) {
        const data = await res.json();
        const el = document.getElementById('cart-count');
        if (el) el.textContent = data.cart_count;
        location.reload();
    } else {
        console.error('updateCart failed', res.status, await res.text());
        alert('No se pudo actualizar el carrito (ver consola)');
    }
}

async function removeFromCart(productId) {
    const csrftoken = getCookie('csrftoken');
    const form = new FormData();
    form.append('product_id', productId);

    const res = await fetch('/cart/remove/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        body: form
    });
    if (res.ok) {
        const data = await res.json();
        const el = document.getElementById('cart-count');
        if (el) el.textContent = data.cart_count;
        location.reload();
    } else {
        console.error('removeFromCart failed', res.status, await res.text());
        alert('No se pudo eliminar el producto (ver consola)');
    }
}
