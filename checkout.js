function validateForm() {
  let isValid = true;
  const fields = ['fullName', 'phone', 'address', 'city'];
  
  fields.forEach(field => {
    const el = document.getElementById(field);
    const group = el?.closest('.form-group') || el?.parentElement;
    if (el && !el.value.trim()) {
      group?.classList.add('form-group--error');
      isValid = false;
    } else if (group) {
      group.classList.remove('form-group--error');
    }
  });

  const paymentMethods = document.getElementsByName('paymentMethod');
  let paymentSelected = false;
  for (let p of paymentMethods) {
    if (p.checked) paymentSelected = true;
  }
  if (!paymentSelected) isValid = false;

  return isValid;
}

function buildOrderObject() {
  const getVal = id => document.getElementById(id)?.value.trim() || '';
  
  let paymentMethod = 'Cash on Delivery';
  const pmElements = document.getElementsByName('paymentMethod');
  for (let p of pmElements) {
    if (p.checked) paymentMethod = p.value === 'online' ? 'Online Payment' : 'Cash on Delivery';
  }

  const phone = getVal('phone');
  const whatsapp = getVal('whatsapp') || phone;

  const cart = getCart();
  const subtotal = getCartSubtotal();
  const deliveryFee = getDeliveryFee(subtotal);

  return {
    customer: {
      name: getVal('fullName'),
      phone,
      whatsapp,
      city: getVal('city'),
      address: getVal('address'),
      postalCode: getVal('postalCode'),
      notes: getVal('notes')
    },
    items: cart,
    paymentMethod,
    subtotal,
    deliveryFee,
    total: subtotal + deliveryFee
  };
}

function generateWhatsAppMessage(order) {
  const c = order.customer;
  let itemsText = order.items.map((item, idx) => 
    `${idx + 1}. ${item.name}\n   Qty: ${item.quantity}\n   Price: ${CONFIG.CURRENCY} ${item.price}\n   Subtotal: ${CONFIG.CURRENCY} ${item.price * item.quantity}`
  ).join('\n\n');

  return `🛒 NEW WEBSITE ORDER
------------------------

Customer: ${c.name}
Phone: ${c.phone}
WhatsApp: ${c.whatsapp}

Address: ${c.address}
City: ${c.city}
${c.postalCode ? `Postal Code: ${c.postalCode}` : ''}

Payment: ${order.paymentMethod}
${c.notes ? `\nNotes: ${c.notes}` : ''}

------------------------
ITEMS

${itemsText}

------------------------

Subtotal: ${CONFIG.CURRENCY} ${order.subtotal}
Delivery: ${order.deliveryFee === 0 ? 'FREE' : `${CONFIG.CURRENCY} ${order.deliveryFee}`}

TOTAL: ${CONFIG.CURRENCY} ${order.total}

------------------------
Please confirm this order.`;
}

function generateWhatsAppURL(message) {
  return `https://wa.me/${CONFIG.WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
}

function handlePlaceOrder() {
  if (!validateForm()) {
    showToast('Please fill all required fields');
    return;
  }

  const order = buildOrderObject();
  const msg = generateWhatsAppMessage(order);
  const url = generateWhatsAppURL(msg);
  
  clearCart();
  window.open(url, '_blank');
  window.location.href = 'success.html'; // Assuming this page exists
}

function renderOrderSummary() {
  const container = document.getElementById('checkout-order-summary');
  if (!container) return;

  const cart = getCart();
  const subtotal = getCartSubtotal();
  const delivery = getDeliveryFee(subtotal);
  const total = subtotal + delivery;

  let itemsHtml = cart.map(item => `
    <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:14px;">
      <span>${item.name} x ${item.quantity}</span>
      <span>${formatPrice(item.price * item.quantity)}</span>
    </div>
  `).join('');

  container.innerHTML = `
    <div style="background:#f9f9f9; padding:20px; border-radius:8px;">
      <h3>Order Summary</h3>
      <div style="margin:20px 0;">
        ${itemsHtml}
      </div>
      <hr style="border:none; border-top:1px solid #ddd; margin:15px 0;">
      <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
        <span>Subtotal:</span>
        <span>${formatPrice(subtotal)}</span>
      </div>
      <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
        <span>Delivery:</span>
        <span>${delivery === 0 ? 'FREE' : formatPrice(delivery)}</span>
      </div>
      <hr style="border:none; border-top:1px solid #ddd; margin:15px 0;">
      <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:18px;">
        <span>Total:</span>
        <span>${formatPrice(total)}</span>
      </div>
    </div>
  `;
}

function renderCheckoutPage() {
  const container = document.getElementById('checkout-page-content');
  if (!container) return;

  const cart = getCart();
  if (cart.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding: 50px;">
        <h2>Your cart is empty</h2>
        <a href="shop.html" class="btn btn--primary" style="margin-top:20px; display:inline-block;">Go to Shop</a>
      </div>
    `;
    // optionally redirect
    // window.location.href = 'shop.html';
    return;
  }

  container.innerHTML = `
    <div style="display:flex; gap:40px; flex-wrap:wrap;">
      <div style="flex:2; min-width:300px;">
        <h2>Checkout</h2>
        <form id="checkout-form" onsubmit="event.preventDefault(); handlePlaceOrder();" style="display:flex; flex-direction:column; gap:20px;">
          
          <div style="background:#fff; padding:20px; border:1px solid #eee; border-radius:8px;">
            <h3>Contact Information</h3>
            <div class="form-group" style="margin-bottom:15px;">
              <label>Full Name *</label>
              <input type="text" id="fullName" class="form-control" style="width:100%; padding:10px;" required>
            </div>
            <div style="display:flex; gap:15px; flex-wrap:wrap;">
              <div class="form-group" style="flex:1; min-width:200px;">
                <label>Phone Number *</label>
                <input type="tel" id="phone" class="form-control" style="width:100%; padding:10px;" required>
              </div>
              <div class="form-group" style="flex:1; min-width:200px;">
                <label>WhatsApp Number (Optional)</label>
                <input type="tel" id="whatsapp" class="form-control" style="width:100%; padding:10px;" placeholder="Leave empty if same as phone">
              </div>
            </div>
          </div>

          <div style="background:#fff; padding:20px; border:1px solid #eee; border-radius:8px;">
            <h3>Delivery Address</h3>
            <div class="form-group" style="margin-bottom:15px;">
              <label>Address *</label>
              <input type="text" id="address" class="form-control" style="width:100%; padding:10px;" required>
            </div>
            <div style="display:flex; gap:15px; flex-wrap:wrap; margin-bottom:15px;">
              <div class="form-group" style="flex:1; min-width:150px;">
                <label>City *</label>
                <input type="text" id="city" class="form-control" style="width:100%; padding:10px;" required>
              </div>
              <div class="form-group" style="flex:1; min-width:150px;">
                <label>Postal Code (Optional)</label>
                <input type="text" id="postalCode" class="form-control" style="width:100%; padding:10px;">
              </div>
            </div>
            <div class="form-group">
              <label>Order Notes (Optional)</label>
              <textarea id="notes" class="form-control" style="width:100%; padding:10px; height:80px;"></textarea>
            </div>
          </div>

          <div style="background:#fff; padding:20px; border:1px solid #eee; border-radius:8px;">
            <h3>Payment Method</h3>
            <div style="margin-bottom:10px;">
              <label style="display:flex; align-items:center; gap:10px;">
                <input type="radio" name="paymentMethod" value="cod" checked>
                Cash on Delivery (COD)
              </label>
            </div>
            <div>
              <label style="display:flex; align-items:center; gap:10px;">
                <input type="radio" name="paymentMethod" value="online">
                Online Payment (Bank Transfer / Card)
              </label>
            </div>
          </div>

          <button type="submit" class="btn btn--primary" style="padding:15px; font-size:16px;">Place Order</button>
        </form>
      </div>

      <div style="flex:1; min-width:300px;">
        <div id="checkout-order-summary"></div>
      </div>
    </div>
  `;

  renderOrderSummary();
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('checkout-page-content')) {
    renderCheckoutPage();
  }
});
