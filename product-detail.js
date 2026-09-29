async function initProductPage() {
  const container = document.getElementById('product-detail-container');
  if (!container) return;

  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get('id');

  const products = await fetchProducts();
  const product = products.find(p => p.id === String(id) || p.id === Number(id));

  if (!product) {
    container.innerHTML = `
      <div style="text-align:center; padding: 100px 20px;">
        <h2>Product Not Found</h2>
        <a href="shop.html" class="btn btn--primary" style="margin-top:20px; display:inline-block;">Back to Shop</a>
      </div>
    `;
    return;
  }

  renderProductDetail(product);
  
  const related = getRelatedProducts(product, products);
  renderRelatedProducts(related);
}

function renderProductDetail(product) {
  const container = document.getElementById('product-detail-container');
  if (!container) return;

  // Assuming an array of images for gallery, otherwise fallback to single image
  const images = product.gallery || [product.image];
  
  let thumbnailsHtml = '';
  if (images.length > 1) {
    thumbnailsHtml = `
      <div class="product-gallery-thumbs" style="display:flex; gap:10px; margin-top:10px; overflow-x:auto;">
        ${images.map((img, idx) => `
          <img src="assets/products/${img}" 
               class="thumbnail ${idx === 0 ? 'active' : ''}" 
               style="width:80px; height:80px; object-fit:cover; cursor:pointer; border:2px solid ${idx===0 ? '#333' : 'transparent'};"
               onclick="changeMainImage(this, 'assets/products/${img}')"
               onerror="handleImageError(this)">
        `).join('')}
      </div>
    `;
  }

  const { id, name, category, rating, reviews, sku, price, old_price, discount, stock, description, brand } = product;

  container.innerHTML = `
    <nav class="breadcrumb" style="margin-bottom:20px; color:#666;">
      <a href="index.html">Home</a> > 
      <a href="shop.html?category=${encodeURIComponent(category || '')}">${category || 'Shop'}</a> > 
      <span>${name}</span>
    </nav>

    <div class="product-detail-grid" style="display:flex; gap:40px; flex-wrap:wrap; margin-bottom:40px;">
      <div class="product-detail-images" style="flex:1; min-width:300px;">
        <img id="main-product-image" src="assets/products/${product.image}" style="width:100%; object-fit:cover;" onerror="handleImageError(this)">
        ${thumbnailsHtml}
      </div>
      
      <div class="product-detail-info" style="flex:1; min-width:300px;">
        <div style="color:#888; text-transform:uppercase; font-size:12px; margin-bottom:5px;">${category || ''}</div>
        <h1 style="margin:0 0 10px 0; font-size:2em;">${name}</h1>
        
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
          ${generateStars(rating)}
          <span style="color:#666; font-size:14px;">(${reviews || 0} reviews)</span>
          ${sku ? `<span style="color:#ccc;">|</span> <span style="color:#666; font-size:14px;">SKU: ${sku}</span>` : ''}
        </div>

        <div style="margin-bottom:20px; display:flex; align-items:center; gap:15px;">
          <span style="font-size:2em; font-weight:bold;">${formatPrice(price)}</span>
          ${old_price > 0 ? `<span style="text-decoration:line-through; color:#999; font-size:1.2em;">${formatPrice(old_price)}</span>` : ''}
          ${discount > 0 ? `<span class="badge badge--discount" style="background:red; color:white; padding:4px 8px; border-radius:4px;">-${discount}%</span>` : ''}
        </div>

        <div style="margin-bottom:20px;">
          <strong style="color:${stock === false ? 'red' : 'green'};">
            ${stock === false ? 'Out of Stock' : 'In Stock'}
          </strong>
        </div>

        <p style="color:#555; line-height:1.6; margin-bottom:30px;">
          ${description || 'No description available.'}
        </p>

        <div style="display:flex; gap:15px; margin-bottom:30px;">
          <div style="display:flex; align-items:center; border:1px solid #ddd; border-radius:4px;">
            <button onclick="changeQty(-1)" style="padding:10px 15px; background:none; border:none; cursor:pointer; font-size:1.2em;">-</button>
            <input type="number" id="detail-qty" value="1" min="1" style="width:50px; text-align:center; border:none; font-size:1.1em; pointer-events:none;">
            <button onclick="changeQty(1)" style="padding:10px 15px; background:none; border:none; cursor:pointer; font-size:1.2em;">+</button>
          </div>
          <button class="btn btn--primary" style="flex:1; padding:15px; font-size:1.1em;" onclick="addDetailToCart('${id}')" ${stock === false ? 'disabled' : ''}>Add to Cart</button>
          <button class="btn btn--secondary" style="flex:1; padding:15px; font-size:1.1em;" onclick="buyDetailNow('${id}')" ${stock === false ? 'disabled' : ''}>Buy Now</button>
        </div>

        <hr style="border:none; border-top:1px solid #eee; margin:20px 0;">
        
        <table class="product-meta-table" style="width:100%; text-align:left; font-size:14px;">
          ${brand ? `<tr><th style="padding:5px 0; color:#666;">Brand:</th><td>${brand}</td></tr>` : ''}
          ${sku ? `<tr><th style="padding:5px 0; color:#666;">SKU:</th><td>${sku}</td></tr>` : ''}
          ${category ? `<tr><th style="padding:5px 0; color:#666;">Category:</th><td>${category}</td></tr>` : ''}
        </table>
      </div>
    </div>

    <div class="product-full-description" style="margin-bottom:50px;">
      <h2>Product Details</h2>
      <div style="line-height:1.8; color:#444; margin-top:20px;">
        ${product.long_description || description || 'More details coming soon.'}
      </div>
    </div>
  `;
}

// Global helpers for detail page
function changeMainImage(thumbEl, src) {
  document.getElementById('main-product-image').src = src;
  document.querySelectorAll('.thumbnail').forEach(el => {
    el.style.borderColor = 'transparent';
  });
  thumbEl.style.borderColor = '#333';
}

function changeQty(delta) {
  const input = document.getElementById('detail-qty');
  let val = parseInt(input.value) || 1;
  val += delta;
  if (val < 1) val = 1;
  input.value = val;
}

function addDetailToCart(id) {
  const qty = parseInt(document.getElementById('detail-qty').value) || 1;
  addToCart(id, qty);
}

async function buyDetailNow(id) {
  const qty = parseInt(document.getElementById('detail-qty').value) || 1;
  await addToCart(id, qty);
  window.location.href = 'checkout.html';
}

function getRelatedProducts(product, allProducts) {
  return allProducts.filter(p => 
    p.id !== product.id && 
    (p.category === product.category || 
     (p.tags && product.tags && p.tags.some(t => product.tags.includes(t))))
  ).slice(0, 4);
}

function renderRelatedProducts(relatedProducts) {
  let container = document.getElementById('related-products-container');
  
  if (!container) {
    // If user didn't define container in HTML, append it
    const wrapper = document.createElement('div');
    wrapper.id = 'related-products-section';
    wrapper.innerHTML = `
      <h2 style="margin-bottom:20px; text-align:center;">Related Products</h2>
      <div id="related-products-container" class="product-grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(250px, 1fr)); gap:20px;"></div>
    `;
    const detailContainer = document.getElementById('product-detail-container');
    if (detailContainer) detailContainer.appendChild(wrapper);
    container = document.getElementById('related-products-container');
  }

  if (container && relatedProducts.length > 0) {
    container.innerHTML = relatedProducts.map(p => renderProductCard(p)).join('');
  } else if (document.getElementById('related-products-section')) {
    document.getElementById('related-products-section').style.display = 'none';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname.includes('product.html') || window.location.search.includes('id=')) {
    initProductPage();
  }
});
