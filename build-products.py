import json
import os
import argparse
from openpyxl import Workbook, load_workbook
import sys

REQUIRED_COLUMNS = ['id', 'name', 'category', 'price', 'image']

def init_sample_data(filepath):
    wb = Workbook()
    ws = wb.active
    ws.title = "Products"

    headers = [
        "id", "name", "slug", "category", "subcategory", "description", 
        "short_description", "price", "old_price", "discount", "image", 
        "image_2", "image_3", "stock", "stock_quantity", "popular", 
        "featured", "sale", "new_arrival", "badge", "brand", "sku", 
        "rating", "reviews", "tags"
    ]
    ws.append(headers)

    sample_products = [
        ["001", "Wireless Headphones", "wireless-headphones", "Electronics", "Audio", "Premium wireless headphones with active noise cancellation, comfortable memory foam ear cushions, and 30-hour battery life. Perfect for music lovers and professionals.", "Wireless headphones with premium sound.", 4999, 5999, 17, "wireless-headphones.jpg", "wireless-headphones-2.jpg", "", "IN", 25, "ON", "ON", "ON", "OFF", "Best Seller", "SoundMax", "WH-001", 4.7, 124, "headphones,wireless,audio,electronics"],
        ["002", "Bluetooth Speaker", "bluetooth-speaker", "Electronics", "Audio", "Portable Bluetooth speaker with deep bass, waterproof IPX7 rating, and 12-hour playtime. Take your music anywhere.", "Portable speaker with deep bass.", 3499, 4499, 22, "bluetooth-speaker.jpg", "", "", "IN", 18, "ON", "OFF", "ON", "OFF", "Sale", "SoundMax", "BS-002", 4.5, 89, "speaker,bluetooth,audio,portable"],
        ["003", "Smart Watch", "smart-watch", "Electronics", "Wearables", "Feature-packed smart watch with heart rate monitor, GPS tracking, sleep analysis, and 7-day battery life. Stay connected on the go.", "Smart watch with health tracking.", 7999, 9999, 20, "smart-watch.jpg", "smart-watch-2.jpg", "smart-watch-3.jpg", "IN", 12, "OFF", "ON", "OFF", "ON", "New", "TechFit", "SW-003", 4.8, 203, "watch,smart,wearable,fitness"],
        ["004", "Wireless Mouse", "wireless-mouse", "Electronics", "Accessories", "Ergonomic wireless mouse with silent clicks, adjustable DPI, and USB-C rechargeable battery. Works with any device.", "Ergonomic wireless mouse.", 1499, 0, 0, "wireless-mouse.jpg", "", "", "IN", 42, "ON", "OFF", "OFF", "OFF", "", "TechFit", "WM-004", 4.3, 67, "mouse,wireless,computer,ergonomic"],
        ["005", "Oversized T-Shirt", "oversized-tshirt", "Clothing", "Men", "Premium cotton oversized t-shirt with a relaxed fit. Available in multiple colors. Soft, breathable, and perfect for everyday wear.", "Premium cotton oversized tee.", 1299, 1799, 28, "oversized-tshirt.jpg", "oversized-tshirt-2.jpg", "", "IN", 55, "ON", "OFF", "ON", "OFF", "Popular", "UrbanWear", "TS-005", 4.6, 156, "tshirt,clothing,cotton,oversized"],
        ["006", "Denim Jacket", "denim-jacket", "Clothing", "Men", "Classic denim jacket with a modern slim fit. Durable construction with copper button details and multiple pockets.", "Classic slim fit denim jacket.", 4499, 0, 0, "denim-jacket.jpg", "denim-jacket-2.jpg", "", "IN", 8, "OFF", "ON", "OFF", "OFF", "", "UrbanWear", "DJ-006", 4.4, 42, "jacket,denim,clothing,outerwear"],
        ["007", "Running Shorts", "running-shorts", "Clothing", "Sportswear", "Lightweight running shorts with moisture-wicking fabric, built-in liner, and zippered pocket. Designed for performance.", "Lightweight performance running shorts.", 999, 0, 0, "running-shorts.jpg", "", "", "IN", 30, "OFF", "OFF", "OFF", "ON", "New", "ActiveGear", "RS-007", 4.2, 31, "shorts,running,sports,activewear"],
        ["008", "Phone Stand", "phone-stand", "Gadgets", "Accessories", "Adjustable aluminum phone stand with anti-slip base. Compatible with all smartphones and small tablets. Perfect for desk setup.", "Adjustable aluminum phone stand.", 799, 999, 20, "phone-stand.jpg", "", "", "IN", 65, "ON", "OFF", "ON", "OFF", "Sale", "DeskPro", "PS-008", 4.1, 88, "phone,stand,desk,gadget,aluminum"],
        ["009", "USB-C Hub", "usb-c-hub", "Gadgets", "Accessories", "7-in-1 USB-C hub with HDMI 4K output, USB 3.0 ports, SD card reader, and 100W power delivery pass-through.", "7-in-1 USB-C hub.", 2499, 0, 0, "usb-c-hub.jpg", "usb-c-hub-2.jpg", "", "IN", 15, "OFF", "ON", "OFF", "OFF", "", "TechFit", "UCH-009", 4.6, 54, "usb,hub,gadget,computer,adapter"],
        ["010", "Portable Charger", "portable-charger", "Gadgets", "Power", "20000mAh portable charger with fast charging, dual USB-C ports, and LED display. Charge 3 devices simultaneously.", "20000mAh fast-charging power bank.", 2999, 3499, 14, "portable-charger.jpg", "", "", "IN", 22, "OFF", "OFF", "ON", "OFF", "Sale", "PowerUp", "PC-010", 4.4, 71, "charger,power,portable,battery"],
        ["011", "Desk Lamp", "desk-lamp", "Home & Living", "Lighting", "Modern LED desk lamp with adjustable brightness, color temperature control, and USB charging port. Sleek minimalist design.", "LED desk lamp with adjustable brightness.", 2199, 2999, 27, "desk-lamp.jpg", "desk-lamp-2.jpg", "", "IN", 14, "OFF", "ON", "ON", "OFF", "Sale", "HomeLux", "DL-011", 4.5, 63, "lamp,desk,led,home,lighting"],
        ["012", "Scented Candle Set", "scented-candles", "Home & Living", "Decor", "Set of 3 premium soy wax scented candles in glass jars. Fragrances: Vanilla, Lavender, and Sandalwood. Burns for 40+ hours each.", "Set of 3 premium scented candles.", 1599, 0, 0, "scented-candles.jpg", "", "", "IN", 20, "OFF", "OFF", "OFF", "ON", "New", "HomeLux", "SC-012", 4.3, 37, "candle,scented,home,decor,gift"],
        ["013", "Throw Pillow", "throw-pillow", "Home & Living", "Decor", "Soft velvet throw pillow with hidden zipper. 18x18 inches, perfect for sofa, bed, or chair. Machine washable cover.", "Soft velvet decorative throw pillow.", 899, 0, 0, "throw-pillow.jpg", "", "", "IN", 35, "ON", "OFF", "OFF", "OFF", "", "HomeLux", "TP-013", 4.0, 28, "pillow,throw,home,decor,velvet"],
        ["014", "Travel Backpack", "travel-backpack", "Accessories", "Bags", "Water-resistant travel backpack with laptop compartment, USB charging port, and anti-theft design. 30L capacity.", "Water-resistant travel backpack.", 3999, 0, 0, "travel-backpack.jpg", "travel-backpack-2.jpg", "", "IN", 10, "ON", "ON", "OFF", "OFF", "Popular", "UrbanWear", "TB-014", 4.7, 112, "backpack,travel,bag,laptop,waterproof"],
        ["015", "Minimalist Wallet", "minimalist-wallet", "Accessories", "Wallets", "Slim RFID-blocking leather wallet with 6 card slots and money clip. Fits front pocket perfectly.", "Slim RFID-blocking leather wallet.", 1499, 0, 0, "minimalist-wallet.jpg", "", "", "IN", 28, "OFF", "OFF", "OFF", "ON", "New", "UrbanWear", "MW-015", 4.2, 45, "wallet,leather,minimalist,rfid"],
        ["016", "Sunglasses", "sunglasses", "Accessories", "Eyewear", "Polarized UV400 sunglasses with lightweight titanium frame. Classic aviator style for men and women.", "Polarized aviator sunglasses.", 2299, 2999, 23, "sunglasses.jpg", "sunglasses-2.jpg", "", "IN", 17, "OFF", "OFF", "ON", "OFF", "Sale", "StyleVue", "SG-016", 4.4, 58, "sunglasses,eyewear,polarized,uv"],
        ["017", "Skincare Set", "skincare-set", "Beauty", "Skincare", "Complete skincare set with cleanser, toner, serum, and moisturizer. Suitable for all skin types. Dermatologist tested.", "Complete 4-step skincare routine.", 3499, 4499, 22, "skincare-set.jpg", "skincare-set-2.jpg", "", "IN", 9, "ON", "OFF", "ON", "OFF", "Sale", "GlowUp", "SK-017", 4.6, 93, "skincare,beauty,moisturizer,serum"],
        ["018", "Hair Styling Kit", "hair-styling-kit", "Beauty", "Hair", "Professional hair styling kit with dryer, straightener, and curling wand. Ceramic tourmaline technology for less damage.", "Professional 3-piece styling kit.", 1999, 0, 0, "hair-styling-kit.jpg", "", "", "OUT", 0, "OFF", "OFF", "OFF", "ON", "New", "GlowUp", "HSK-018", 4.1, 22, "hair,styling,beauty,dryer"],
        ["019", "Running Shoes", "running-shoes", "Sports", "Footwear", "Lightweight running shoes with responsive cushioning, breathable mesh upper, and durable rubber outsole. Perfect for daily runs.", "Lightweight responsive running shoes.", 5999, 7499, 20, "running-shoes.jpg", "running-shoes-2.jpg", "running-shoes-3.jpg", "IN", 7, "ON", "ON", "ON", "OFF", "Best Seller", "ActiveGear", "RSH-019", 4.8, 187, "shoes,running,sports,footwear"],
        ["020", "Yoga Mat", "yoga-mat", "Sports", "Fitness", "Extra thick 6mm yoga mat with non-slip surface and carrying strap. Eco-friendly TPE material. 72x24 inches.", "Extra thick non-slip yoga mat.", 1799, 0, 0, "yoga-mat.jpg", "", "", "IN", 19, "OFF", "OFF", "OFF", "ON", "New", "ActiveGear", "YM-020", 4.3, 41, "yoga,mat,fitness,sports,exercise"]
    ]

    for row in sample_products:
        ws.append(row)

    wb.save(filepath)
    print(f"Created sample products file at {filepath}")


def process_products(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return

    wb = load_workbook(filepath, data_only=True)
    ws = wb.active

    headers = []
    for col in ws.iter_cols(min_row=1, max_row=1):
        for cell in col:
            headers.append(str(cell.value).strip().lower() if cell.value else f"col_{cell.column}")

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in headers]
    if missing_cols:
        print(f"Warning: Missing required columns: {', '.join(missing_cols)}")

    products = []
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not any(row):
            continue
            
        product = {}
        for i, val in enumerate(row):
            if i < len(headers):
                product[headers[i]] = val
        
        # Convert values
        for key in ['price', 'old_price', 'discount', 'stock_quantity', 'reviews']:
            try:
                product[key] = int(product.get(key) or 0)
            except ValueError:
                try:
                    product[key] = float(product.get(key) or 0)
                except ValueError:
                    product[key] = 0

        for key in ['rating']:
            try:
                product[key] = float(product.get(key) or 0)
            except ValueError:
                product[key] = 0.0
                
        for key in ['popular', 'featured', 'sale', 'new_arrival']:
            val = str(product.get(key) or '').strip().upper()
            product[key] = val == 'ON'
            
        # tags
        tags_str = str(product.get('tags') or '')
        product['tags'] = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

        # stock
        stock_val = str(product.get('stock') or '').strip().upper()
        product['stock'] = stock_val == 'IN' or stock_val == 'TRUE' or stock_val == 'ON' or stock_val == 'YES'
        if 'stock_quantity' in product and product['stock_quantity'] <= 0:
            product['stock'] = False
            
        # Optional: ensure string formats
        for key in ['id', 'name', 'slug', 'category', 'subcategory', 'description', 
                    'short_description', 'image', 'image_2', 'image_3', 'badge', 'brand', 'sku']:
            if key in product:
                product[key] = str(product[key] or '').strip()

        # Add to list if we have at least ID and Name
        if product.get('id') and product.get('name'):
            products.append(product)

    # Make data directory
    os.makedirs('data', exist_ok=True)
    
    with open('data/products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)

    print(f"Successfully processed {len(products)} products.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build products JSON from Excel")
    parser.add_argument('--init', action='store_true', help="Initialize sample products.xlsx")
    args = parser.parse_args()

    excel_file = "products.xlsx"

    if args.init:
        if not os.path.exists(excel_file):
            init_sample_data(excel_file)
        else:
            print(f"{excel_file} already exists. Skipping init.")
    else:
        process_products(excel_file)
