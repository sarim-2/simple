const CART_KEY = 'nexamart_cart';

function getCart() {
  try {
    const data = localStorage.getItem(CART_KEY);
    return data ? JSON.parse(data) : [];
  } catch (e) {
    console.error('Error reading cart', e);
    return [];
  }
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

async function addToCart(productId, qty = 1) {
  const products = await fetchProducts();
  const product = products.find(p => p.id === String(productId) || p.id === Number(productId));
  
  if (!product) {
    showToast('Product not found');
    return;
  }
  
  if (product.stock === false) {
    showToast('This product is out of stock');
    return;
  }
  
  let cart = getCart();
  const existing = cart.find(item => item.id === product.id);
  
  if (existing) {
    existing.quantity += qty;
  } else {
    cart.push({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      quantity: qty,
      stock: product.stock
    });
  }
  
  saveCart(cart);
  showToast('Added to cart');
  updateCartBadge();
  renderCartDrawer();
  if (document.getElementById('cart-page-content')) {
    renderCartPage();
  }
}

function removeFromCart(productId) {
  let cart = getCart();
  cart = cart.filter(item => item.id !== String(productId) && item.id !== Number(productId));
  saveCart(cart);
  updateCartBadge();
  renderCartDrawer();
  if (document.getElementById('cart-page-content')) {
    renderCartPage();
  }
}

function updateCartQuantity(productId, qty) {
  qty = Number(qty);
  if (qty <= 0) {
    removeFromCart(productId);
    return;
  }
  
  let cart = getCart();
  const item = cart.find(item => item.id === String(productId) || item.id === Number(productId));
  if (item) {
    item.quantity = qty;
    saveCart(cart);
    updateCartBadge();
    renderCartDrawer();
    if (document.getElementById('cart-page-content')) {
      renderCartPage();
    }
  }
}

function clearCart() {
  saveCart([]);
  updateCartBadge();
  renderCartDrawer();
  if (document.getElementById('cart-page-content')) {
    renderCartPage();
  }
}

function getCartSubtotal() {
  const cart = getCart();
  return cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
}

function getCartCount() {
  const cart = getCart();
  return cart.reduce((sum, item) => sum + item.quantity, 0);
}

function getDeliveryFee(subtotal) {
  if (subtotal >= CONFIG.FREE_DELIVERY_THRESHOLD || subtotal === 0) return 0;
  return CONFIG.DELIVERY_FEE;
}

function getCartTotal() {
  const subtotal = getCartSubtotal();
  return subtotal + getDeliveryFee(subtotal);
}

function updateCartBadge() {
  const badge = document.getElementById('cart-count');
  if (!badge) return;
  const count = getCartCount();
  if (count > 0) {
    badge.innerText = count;
    badge.style.display = 'inline-block';
  } else {
    badge.style.display = 'none';
  }
}

async function buyNow(productId) {
  await addToCart(productId, 1);
  window.location.href = 'checkout.html';
}

function renderCartDrawer() {
  let container = document.getElementById('cart-drawer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'cart-drawer';
    container.className = 'cart-drawer';
    document.body.appendChild(container);
  }
  
  const cart = getCart();
  const subtotal = getCartSubtotal();
  
  let itemsHtml = '';
  if (cart.length === 0) {
    itemsHtml = '<p style="padding: 20px;">Your cart is empty.</p>';
  } else {
    itemsHtml = cart.map(item => `
      <div class="cart-drawer-item" style="display:flex; margin-bottom:15px; gap:10px;">
        <img src="assets/products/${item.image}" width="60" onerror="handleImageError(this)">
        <div style="flex:1;">
          <h4 style="margin:0">${item.name}</h4>
          <p style="margin:5px 0">${formatPrice(item.price)}</p>
          <div>
            <button onclick="updateCartQuantity('${item.id}', ${item.quantity - 1})">-</button>
            <span>${item.quantity}</span>
            <button onclick="updateCartQuantity('${item.id}', ${item.quantity + 1})">+</button>
          </div>
        </div>
        <button onclick="removeFromCart('${item.id}')" style="background:none; border:none; color:red; cursor:pointer;">×</button>
      </div>
    `).join('');
  }
  
  container.innerHTML = `
    <div class="cart-drawer-header" style="display:flex; justify-content:space-between; padding:15px; border-bottom:1px solid #eee;">
      <h3>Cart (${getCartCount()})</h3>
      <button onclick="toggleCartDrawer()">×</button>
    </div>
    <div class="cart-drawer-body" style="padding:15px; overflow-y:auto; flex:1;">
      ${itemsHtml}
    </div>
    <div class="cart-drawer-footer" style="padding:15px; border-top:1px solid #eee;">
      <div style="display:flex; justify-content:space-between; margin-bottom:15px;">
        <span>Subtotal:</span>
        <strong>${formatPrice(subtotal)}</strong>
      </div>
      <a href="cart.html" class="btn btn--secondary" style="display:block; text-align:center; margin-bottom:10px;">View Cart</a>
      <a href="checkout.html" class="btn btn--primary" style="display:block; text-align:center;">Checkout</a>
    </div>
  `;
}

function toggleCartDrawer() {
  let drawer = document.getElementById('cart-drawer');
  if (!drawer) {
    renderCartDrawer();
    drawer = document.getElementById('cart-drawer');
  }
  
  drawer.classList.toggle('active');
  
  // Overlay management
  let overlay = document.getElementById('cart-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'cart-overlay';
    overlay.style.cssText = 'position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:99; display:none;';
    overlay.onclick = toggleCartDrawer;
    document.body.appendChild(overlay);
  }
  
  if (drawer.classList.contains('active')) {
    overlay.style.display = 'block';
    drawer.style.cssText = 'position:fixed; top:0; right:0; bottom:0; width:350px; max-width:100%; background:white; z-index:100; display:flex; flex-direction:column; box-shadow:-2px 0 5px rgba(0,0,0,0.1); transform:translateX(0); transition:transform 0.3s;';
  } else {
    overlay.style.display = 'none';
    drawer.style.transform = 'translateX(100%)';
  }
}

function renderCartPage() {
  const container = document.getElementById('cart-page-content');
  if (!container) return;
  
  const cart = getCart();
  
  if (cart.length === 0) {
    container.innerHTML = `
      <div class="empty-cart" style="text-align:center; padding: 50px 20px;">
        <h2>Your cart is empty</h2>
        <p>Looks like you haven't added anything yet.</p>
        <a href="shop.html" class="btn btn--primary" style="margin-top:20px; display:inline-block;">Continue Shopping</a>
      </div>
    `;
    return;
  }
  
  const subtotal = getCartSubtotal();
  const delivery = getDeliveryFee(subtotal);
  const total = subtotal + delivery;
  
  const itemsHtml = cart.map(item => `
    <div class="cart-page-item" style="display:flex; border-bottom:1px solid #eee; padding:20px 0; align-items:center; gap:20px;">
      <img src="assets/products/${item.image}" width="100" onerror="handleImageError(this)">
      <div style="flex:1;">
        <h3><a href="product.html?id=${item.id}">${item.name}</a></h3>
        <p>${formatPrice(item.price)}</p>
      </div>
      <div>
        <button onclick="updateCartQuantity('${item.id}', ${item.quantity - 1})" class="btn btn--sm">-</button>
        <span style="padding: 0 10px;">${item.quantity}</span>
        <button onclick="updateCartQuantity('${item.id}', ${item.quantity + 1})" class="btn btn--sm">+</button>
      </div>
      <div style="min-width: 100px; text-align:right;">
        <strong>${formatPrice(item.price * item.quantity)}</strong>
      </div>
      <button onclick="removeFromCart('${item.id}')" class="btn btn--sm btn--danger">Remove</button>
    </div>
  `).join('');
  
  container.innerHTML = `
    <div class="cart-page-layout" style="display:flex; gap:30px; flex-wrap:wrap;">
      <div class="cart-items-section" style="flex:2; min-width:300px;">
        ${itemsHtml}
        <div style="margin-top:20px; display:flex; justify-content:space-between;">
          <a href="shop.html" class="btn btn--secondary">Continue Shopping</a>
          <button onclick="clearCart()" class="btn btn--secondary">Clear Cart</button>
        </div>
      </div>
      <div class="cart-summary-section" style="flex:1; min-width:300px; background:#f9f9f9; padding:20px; border-radius:8px; height:fit-content;">
        <h3>Order Summary</h3>
        <div style="display:flex; justify-content:space-between; margin:15px 0;">
          <span>Subtotal:</span>
          <span>${formatPrice(subtotal)}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin:15px 0;">
          <span>Delivery Fee:</span>
          <span>${delivery === 0 ? 'FREE' : formatPrice(delivery)}</span>
        </div>
        <hr style="border:none; border-top:1px solid #ddd; margin:15px 0;">
        <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:1.2em;">
          <span>Total:</span>
          <span>${formatPrice(total)}</span>
        </div>
        <a href="checkout.html" class="btn btn--primary" style="display:block; text-align:center; width:100%; margin-top:20px;">Proceed to Checkout</a>
      </div>
    </div>
  `;
}
