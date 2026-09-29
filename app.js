// CORE module loaded on every page

function formatPrice(num) {
  if (num === null || num === undefined) return '';
  num = Number(num);
  if (isNaN(num)) return '';
  return `${CONFIG.CURRENCY} ${num.toLocaleString()}`;
}

function generateStars(rating) {
  if (!rating) return '';
  let starsHtml = '';
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.5;
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

  const fullStarSvg = `<svg class="star star-full" viewBox="0 0 24 24" width="16" height="16" fill="gold"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>`;
  const halfStarSvg = `<svg class="star star-half" viewBox="0 0 24 24" width="16" height="16" fill="gold"><path d="M22 9.24l-7.19-.62L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.63-7.03L22 9.24zM12 15.4V6.1l1.71 4.04 4.38.38-3.32 2.88 1 4.28L12 15.4z"/></svg>`;
  const emptyStarSvg = `<svg class="star star-empty" viewBox="0 0 24 24" width="16" height="16" fill="#ccc"><path d="M22 9.24l-7.19-.62L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.63-7.03L22 9.24zM12 15.4l-3.76 2.27 1-4.28-3.32-2.88 4.38-.38L12 6.1l1.71 4.04 4.38.38-3.32 2.88 1 4.28L12 15.4z"/></svg>`;

  for (let i = 0; i < fullStars; i++) starsHtml += fullStarSvg;
  if (hasHalfStar) starsHtml += halfStarSvg;
  for (let i = 0; i < emptyStars; i++) starsHtml += emptyStarSvg;
  return starsHtml;
}

function showToast(message, duration = 3000) {
  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px;';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.style.cssText = 'background: #333; color: white; padding: 12px 20px; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); opacity: 0; transition: opacity 0.3s ease;';
  toast.innerText = message;
  
  toastContainer.appendChild(toast);
  
  // Trigger animation
  setTimeout(() => toast.style.opacity = '1', 10);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

function handleImageError(img) {
  if (img.getAttribute('data-error')) return; // prevent infinite loop
  img.setAttribute('data-error', 'true');
  img.src = 'assets/placeholder.svg';
}

function renderHeader() {
  const headerContainer = document.getElementById('header');
  if (!headerContainer) return;

  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const getActiveClass = (path) => currentPath === path ? 'active' : '';

  headerContainer.innerHTML = `
    <div class="promo-bar">
      Free delivery on orders above ${formatPrice(CONFIG.FREE_DELIVERY_THRESHOLD)}
    </div>
    <header class="main-header">
      <div class="header-left">
        <button id="mobile-menu-btn" class="mobile-menu-btn">☰</button>
        <a href="index.html" class="logo">${CONFIG.STORE_NAME}</a>
      </div>
      
      <nav id="main-nav" class="main-nav">
        <ul>
          <li><a href="index.html" class="${getActiveClass('index.html')}">Home</a></li>
          <li><a href="shop.html" class="${getActiveClass('shop.html')}">Shop</a></li>
          <li class="dropdown">
            <a href="#" class="dropdown-toggle">Categories ▼</a>
            <ul class="dropdown-menu">
              <li><a href="shop.html?category=electronics">Electronics</a></li>
              <li><a href="shop.html?category=fashion">Fashion</a></li>
              <li><a href="shop.html?category=home">Home & Living</a></li>
            </ul>
          </li>
          <li><a href="shop.html?sale=true">Sale</a></li>
          <li><a href="shop.html?new_arrival=true">New Arrivals</a></li>
        </ul>
      </nav>

      <div class="header-right">
        <div class="search-container">
          <input type="text" id="header-search-input" placeholder="Search...">
          <button id="header-search-btn">🔍</button>
        </div>
        <div class="cart-icon-wrapper" onclick="if(typeof toggleCartDrawer === 'function') toggleCartDrawer()">
          🛒
          <span id="cart-count" class="cart-badge" style="display:none;">0</span>
        </div>
      </div>
    </header>
  `;

  // Search logic
  const searchInput = document.getElementById('header-search-input');
  const searchBtn = document.getElementById('header-search-btn');
  
  const doSearch = () => {
    const q = searchInput.value.trim();
    if (q) window.location.href = `search.html?q=${encodeURIComponent(q)}`;
  };
  
  if (searchBtn) searchBtn.addEventListener('click', doSearch);
  if (searchInput) searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') doSearch();
  });
}

function renderFooter() {
  const footerContainer = document.getElementById('footer');
  if (!footerContainer) return;

  footerContainer.innerHTML = `
    <footer class="main-footer">
      <div class="footer-grid">
        <div class="footer-col">
          <h4>${CONFIG.STORE_NAME}</h4>
          <p>${CONFIG.TAGLINE}</p>
          <p>${CONFIG.ADDRESS}</p>
        </div>
        <div class="footer-col">
          <h4>Quick Links</h4>
          <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="shop.html">Shop</a></li>
            <li><a href="shop.html">Categories</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Customer Support</h4>
          <ul>
            <li><a href="faq.html">FAQ</a></li>
            <li><a href="shipping.html">Shipping</a></li>
            <li><a href="faq.html">Returns</a></li>
            <li><a href="privacy.html">Privacy Policy</a></li>
            <li><a href="terms.html">Terms</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Connect</h4>
          <div class="social-links">
            <a href="${CONFIG.INSTAGRAM_URL}" target="_blank">IG</a>
            <a href="${CONFIG.FACEBOOK_URL}" target="_blank">FB</a>
            <a href="${CONFIG.TIKTOK_URL}" target="_blank">TT</a>
            <a href="${CONFIG.WHATSAPP_URL}" target="_blank">WA</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>Copyright © 2026 ${CONFIG.STORE_NAME}. All rights reserved.</p>
      </div>
    </footer>
  `;
}

function renderWhatsAppFloat() {
  const waFloat = document.createElement('a');
  waFloat.href = `https://wa.me/${CONFIG.WHATSAPP_NUMBER}`;
  waFloat.target = '_blank';
  waFloat.className = 'whatsapp-float';
  waFloat.innerHTML = '💬'; // simple icon for now
  waFloat.style.cssText = 'position: fixed; bottom: 20px; left: 20px; background: #25D366; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 100; text-decoration: none;';
  document.body.appendChild(waFloat);
}

function initMobileMenu() {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const nav = document.getElementById('main-nav');
  if (!menuBtn || !nav) return;

  // simplistic implementation for vanilla JS
  menuBtn.addEventListener('click', () => {
    nav.classList.toggle('open');
  });
}

document.addEventListener('DOMContentLoaded', () => {
  renderHeader();
  renderFooter();
  renderWhatsAppFloat();
  initMobileMenu();
  if (typeof updateCartBadge === 'function') {
    updateCartBadge();
  }
});
