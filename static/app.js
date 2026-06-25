const API_URL = '/api';

const productsGrid = document.getElementById('products-grid');
const cartToggle = document.getElementById('carrito');
const closeCartBtn = document.getElementById('cerrar-carrito');
const cartSidebar = document.getElementById('cart-sidebar');
const overlay = document.getElementById('overlay');
const cartItemsContainer = document.getElementById('cart-items');
const cartTotalElement = document.getElementById('total-carrito');
const cartCountElement = document.getElementById('contador-carrito');

async function loadProducts() {
    try {
        const res = await fetch(`${API_URL}/products`);
        const products = await res.json();
        renderProducts(products);
    } catch (e) {
        console.error("Error cargando productos", e);
    }
}

function renderProducts(products) {
    productsGrid.innerHTML = '';
    products.forEach(p => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <img src="${p.imagen_url}" alt="${p.nombre}" class="card-img">
            <div class="card-content">
                <h3 class="card-title">${p.nombre}</h3>
                <p class="card-desc">${p.descripcion}</p>
                <div class="card-price">$${p.precio.toFixed(2)} ARS</div>
                <button class="add-btn" id="agregar-pizza-${p.id}" onclick="addToCart(${p.id}, this)">Agregar al pedido</button>
            </div>
        `;
        productsGrid.appendChild(card);
    });
}

async function loadCart() {
    try {
        const res = await fetch(`${API_URL}/cart`);
        const data = await res.json();
        renderCart(data);
    } catch (e) {
        console.error("Error cargando carrito", e);
    }
}

function renderCart(cartData) {
    cartItemsContainer.innerHTML = '';
    
    let totalItems = 0;
    cartData.items.forEach(item => {
        totalItems += item.quantity;
        const itemEl = document.createElement('div');
        itemEl.className = 'cart-item';
        itemEl.innerHTML = `
            <div class="item-info">
                <h4>${item.name} (x${item.quantity})</h4>
                <p>$${item.price.toFixed(2)} ARS</p>
            </div>
            <button class="del-btn" id="eliminar-pizza-${item.productId}" onclick="removeFromCart(${item.productId})">Eliminar</button>
        `;
        cartItemsContainer.appendChild(itemEl);
    });

    cartTotalElement.innerText = `$${cartData.total.toFixed(2)} ARS`;
    cartCountElement.innerText = totalItems;
}

async function addToCart(productId, btnElement) {
    try {
        const res = await fetch(`${API_URL}/cart`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ productId: productId })
        });
        if (res.ok) {
            btnElement.innerText = '¡Añadido!';
            btnElement.classList.add('added');
            setTimeout(() => {
                btnElement.innerText = 'Agregar al pedido';
                btnElement.classList.remove('added');
            }, 1000);
            loadCart();
        }
    } catch (e) {
        console.error("Error agregando al carrito", e);
    }
}

async function removeFromCart(productId) {
    try {
        const res = await fetch(`${API_URL}/cart/${productId}`, { method: 'DELETE' });
        if (res.ok) loadCart();
    } catch (e) {
        console.error("Error eliminando del carrito", e);
    }
}

cartToggle.addEventListener('click', () => {
    cartSidebar.classList.add('open');
    overlay.classList.add('show');
});

closeCartBtn.addEventListener('click', () => {
    cartSidebar.classList.remove('open');
    overlay.classList.remove('show');
});

overlay.addEventListener('click', () => {
    cartSidebar.classList.remove('open');
    overlay.classList.remove('show');
});

loadProducts();
loadCart();
