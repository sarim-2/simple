import os

workspace = r"c:\Users\Sarim Ali\OneDrive\Desktop\Ecommerce"
os.makedirs(workspace, exist_ok=True)

template_top = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | NexaMart</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title} | NexaMart">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/responsive.css">
</head>
<body>
  <header id="header"></header>
  
  <main>
"""

template_bottom = """  </main>

  <footer id="footer"></footer>

  <!-- Cart Drawer -->
  <div id="cart-drawer"></div>
  <div id="cart-drawer-overlay" class="cart-drawer__overlay" onclick="toggleCartDrawer()"></div>

  <!-- Quick View Modal -->
  <div id="quick-view-modal" class="modal-overlay" onclick="closeQuickView()">
    <div class="modal" onclick="event.stopPropagation()">
      <button class="modal__close" onclick="closeQuickView()" aria-label="Close">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
      <div id="quick-view-content"></div>
    </div>
  </div>

  <!-- Mobile Menu -->
  <div id="mobile-menu-overlay" class="mobile-menu__overlay" onclick="closeMobileMenu()"></div>
  <div id="mobile-menu" class="mobile-menu">
    <div class="mobile-menu__header">
      <span style="font-size:20px;font-weight:700">NexaMart</span>
      <button class="mobile-menu__close" onclick="closeMobileMenu()" aria-label="Close menu">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
    </div>
    <nav class="mobile-menu__nav">
      <a href="index.html">Home</a>
      <a href="shop.html">Shop</a>
      <a href="shop.html">Categories</a>
      <a href="sale.html">Sale</a>
      <a href="new-arrivals.html">New Arrivals</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
      <a href="faq.html">FAQ</a>
    </nav>
  </div>

  <!-- Toast -->
  <div id="toast" class="toast"></div>

  <!-- Scripts -->
  <script src="js/config.js"></script>
  <script src="js/app.js"></script>
  <script src="js/products.js"></script>
  <script src="js/cart.js"></script>
{scripts}
</body>
</html>
"""

def write_page(filename, title, desc, main_content, scripts=""):
    content = template_top.format(title=title, desc=desc) + main_content + template_bottom.format(scripts=scripts)
    with open(os.path.join(workspace, filename), "w", encoding="utf-8") as f:
        f.write(content)

# 1. index.html
index_main = """
<section class="hero">
  <div class="container">
    <div class="hero__inner">
      <div class="hero__content">
        <h1 class="hero__title">Everything You Need.<br>All in One Place.</h1>
        <p class="hero__subtitle">Discover everyday products at simple prices. Quality items delivered to your doorstep.</p>
        <div class="hero__actions">
          <a href="shop.html" class="btn btn--primary btn--lg">Shop Now</a>
          <a href="shop.html" class="btn btn--secondary btn--lg">View Categories</a>
        </div>
      </div>
      <div class="hero__image">
        <img src="assets/banners/hero-illustration.svg" alt="Shopping illustration" onerror="handleImageError(this)">
      </div>
    </div>
  </div>
</section>

<section class="section" id="categories-section">
  <div class="container">
    <div class="section__header">
      <h2 class="section__title">Shop by Category</h2>
      <a href="shop.html" class="section__link">View All →</a>
    </div>
    <div id="categories-grid" class="categories-grid">
      <!-- Rendered by JS -->
    </div>
  </div>
</section>

<section class="section" id="sale-section" style="background:var(--color-bg-secondary)">
  <div class="container">
    <div class="section__header">
      <h2 class="section__title">🔥 On Sale</h2>
      <a href="sale.html" class="section__link">View All →</a>
    </div>
    <div id="sale-products" class="product-grid">
      <!-- Rendered by JS -->
    </div>
  </div>
</section>

<section class="section" id="popular-section">
  <div class="container">
    <div class="section__header">
      <h2 class="section__title">Popular Products</h2>
      <a href="shop.html?filter=popular" class="section__link">View All →</a>
    </div>
    <div id="popular-products" class="product-grid">
      <!-- Rendered by JS -->
    </div>
  </div>
</section>

<section class="section" id="new-arrivals-section" style="background:var(--color-bg-secondary)">
  <div class="container">
    <div class="section__header">
      <h2 class="section__title">New Arrivals</h2>
      <a href="new-arrivals.html" class="section__link">View All →</a>
    </div>
    <div id="new-arrivals-products" class="product-grid">
      <!-- Rendered by JS -->
    </div>
  </div>
</section>

<section class="newsletter">
  <div class="container">
    <h2>Stay Updated</h2>
    <p>Subscribe to get notified about new products and exclusive offers.</p>
    <form class="newsletter__form" onsubmit="event.preventDefault(); showToast('Thank you for subscribing!');">
      <input type="email" placeholder="Enter your email" required aria-label="Email address">
      <button type="submit">Subscribe</button>
    </form>
  </div>
</section>
"""
index_scripts = """  <script>
    document.addEventListener('DOMContentLoaded', async function() {
      const products = await fetchProducts();
      if (!products.length) return;
      
      // Render categories
      const categories = getCategories(products);
      const catGrid = document.getElementById('categories-grid');
      if (catGrid) {
        // Category icons mapping
        const categoryIcons = {
          'Electronics': '⚡', 'Clothing': '👕', 'Gadgets': '🔧',
          'Home & Living': '🏠', 'Accessories': '👜', 'Beauty': '✨',
          'Sports': '⚽'
        };
        catGrid.innerHTML = categories.map(cat => `
          <a href="category.html?category=${encodeURIComponent(cat.name)}" class="category-card">
            <div class="category-card__icon" style="font-size:32px">${categoryIcons[cat.name] || '📦'}</div>
            <div class="category-card__name">${cat.name}</div>
            <div class="category-card__count">${cat.count} Products</div>
          </a>
        `).join('');
      }
      
      // Render sale products (max 4)
      const saleProducts = products.filter(p => p.sale);
      const saleSection = document.getElementById('sale-section');
      if (saleProducts.length === 0 && saleSection) saleSection.style.display = 'none';
      else renderProductGrid('sale-products', saleProducts.slice(0, 4));
      
      // Render popular products (max 4)
      const popularProducts = products.filter(p => p.popular);
      const popSection = document.getElementById('popular-section');
      if (popularProducts.length === 0 && popSection) popSection.style.display = 'none';
      else renderProductGrid('popular-products', popularProducts.slice(0, 4));
      
      // Render new arrivals (max 4)
      const newProducts = products.filter(p => p.new_arrival);
      const newSection = document.getElementById('new-arrivals-section');
      if (newProducts.length === 0 && newSection) newSection.style.display = 'none';
      else renderProductGrid('new-arrivals-products', newProducts.slice(0, 4));
    });
  </script>"""

write_page("index.html", "NexaMart - Everything You Need", "Discover everyday products at simple prices.", index_main, index_scripts)

# 2. shop.html
shop_main = """
<div class="container">
  <div class="page-header">
    <h1>Shop</h1>
    <p>Browse our complete collection</p>
  </div>
  
  <button class="btn btn--secondary mobile-filter-btn" onclick="toggleShopSidebar()">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 21V14M4 10V3M12 21V12M12 8V3M20 21V16M20 12V3M1 14h6M9 8h6M17 16h6"/></svg>
    Filters
  </button>
  
  <div class="shop-layout">
    <aside class="shop-sidebar" id="shop-sidebar">
      <div class="shop-sidebar__section">
        <h3 class="shop-sidebar__title">Categories</h3>
        <div id="filter-categories" class="shop-sidebar__list"></div>
      </div>
      <div class="shop-sidebar__section">
        <h3 class="shop-sidebar__title">Price Range</h3>
        <div class="price-range">
          <input type="number" id="price-min" placeholder="Min" aria-label="Minimum price">
          <span>—</span>
          <input type="number" id="price-max" placeholder="Max" aria-label="Maximum price">
        </div>
        <button class="btn btn--secondary btn--sm btn--full" onclick="applyFilters()" style="margin-top:8px">Apply</button>
      </div>
      <div class="shop-sidebar__section">
        <h3 class="shop-sidebar__title">Availability</h3>
        <div class="shop-sidebar__list">
          <label class="shop-sidebar__item"><input type="radio" name="stock" value="all" checked onchange="applyFilters()"> All</label>
          <label class="shop-sidebar__item"><input type="radio" name="stock" value="in" onchange="applyFilters()"> In Stock</label>
          <label class="shop-sidebar__item"><input type="radio" name="stock" value="out" onchange="applyFilters()"> Out of Stock</label>
        </div>
      </div>
      <div class="shop-sidebar__section">
        <h3 class="shop-sidebar__title">Filter</h3>
        <div class="shop-sidebar__list">
          <label class="shop-sidebar__item"><input type="checkbox" id="filter-sale" onchange="applyFilters()"> On Sale</label>
          <label class="shop-sidebar__item"><input type="checkbox" id="filter-new" onchange="applyFilters()"> New Arrivals</label>
          <label class="shop-sidebar__item"><input type="checkbox" id="filter-popular" onchange="applyFilters()"> Popular</label>
        </div>
      </div>
    </aside>
    
    <div class="shop-main">
      <div class="shop-header">
        <div class="shop-header__count" id="products-count">Showing 0 products</div>
        <div class="shop-header__sort">
          <select id="sort-select" onchange="applyFilters()" aria-label="Sort products">
            <option value="featured">Featured</option>
            <option value="newest">Newest</option>
            <option value="price-asc">Price: Low to High</option>
            <option value="price-desc">Price: High to Low</option>
            <option value="name-asc">Name: A-Z</option>
            <option value="popular">Popular</option>
            <option value="rating">Highest Rated</option>
          </select>
        </div>
      </div>
      <div id="shop-products" class="product-grid"></div>
      <div id="shop-pagination" class="pagination"></div>
    </div>
  </div>
</div>
"""
shop_scripts = """  <script>
    let currentPage = 1;
    let allProducts = [];
    
    function getFilters() {
      const category = document.querySelector('#filter-categories .shop-sidebar__item.active');
      const stockEl = document.querySelector('input[name="stock"]:checked');
      return {
        category: category ? category.dataset.category : null,
        minPrice: document.getElementById('price-min')?.value ? Number(document.getElementById('price-min').value) : null,
        maxPrice: document.getElementById('price-max')?.value ? Number(document.getElementById('price-max').value) : null,
        stock: stockEl ? stockEl.value : 'all',
        sale: document.getElementById('filter-sale')?.checked || false,
        new_arrival: document.getElementById('filter-new')?.checked || false,
        popular: document.getElementById('filter-popular')?.checked || false
      };
    }
    
    function applyFilters() {
      currentPage = 1;
      renderShop();
    }
    
    function renderShop() {
      const filters = getFilters();
      let filtered = filterProducts(allProducts, filters);
      const sortBy = document.getElementById('sort-select')?.value || 'featured';
      filtered = sortProducts(filtered, sortBy);
      
      const { items, totalPages, totalItems } = paginateProducts(filtered, currentPage, CONFIG.PRODUCTS_PER_PAGE);
      
      document.getElementById('products-count').textContent = `Showing ${items.length} of ${totalItems} products`;
      renderProductGrid('shop-products', items);
      
      if (totalItems === 0) {
        document.getElementById('shop-products').innerHTML = '<div class="empty-state"><h2>No products found</h2><p>Try adjusting your filters.</p></div>';
      }
      
      renderPagination('shop-pagination', currentPage, totalPages, (page) => {
        currentPage = page;
        renderShop();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
    
    function toggleShopSidebar() {
      document.getElementById('shop-sidebar').classList.toggle('active');
    }
    
    document.addEventListener('DOMContentLoaded', async function() {
      allProducts = await fetchProducts();
      
      // Render category filter list
      const categories = getCategories(allProducts);
      const catContainer = document.getElementById('filter-categories');
      if (catContainer) {
        let html = '<div class="shop-sidebar__item active" data-category="" onclick="selectCategory(this)">All <span>' + allProducts.length + '</span></div>';
        categories.forEach(cat => {
          html += `<div class="shop-sidebar__item" data-category="${cat.name}" onclick="selectCategory(this)">${cat.name} <span>${cat.count}</span></div>`;
        });
        catContainer.innerHTML = html;
      }
      
      // Check URL params for pre-selected filter
      const params = new URLSearchParams(window.location.search);
      if (params.get('filter') === 'popular') {
        document.getElementById('filter-popular').checked = true;
      }
      
      renderShop();
    });
    
    function selectCategory(el) {
      document.querySelectorAll('#filter-categories .shop-sidebar__item').forEach(i => i.classList.remove('active'));
      el.classList.add('active');
      applyFilters();
    }
  </script>"""

write_page("shop.html", "Shop", "Browse our complete collection", shop_main, shop_scripts)

# 3. category.html
category_main = """
<div class="container">
  <div class="breadcrumb">
    <a href="index.html">Home</a>
    <span class="breadcrumb__separator">›</span>
    <span id="breadcrumb-category">Category</span>
  </div>
  <div class="page-header">
    <h1 id="category-title">Category</h1>
    <p id="category-count"></p>
  </div>
  <div id="category-products" class="product-grid" style="padding:32px 0"></div>
  <div id="category-pagination" class="pagination"></div>
</div>
"""
category_scripts = """  <script>
    let catPage = 1;
    document.addEventListener('DOMContentLoaded', async function() {
      const params = new URLSearchParams(window.location.search);
      const category = params.get('category');
      if (!category) {
        document.getElementById('category-products').innerHTML = '<div class="empty-state"><h2>No category selected</h2><p>Please select a category.</p><a href="shop.html" class="btn btn--primary">Go to Shop</a></div>';
        return;
      }
      document.getElementById('category-title').textContent = category;
      document.getElementById('breadcrumb-category').textContent = category;
      document.title = category + ' | NexaMart';
      
      const products = await fetchProducts();
      const catProducts = products.filter(p => p.category === category);
      document.getElementById('category-count').textContent = catProducts.length + ' products';
      
      function renderCatPage() {
        const { items, totalPages } = paginateProducts(catProducts, catPage, CONFIG.PRODUCTS_PER_PAGE);
        renderProductGrid('category-products', items);
        if (catProducts.length === 0) {
          document.getElementById('category-products').innerHTML = '<div class="empty-state"><h2>No products in this category</h2><a href="shop.html" class="btn btn--primary">Browse All Products</a></div>';
        }
        renderPagination('category-pagination', catPage, totalPages, (page) => {
          catPage = page;
          renderCatPage();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        });
      }
      renderCatPage();
    });
  </script>"""

write_page("category.html", "Category", "Shop by Category", category_main, category_scripts)


# 4. product.html
product_main = """
<div class="container">
  <div id="product-breadcrumb" class="breadcrumb">
    <a href="index.html">Home</a>
    <span class="breadcrumb__separator">›</span>
    <a href="shop.html">Shop</a>
  </div>
  <div id="product-detail"></div>
  <section class="section" id="related-products-section">
    <div class="section__header">
      <h2 class="section__title">Related Products</h2>
    </div>
    <div id="related-products" class="product-grid"></div>
  </section>
</div>
"""
product_scripts = """  <script src="js/product-detail.js"></script>"""
write_page("product.html", "Product", "Product Details", product_main, product_scripts)


# 5. search.html
search_main = """
<div class="container">
  <div class="page-header">
    <h1 id="search-title">Search Results</h1>
    <p id="search-count"></p>
  </div>
  <div id="search-results" class="product-grid" style="padding:32px 0"></div>
</div>
"""
search_scripts = """  <script src="js/search.js"></script>"""
write_page("search.html", "Search", "Search Results", search_main, search_scripts)

# 6. sale.html
sale_main = """
<div class="container">
  <div class="page-header">
    <h1>🔥 Sale</h1>
    <p>Grab these deals before they're gone</p>
  </div>
  <div id="sale-products" class="product-grid" style="padding:32px 0"></div>
</div>
"""
sale_scripts = """  <script>
    document.addEventListener('DOMContentLoaded', async function() {
      const products = await fetchProducts();
      const saleProducts = products.filter(p => p.sale);
      renderProductGrid('sale-products', saleProducts);
      if (saleProducts.length === 0) {
        document.getElementById('sale-products').innerHTML = '<div class="empty-state"><h2>No sale products available</h2><p>Check back soon for amazing deals!</p><a href="shop.html" class="btn btn--primary">Browse Shop</a></div>';
      }
    });
  </script>"""
write_page("sale.html", "Sale", "Products on sale", sale_main, sale_scripts)

# 7. new-arrivals.html
new_arrivals_main = """
<div class="container">
  <div class="page-header">
    <h1>New Arrivals</h1>
    <p>Discover our latest products</p>
  </div>
  <div id="new-arrivals-products" class="product-grid" style="padding:32px 0"></div>
</div>
"""
new_arrivals_scripts = """  <script>
    document.addEventListener('DOMContentLoaded', async function() {
      const products = await fetchProducts();
      const newProducts = products.filter(p => p.new_arrival);
      renderProductGrid('new-arrivals-products', newProducts);
      if (newProducts.length === 0) {
        document.getElementById('new-arrivals-products').innerHTML = '<div class="empty-state"><h2>No new arrivals</h2><p>Check back later for new products.</p><a href="shop.html" class="btn btn--primary">Browse Shop</a></div>';
      }
    });
  </script>"""
write_page("new-arrivals.html", "New Arrivals", "Latest new arrivals", new_arrivals_main, new_arrivals_scripts)

# 8. cart.html
cart_main = """
<div class="container cart-layout">
  <div class="page-header">
    <h1>Shopping Cart</h1>
  </div>
  <div id="cart-page-content"></div>
</div>
"""
cart_scripts = """  <script>
    document.addEventListener('DOMContentLoaded', function() {
      renderCartPage();
    });
  </script>"""
write_page("cart.html", "Cart", "Your Shopping Cart", cart_main, cart_scripts)

# 9. checkout.html
checkout_main = """
<div class="container">
  <div class="page-header">
    <h1>Checkout</h1>
  </div>
  <div id="checkout-content"></div>
</div>
"""
checkout_scripts = """  <script src="js/checkout.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      renderCheckoutPage();
    });
  </script>"""
write_page("checkout.html", "Checkout", "Checkout and complete order", checkout_main, checkout_scripts)

# 10. success.html
success_main = """
<div class="container">
  <div class="success-page">
    <div class="success-page__icon">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>
    </div>
    <h1>Order Request Created!</h1>
    <p>Your order details have been prepared for WhatsApp. The store will confirm your order shortly.</p>
    <p style="color:var(--color-text-muted);font-size:14px;margin-bottom:24px">Please note: Your order is not officially confirmed until the store responds on WhatsApp.</p>
    <a href="index.html" class="btn btn--primary btn--lg">Continue Shopping</a>
  </div>
</div>
"""
write_page("success.html", "Order Confirmed", "Order successful", success_main, "")


# 11. about.html
about_main = """
<div class="container">
  <div class="page-header">
    <h1>About Us</h1>
  </div>
  <section class="section">
    <h2>Who We Are</h2>
    <p>Welcome to NexaMart, your number one source for everyday products. We're dedicated to providing you the very best of items, with an emphasis on quality, customer service, and uniqueness.</p>
  </section>
  <section class="section">
    <h2>Why Shop With Us</h2>
    <div class="grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;">
      <div class="card" style="padding:20px;border:1px solid #ddd;border-radius:8px;">
        <h3>Quality Products</h3>
        <p>We source only the finest quality items for our customers.</p>
      </div>
      <div class="card" style="padding:20px;border:1px solid #ddd;border-radius:8px;">
        <h3>Fast Delivery</h3>
        <p>Your orders reach you in record time, safely and securely.</p>
      </div>
      <div class="card" style="padding:20px;border:1px solid #ddd;border-radius:8px;">
        <h3>Customer Support</h3>
        <p>Our team is available round the clock to help you with queries.</p>
      </div>
    </div>
  </section>
  <section class="section">
    <h2>What We Offer</h2>
    <p>We offer a wide range of products including electronics, clothing, and home accessories. Our goal is to make shopping easy and accessible to everyone.</p>
  </section>
  <div style="text-align:center;margin-top:40px;">
    <a href="contact.html" class="btn btn--primary">Contact Us</a>
  </div>
</div>
"""
write_page("about.html", "About Us", "About NexaMart", about_main, "")


# 12. contact.html
contact_main = """
<div class="container">
  <div class="page-header">
    <h1>Contact Us</h1>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:40px;margin-bottom:60px;">
    <div>
      <h2>Get in Touch</h2>
      <p>Have questions? We'd love to hear from you.</p>
      <ul style="list-style:none;padding:0;line-height:2;">
        <li>📞 Phone: <span id="contact-phone"></span></li>
        <li>💬 WhatsApp: <span id="contact-whatsapp"></span></li>
        <li>📧 Email: <span id="contact-email"></span></li>
        <li>📍 Address: 123 E-Commerce St, Tech City</li>
        <li>⏰ Business Hours: Mon - Fri, 9am - 6pm</li>
      </ul>
      <a href="#" id="contact-whatsapp-btn" class="btn btn--primary" style="margin-top:16px;">Chat on WhatsApp</a>
    </div>
    <div>
      <h2>Send a Message</h2>
      <form onsubmit="event.preventDefault(); showToast('Message sent successfully!'); this.reset();" style="display:flex;flex-direction:column;gap:16px;">
        <div>
          <label for="contact-name">Name</label>
          <input type="text" id="contact-name" required style="width:100%;padding:10px;margin-top:4px;border:1px solid #ddd;border-radius:4px;">
        </div>
        <div>
          <label for="contact-email-input">Email</label>
          <input type="email" id="contact-email-input" required style="width:100%;padding:10px;margin-top:4px;border:1px solid #ddd;border-radius:4px;">
        </div>
        <div>
          <label for="contact-subject">Subject</label>
          <input type="text" id="contact-subject" required style="width:100%;padding:10px;margin-top:4px;border:1px solid #ddd;border-radius:4px;">
        </div>
        <div>
          <label for="contact-message">Message</label>
          <textarea id="contact-message" rows="5" required style="width:100%;padding:10px;margin-top:4px;border:1px solid #ddd;border-radius:4px;"></textarea>
        </div>
        <button type="submit" class="btn btn--primary">Send Message</button>
      </form>
    </div>
  </div>
</div>
"""
contact_scripts = """  <script>
    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('contact-phone').textContent = CONFIG.STORE_PHONE || '+1234567890';
      document.getElementById('contact-whatsapp').textContent = CONFIG.WHATSAPP_NUMBER || '+1234567890';
      document.getElementById('contact-email').textContent = 'support@nexamart.com';
      document.getElementById('contact-whatsapp-btn').href = `https://wa.me/${CONFIG.WHATSAPP_NUMBER || '1234567890'}`;
    });
  </script>"""
write_page("contact.html", "Contact Us", "Contact NexaMart support", contact_main, contact_scripts)

# 13. faq.html
faq_main = """
<div class="container">
  <div class="page-header">
    <h1>Frequently Asked Questions</h1>
  </div>
  <div class="faq-list" style="max-width:800px;margin:0 auto 60px;">
    <div class="faq-item" style="border:1px solid #ddd;border-radius:4px;margin-bottom:10px;overflow:hidden;" onclick="this.classList.toggle('active')">
      <div class="faq-item__question" style="padding:15px;background:#f9f9f9;cursor:pointer;font-weight:600;">1. How do I place an order?</div>
      <div class="faq-item__answer" style="padding:15px;display:none;background:#fff;">Simply browse our products, add them to your cart, and proceed to checkout. Your order will be sent to us via WhatsApp for confirmation.</div>
    </div>
    <div class="faq-item" style="border:1px solid #ddd;border-radius:4px;margin-bottom:10px;overflow:hidden;" onclick="this.classList.toggle('active')">
      <div class="faq-item__question" style="padding:15px;background:#f9f9f9;cursor:pointer;font-weight:600;">2. What payment methods are available?</div>
      <div class="faq-item__answer" style="padding:15px;display:none;background:#fff;">We accept Cash on Delivery (COD) and bank transfers. Payment details will be discussed during order confirmation.</div>
    </div>
    <div class="faq-item" style="border:1px solid #ddd;border-radius:4px;margin-bottom:10px;overflow:hidden;" onclick="this.classList.toggle('active')">
      <div class="faq-item__question" style="padding:15px;background:#f9f9f9;cursor:pointer;font-weight:600;">3. Do you offer Cash on Delivery?</div>
      <div class="faq-item__answer" style="padding:15px;display:none;background:#fff;">Yes, Cash on Delivery is available for all regions we deliver to.</div>
    </div>
    <div class="faq-item" style="border:1px solid #ddd;border-radius:4px;margin-bottom:10px;overflow:hidden;" onclick="this.classList.toggle('active')">
      <div class="faq-item__question" style="padding:15px;background:#f9f9f9;cursor:pointer;font-weight:600;">4. How long does delivery take?</div>
      <div class="faq-item__answer" style="padding:15px;display:none;background:#fff;">Standard delivery usually takes 3-5 business days depending on your location.</div>
    </div>
    <div class="faq-item" style="border:1px solid #ddd;border-radius:4px;margin-bottom:10px;overflow:hidden;" onclick="this.classList.toggle('active')">
      <div class="faq-item__question" style="padding:15px;background:#f9f9f9;cursor:pointer;font-weight:600;">5. Can I cancel an order?</div>
      <div class="faq-item__answer" style="padding:15px;display:none;background:#fff;">Yes, you can cancel your order by replying to the WhatsApp confirmation message before the order is dispatched.</div>
    </div>
    <div class="faq-item" style="border:1px solid #ddd;border-radius:4px;margin-bottom:10px;overflow:hidden;" onclick="this.classList.toggle('active')">
      <div class="faq-item__question" style="padding:15px;background:#f9f9f9;cursor:pointer;font-weight:600;">6. How can I contact support?</div>
      <div class="faq-item__answer" style="padding:15px;display:none;background:#fff;">You can contact us via the Contact Us page, or simply message us on WhatsApp using the button on our site.</div>
    </div>
    <div class="faq-item" style="border:1px solid #ddd;border-radius:4px;margin-bottom:10px;overflow:hidden;" onclick="this.classList.toggle('active')">
      <div class="faq-item__question" style="padding:15px;background:#f9f9f9;cursor:pointer;font-weight:600;">7. Is there free delivery?</div>
      <div class="faq-item__answer" style="padding:15px;display:none;background:#fff;">We occasionally run promotions offering free delivery. Check our banners or subscribe to our newsletter for updates.</div>
    </div>
    <div class="faq-item" style="border:1px solid #ddd;border-radius:4px;margin-bottom:10px;overflow:hidden;" onclick="this.classList.toggle('active')">
      <div class="faq-item__question" style="padding:15px;background:#f9f9f9;cursor:pointer;font-weight:600;">8. How do I track my order?</div>
      <div class="faq-item__answer" style="padding:15px;display:none;background:#fff;">Once dispatched, we will send you a tracking link via WhatsApp.</div>
    </div>
  </div>
  <style>
    .faq-item.active .faq-item__answer { display: block !important; }
    .faq-item.active .faq-item__question { background: #eee !important; }
  </style>
</div>
"""
write_page("faq.html", "FAQ", "Frequently Asked Questions", faq_main, "")

# 14. privacy.html
privacy_main = """
<div class="container">
  <div class="legal-content" style="max-width:800px;margin:40px auto;">
    <h1>Privacy Policy</h1>
    <section style="margin-top:20px;">
      <h2>Information We Collect</h2>
      <p>We may collect personal information such as your name, email address, phone number, and shipping address when you place an order or interact with our website.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>How We Use Your Information</h2>
      <p>Your information is used to process orders, communicate with you about your order status, and improve our services. We do not sell your data to third parties.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Data Sharing</h2>
      <p>We may share your data with trusted third-party service providers (such as shipping partners) strictly for the purpose of fulfilling your order.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Data Security</h2>
      <p>We implement appropriate security measures to protect your personal information from unauthorized access or disclosure.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Your Rights</h2>
      <p>You have the right to access, update, or request deletion of your personal information at any time by contacting our support team.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Contact Us</h2>
      <p>If you have any questions about this Privacy Policy, please contact us via our Contact page.</p>
    </section>
  </div>
</div>
"""
write_page("privacy.html", "Privacy Policy", "NexaMart Privacy Policy", privacy_main, "")

# 15. terms.html
terms_main = """
<div class="container">
  <div class="legal-content" style="max-width:800px;margin:40px auto;">
    <h1>Terms & Conditions</h1>
    <section style="margin-top:20px;">
      <h2>Terms of Use</h2>
      <p>By accessing and using this website, you agree to be bound by these Terms & Conditions. If you disagree with any part of the terms, please do not use our website.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Products & Pricing</h2>
      <p>All products are subject to availability. We reserve the right to modify prices without prior notice. We strive to provide accurate product images and descriptions.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Orders & Payment</h2>
      <p>By placing an order, you make an offer to purchase the products. Orders are officially confirmed once we reply via WhatsApp. Payment terms are as agreed during the confirmation.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Delivery</h2>
      <p>We aim to deliver products within the estimated timeframes. We are not liable for any delays caused by external factors beyond our control.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Returns</h2>
      <p>Returns are accepted within 7 days of delivery for defective or damaged items. Please contact our support team for a return authorization.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Limitation of Liability</h2>
      <p>NexaMart shall not be liable for any indirect, incidental, or consequential damages arising from the use of our website or products.</p>
    </section>
    <section style="margin-top:20px;">
      <h2>Contact</h2>
      <p>For any inquiries regarding these terms, please contact us.</p>
    </section>
  </div>
</div>
"""
write_page("terms.html", "Terms & Conditions", "NexaMart Terms & Conditions", terms_main, "")
