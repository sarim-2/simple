let productsData = null;

async function fetchProducts() {
  if (productsData) return productsData;
  try {
    const response = await fetch(CONFIG.PRODUCTS_JSON_PATH);
    if (!response.ok) throw new Error('Failed to fetch products');
    productsData = await response.json();
    return productsData;
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
}

function getCategories(products) {
  const counts = {};
  products.forEach(p => {
    if (p.category) {
      counts[p.category] = (counts[p.category] || 0) + 1;
    }
  });
  return Object.keys(counts)
    .map(name => ({ name, count: counts[name] }))
    .sort((a, b) => a.name.localeCompare(b.name));
}

function filterProducts(products, filters) {
  if (!filters) return products;
  
  return products.filter(p => {
    let match = true;
    if (filters.category && p.category !== filters.category) match = false;
    if (filters.subcategory && p.subcategory !== filters.subcategory) match = false;
    if (filters.minPrice !== undefined && p.price < filters.minPrice) match = false;
    if (filters.maxPrice !== undefined && p.price > filters.maxPrice) match = false;
    
    if (filters.stock) {
      if (filters.stock === 'in' && p.stock === false) match = false;
      if (filters.stock === 'out' && p.stock !== false) match = false;
    }
    
    if (filters.sale && (!p.discount || p.discount <= 0)) match = false;
    if (filters.popular && !p.popular) match = false;
    if (filters.new_arrival && !p.new_arrival) match = false;
    if (filters.featured && !p.featured) match = false;
    
    if (filters.search) {
      const q = filters.search.toLowerCase();
      const text = `${p.name} ${p.category} ${p.subcategory} ${p.brand || ''} ${p.sku || ''} ${p.description || ''} ${(p.tags || []).join(' ')}`.toLowerCase();
      if (!text.includes(q)) match = false;
    }
    
    return match;
  });
}

function sortProducts(products, sortBy) {
  const arr = [...products];
  switch (sortBy) {
    case 'featured':
      return arr.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0));
    case 'newest':
      return arr.sort((a, b) => (b.new_arrival ? 1 : 0) - (a.new_arrival ? 1 : 0));
    case 'price-asc':
      return arr.sort((a, b) => a.price - b.price);
    case 'price-desc':
      return arr.sort((a, b) => b.price - a.price);
    case 'name-asc':
      return arr.sort((a, b) => a.name.localeCompare(b.name));
    case 'popular':
      return arr.sort((a, b) => (b.popular ? 1 : 0) - (a.popular ? 1 : 0));
    case 'rating':
      return arr.sort((a, b) => (b.rating || 0) - (a.rating || 0));
    default:
      return arr;
  }
}

function paginateProducts(products, page, perPage) {
  const totalItems = products.length;
  const totalPages = Math.ceil(totalItems / perPage) || 1;
  const currentPage = Math.max(1, Math.min(page, totalPages));
  
  const start = (currentPage - 1) * perPage;
  const items = products.slice(start, start + perPage);
  
  return { items, currentPage, totalPages, totalItems };
}

function renderProductCard(product) {
  const { id, image, name, category, rating, reviews, price, old_price, discount, stock } = product;
  
  let badges = '';
  if (product.new_arrival) badges += `<span class="badge badge--new">New</span>`;
  if (product.popular) badges += `<span class="badge badge--popular">Popular</span>`;
  
  return `
<div class="product-card" data-id="${id}">
  <div class="product-card__image-wrap">
    <a href="product.html?id=${id}">
      <img src="assets/products/${image}" alt="${name}" loading="lazy" onerror="handleImageError(this)">
    </a>
    ${badges}
    ${discount > 0 ? `<span class="badge badge--discount">-${discount}%</span>` : ''}
    ${stock === false ? `<span class="badge badge--stock-out">Out of Stock</span>` : ''}
    <button class="product-card__quick-view" onclick="openQuickView('${id}')" aria-label="Quick view">
      👁️
    </button>
  </div>
  <div class="product-card__info">
    <div class="product-card__category">${category || ''}</div>
    <h3 class="product-card__name"><a href="product.html?id=${id}">${name}</a></h3>
    <div class="product-card__rating">
      ${generateStars(rating)}
      <span class="product-card__reviews">(${reviews || 0})</span>
    </div>
    <div class="product-card__price-row">
      <span class="product-card__price">${formatPrice(price)}</span>
      ${old_price > 0 ? `<span class="product-card__old-price">${formatPrice(old_price)}</span>` : ''}
    </div>
    ${stock === false ? '<div class="product-card__stock--out">Out of Stock</div>' : ''}
    <div class="product-card__actions">
      <button class="btn btn--primary btn--sm" onclick="addToCart('${id}')" ${stock === false ? 'disabled' : ''}>Add to Cart</button>
      <button class="btn btn--secondary btn--sm" onclick="buyNow('${id}')" ${stock === false ? 'disabled' : ''}>Buy Now</button>
    </div>
  </div>
</div>
  `;
}

function renderProductGrid(containerId, products) {
  const container = document.getElementById(containerId);
  if (!container) return;
  if (!products || products.length === 0) {
    container.innerHTML = '<p>No products found.</p>';
    return;
  }
  container.innerHTML = products.map(p => renderProductCard(p)).join('');
}

function renderPagination(containerId, currentPage, totalPages, onPageChangeName) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }
  
  let html = `<div class="pagination">`;
  
  html += `<button onclick="${onPageChangeName}(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>Prev</button>`;
  
  for (let i = 1; i <= totalPages; i++) {
    html += `<button onclick="${onPageChangeName}(${i})" class="${i === currentPage ? 'active' : ''}">${i}</button>`;
  }
  
  html += `<button onclick="${onPageChangeName}(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>Next</button>`;
  html += `</div>`;
  
  container.innerHTML = html;
}

async function openQuickView(productId) {
  const products = await fetchProducts();
  const product = products.find(p => p.id === String(productId) || p.id === Number(productId));
  if (!product) return;
  
  let modal = document.getElementById('quick-view-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'quick-view-modal';
    modal.className = 'modal-overlay';
    modal.onclick = (e) => {
      if (e.target === modal) closeQuickView();
    };
    document.body.appendChild(modal);
  }
  
  modal.innerHTML = `
    <div class="modal-content quick-view-content">
      <button class="modal-close" onclick="closeQuickView()">×</button>
      <div class="quick-view-grid" style="display:flex; gap:20px;">
        <div style="flex:1;">
           <img src="assets/products/${product.image}" style="width:100%" onerror="handleImageError(this)">
        </div>
        <div style="flex:1;">
           <h2>${product.name}</h2>
           <p>${formatPrice(product.price)}</p>
           <p>${product.description || ''}</p>
           <p>Status: ${product.stock === false ? 'Out of Stock' : 'In Stock'}</p>
           <div style="margin-top:20px;">
             <button class="btn btn--primary" onclick="addToCart('${product.id}')" ${product.stock === false ? 'disabled' : ''}>Add to Cart</button>
             <a href="product.html?id=${product.id}" class="btn">View Details</a>
           </div>
        </div>
      </div>
    </div>
  `;
  modal.style.display = 'flex';
}

function closeQuickView() {
  const modal = document.getElementById('quick-view-modal');
  if (modal) {
    modal.style.display = 'none';
  }
}

function searchProducts(query, products) {
  if (!query) return products;
  return filterProducts(products, { search: query });
}
