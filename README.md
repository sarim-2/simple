# NexaMart - Simple E-Commerce Store

A clean, minimalist e-commerce website powered by Excel product management and WhatsApp-based ordering.

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- A text editor (VS Code recommended)
- A web browser

### Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize sample products (first time only):**
   ```bash
   python build-products.py --init
   ```
   This creates `products.xlsx` with 20 sample products.

3. **Build product data:**
   ```bash
   python build-products.py
   ```
   This generates `data/products.json` from the Excel file.

4. **Open the website:**
   - Open `index.html` in your browser, OR
   - Use a local server: `python -m http.server 8000`
   - Visit: `http://localhost:8000`

### Windows Quick Update
Double-click `update-products.bat` to rebuild products from Excel.

---

## 📦 Managing Products

### Adding a New Product

1. Open `products.xlsx` in Excel/Google Sheets
2. Add a new row with product details
3. Save the file
4. Run `python build-products.py` (or double-click `update-products.bat`)
5. Refresh your website

### Excel Columns

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| id | ✅ | Unique product ID | 001 |
| name | ✅ | Product name | Wireless Headphones |
| slug | | URL-friendly name | wireless-headphones |
| category | ✅ | Product category | Electronics |
| subcategory | | Sub-category | Audio |
| description | | Full description | Premium wireless... |
| short_description | | Brief description | Wireless headphones... |
| price | ✅ | Current price (number) | 4999 |
| old_price | | Original price | 5999 |
| discount | | Discount percentage | 17 |
| image | ✅ | Main image filename | headphones.svg |
| image_2 | | Second image | headphones-2.svg |
| image_3 | | Third image | |
| stock | | IN or OUT | IN |
| stock_quantity | | Number in stock | 25 |
| popular | | Show in Popular | ON |
| featured | | Show in Featured | ON |
| sale | | Show in Sale | ON |
| new_arrival | | Show in New Arrivals | ON |
| badge | | Badge text | Best Seller |
| brand | | Brand name | SoundMax |
| sku | | SKU code | WH-001 |
| rating | | Rating (0-5) | 4.7 |
| reviews | | Review count | 124 |
| tags | | Comma-separated tags | audio,wireless |

### Product Images

1. Place images in `assets/products/`
2. Use the filename (without path) in the Excel `image` column
3. Supported formats: JPG, PNG, WEBP, SVG
4. Recommended: Square images (e.g., 800x800px)
5. Missing images show a placeholder automatically

### Controlling Website Sections from Excel

| Flag | Value | Effect |
|------|-------|--------|
| popular | ON | Shows in Popular Products section |
| featured | ON | Shows in Featured Products section |
| sale | ON | Shows in Sale section |
| new_arrival | ON | Shows in New Arrivals section |
| stock | IN | Product is available |
| stock | OUT | Product shows "Out of Stock" |

### Marking a Product as Out of Stock
- Set `stock` to `OUT`, OR
- Set `stock_quantity` to `0`

Out of stock products:
- Show "Out of Stock" label
- Have disabled Add to Cart / Buy Now buttons
- Cannot be ordered

---

## ⚙️ Configuration

Edit `js/config.js` to change:

```javascript
const CONFIG = {
  STORE_NAME: 'NexaMart',        // Your store name
  WHATSAPP_NUMBER: '923001234567', // Your WhatsApp (with country code, no +)
  EMAIL: 'hello@nexamart.com',     // Contact email
  PHONE: '+92 300 1234567',        // Display phone
  ADDRESS: 'Karachi, Pakistan',    // Store address
  DELIVERY_FEE: 200,               // Delivery fee in PKR
  FREE_DELIVERY_THRESHOLD: 5000,   // Free delivery above this amount
  CURRENCY: 'PKR',                 // Currency code
  // ... social links, etc.
};
```

---

## 📱 How Orders Work

1. Customer browses products and adds to cart
2. Customer fills checkout form (name, phone, address)
3. Customer selects payment method (COD or Online)
4. System generates a formatted WhatsApp message
5. Customer is redirected to WhatsApp with the order details
6. Store owner receives and confirms the order

---

## 🚀 Deployment

### Netlify
1. Push your project to GitHub
2. Go to [Netlify](https://netlify.com) → New Site → Import from Git
3. Select your repository
4. Build command: (leave empty)
5. Publish directory: `.` (root)
6. Click Deploy

### Vercel
1. Push your project to GitHub
2. Go to [Vercel](https://vercel.com) → New Project → Import
3. Framework: Other
4. Output directory: `.` (root)
5. Click Deploy

### GitHub Pages
1. Push your project to GitHub
2. Go to Repository → Settings → Pages
3. Source: Deploy from branch
4. Branch: main, folder: / (root)
5. Click Save

### Important
- Run `python build-products.py` BEFORE deploying
- Make sure `data/products.json` is committed/included
- After updating Excel, rebuild and redeploy

---

## 📁 Project Structure

```
├── index.html              # Homepage
├── shop.html               # Shop page with filters
├── category.html           # Category page
├── product.html            # Product detail page
├── search.html             # Search results
├── sale.html               # Sale products
├── new-arrivals.html       # New arrivals
├── cart.html               # Shopping cart
├── checkout.html           # Checkout form
├── success.html            # Order success
├── about.html              # About page
├── contact.html            # Contact page
├── faq.html                # FAQ page
├── privacy.html            # Privacy policy
├── terms.html              # Terms & conditions
├── css/
│   ├── style.css           # Main styles
│   └── responsive.css      # Responsive styles
├── js/
│   ├── config.js           # Store configuration
│   ├── app.js              # Core (header, footer, utils)
│   ├── products.js         # Product data & rendering
│   ├── cart.js             # Cart functionality
│   ├── checkout.js         # Checkout & WhatsApp
│   ├── search.js           # Search functionality
│   └── product-detail.js   # Product detail page
├── data/
│   └── products.json       # Generated product data
├── assets/
│   ├── products/           # Product images
│   ├── banners/            # Hero/banner images
│   └── placeholder.svg     # Fallback image
├── products.xlsx           # Product database (Excel)
├── build-products.py       # Excel → JSON converter
├── update-products.bat     # Windows update script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🔧 Update Workflow

```
Excel (products.xlsx)
        ↓
Build Script (python build-products.py)
        ↓
JSON (data/products.json)
        ↓
Website (static files)
        ↓
Deploy (Netlify/Vercel/GitHub Pages)
```

1. Edit `products.xlsx`
2. Save the file
3. Run `python build-products.py` or double-click `update-products.bat`
4. Test locally
5. Deploy to your hosting provider

---

## 📝 License

MIT License - Feel free to use and modify.
