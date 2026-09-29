async function initSearchPage() {
  const container = document.getElementById('search-results-container');
  const heading = document.getElementById('search-heading');
  
  if (!container) return;

  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get('q');

  if (heading) {
    heading.innerText = query ? `Search results for "${query}"` : 'Search Products';
  }

  const products = await fetchProducts();
  const results = searchProducts(query || '', products);

  if (results.length === 0) {
    container.innerHTML = `<p style="text-align:center; padding: 40px; font-size:1.2em;">No products match your search.</p>`;
  } else {
    // Re-use renderProductGrid from products.js
    renderProductGrid('search-results-container', results);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname.includes('search.html')) {
    initSearchPage();
  }
});
