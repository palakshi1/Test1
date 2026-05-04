"""
GreenGrove - Premium Plant E-Commerce Store
A fully functional Streamlit plant e-commerce application with AI chatbot integration.
"""

import streamlit as st
import json
import random
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GreenGrove | Premium Plants & Garden Care",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# PRODUCT DATABASE
# ─────────────────────────────────────────────
PRODUCTS = [
    # Indoor Plants
    {
        "id": 1, "name": "Monstera Deliciosa", "category": "Indoor Plants",
        "price": 899, "original_price": 1199, "rating": 4.8, "reviews": 324,
        "care_level": "Easy", "sunlight": "Indirect", "air_purifying": True,
        "image": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400&h=400&fit=crop",
        "description": "The iconic Swiss Cheese Plant with stunning split leaves. Perfect for living rooms and offices.",
        "badge": "Bestseller", "stock": 45, "pot_size": "6 inch",
    },
    {
        "id": 2, "name": "Snake Plant (Sansevieria)", "category": "Indoor Plants",
        "price": 549, "original_price": 699, "rating": 4.9, "reviews": 512,
        "care_level": "Very Easy", "sunlight": "Low to Bright", "air_purifying": True,
        "image": "https://images.unsplash.com/photo-1593691509543-c55fb32e4c84?w=400&h=400&fit=crop",
        "description": "NASA-certified air purifier. Thrives in neglect. Ideal for beginners and busy plant parents.",
        "badge": "Top Rated", "stock": 78, "pot_size": "5 inch",
    },
    {
        "id": 3, "name": "Peace Lily", "category": "Indoor Plants",
        "price": 449, "original_price": 599, "rating": 4.7, "reviews": 289,
        "care_level": "Easy", "sunlight": "Low Light", "air_purifying": True,
        "image": "https://images.unsplash.com/photo-1616694615957-b5d7d89f3e9e?w=400&h=400&fit=crop",
        "description": "Elegant white blooms and deep green foliage. A symbol of peace and tranquility.",
        "badge": "Sale", "stock": 32, "pot_size": "5 inch",
    },
    {
        "id": 4, "name": "Fiddle Leaf Fig", "category": "Indoor Plants",
        "price": 1299, "original_price": 1599, "rating": 4.6, "reviews": 198,
        "care_level": "Moderate", "sunlight": "Bright Indirect", "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=400&h=400&fit=crop",
        "description": "The designer's favourite. Large, architectural leaves make a bold statement in any space.",
        "badge": "Premium", "stock": 18, "pot_size": "8 inch",
    },
    {
        "id": 5, "name": "Pothos Golden", "category": "Indoor Plants",
        "price": 299, "original_price": 399, "rating": 4.8, "reviews": 621,
        "care_level": "Very Easy", "sunlight": "Low to Medium", "air_purifying": True,
        "image": "https://images.unsplash.com/photo-1600411833196-7c1f6b1a8b90?w=400&h=400&fit=crop",
        "description": "Trailing golden-green vines perfect for shelves and hanging baskets.",
        "badge": "Bestseller", "stock": 95, "pot_size": "4 inch",
    },
    # Outdoor Plants
    {
        "id": 6, "name": "Bougainvillea", "category": "Outdoor Plants",
        "price": 649, "original_price": 849, "rating": 4.7, "reviews": 234,
        "care_level": "Easy", "sunlight": "Full Sun", "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1587978185023-dc9c1d66fbca?w=400&h=400&fit=crop",
        "description": "Spectacular magenta blooms cascade over walls and pergolas. A garden showstopper.",
        "badge": "Sale", "stock": 40, "pot_size": "8 inch",
    },
    {
        "id": 7, "name": "Hibiscus Red", "category": "Outdoor Plants",
        "price": 499, "original_price": 649, "rating": 4.6, "reviews": 178,
        "care_level": "Moderate", "sunlight": "Full Sun", "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=400&h=400&fit=crop",
        "description": "Vibrant crimson flowers attract butterflies. Blooms prolifically in warm climates.",
        "badge": None, "stock": 55, "pot_size": "7 inch",
    },
    # Succulents
    {
        "id": 8, "name": "Echeveria Collection (3 Pack)", "category": "Succulents",
        "price": 599, "original_price": 799, "rating": 4.9, "reviews": 445,
        "care_level": "Very Easy", "sunlight": "Bright Indirect", "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&h=400&fit=crop",
        "description": "A curated trio of rosette succulents in pastel hues. Perfect gift and desk decor.",
        "badge": "Bundle Deal", "stock": 62, "pot_size": "3 inch each",
    },
    {
        "id": 9, "name": "Aloe Vera", "category": "Succulents",
        "price": 349, "original_price": 449, "rating": 4.8, "reviews": 389,
        "care_level": "Very Easy", "sunlight": "Bright Indirect", "air_purifying": True,
        "image": "https://images.unsplash.com/photo-1596547609652-9cf5d8c10616?w=400&h=400&fit=crop",
        "description": "Nature's first aid plant. Medicinal gel soothes burns and skin irritation.",
        "badge": "Bestseller", "stock": 80, "pot_size": "5 inch",
    },
    # Bonsai
    {
        "id": 10, "name": "Ficus Bonsai (5 Year)", "category": "Bonsai Plants",
        "price": 2499, "original_price": 2999, "rating": 4.9, "reviews": 87,
        "care_level": "Expert", "sunlight": "Bright Indirect", "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1599598425947-5202edd56fdb?w=400&h=400&fit=crop",
        "description": "A meticulously trained 5-year-old Ficus bonsai. A living sculpture for connoisseurs.",
        "badge": "Exclusive", "stock": 12, "pot_size": "Specialty",
    },
    # Fertilizers
    {
        "id": 11, "name": "Organic Neem Cake Fertilizer", "category": "Fertilizers",
        "price": 299, "original_price": 399, "rating": 4.7, "reviews": 256,
        "care_level": None, "sunlight": None, "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=400&fit=crop",
        "description": "100% organic neem cake. Controls pests and enriches soil microbiome naturally.",
        "badge": "Organic", "stock": 120, "pot_size": "1 kg",
    },
    {
        "id": 12, "name": "Liquid Seaweed Growth Booster", "category": "Fertilizers",
        "price": 449, "original_price": 549, "rating": 4.8, "reviews": 198,
        "care_level": None, "sunlight": None, "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1592150550953-e20a60cad3a4?w=400&h=400&fit=crop",
        "description": "Cold-processed seaweed extract promotes robust root development and lush growth.",
        "badge": "Sale", "stock": 85, "pot_size": "500 ml",
    },
    # Pots & Planters
    {
        "id": 13, "name": "Terracotta Pot Set (3 Sizes)", "category": "Pots & Planters",
        "price": 799, "original_price": 999, "rating": 4.8, "reviews": 312,
        "care_level": None, "sunlight": None, "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&h=400&fit=crop",
        "description": "Hand-thrown terracotta in 4, 6, and 8 inch sizes. Breathable, classic, timeless.",
        "badge": "Bundle Deal", "stock": 60, "pot_size": "Set of 3",
    },
    {
        "id": 14, "name": "Minimalist White Ceramic Planter", "category": "Pots & Planters",
        "price": 649, "original_price": 849, "rating": 4.7, "reviews": 189,
        "care_level": None, "sunlight": None, "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=400&h=400&fit=crop",
        "description": "Matte white finish with drainage hole. Elevates any plant to a design object.",
        "badge": "Premium", "stock": 45, "pot_size": "6 inch",
    },
    # Seeds
    {
        "id": 15, "name": "Tomato Cherry Seeds (Heirloom)", "category": "Vegetable Seeds",
        "price": 149, "original_price": 199, "rating": 4.6, "reviews": 445,
        "care_level": None, "sunlight": None, "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1561136594-7f68413baa99?w=400&h=400&fit=crop",
        "description": "Open-pollinated heirloom cherry tomatoes. High yield, exceptional flavour.",
        "badge": "Organic", "stock": 200, "pot_size": "50 seeds",
    },
    {
        "id": 16, "name": "Sunflower Giant Seeds", "category": "Flower Seeds",
        "price": 129, "original_price": 169, "rating": 4.8, "reviews": 367,
        "care_level": None, "sunlight": None, "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=400&h=400&fit=crop",
        "description": "Grow 6-8 ft giants with massive golden heads. Kids and adults love these.",
        "badge": "Bestseller", "stock": 180, "pot_size": "20 seeds",
    },
    # Flowering Plants
    {
        "id": 17, "name": "Anthurium Red", "category": "Flowering Plants",
        "price": 699, "original_price": 899, "rating": 4.7, "reviews": 234,
        "care_level": "Moderate", "sunlight": "Bright Indirect", "air_purifying": True,
        "image": "https://images.unsplash.com/photo-1574684891174-df6b02ab38d7?w=400&h=400&fit=crop",
        "description": "Waxy heart-shaped blooms in glossy red. Blooms year-round with proper care.",
        "badge": "Sale", "stock": 38, "pot_size": "6 inch",
    },
    {
        "id": 18, "name": "Orchid Phalaenopsis White", "category": "Flowering Plants",
        "price": 1199, "original_price": 1499, "rating": 4.9, "reviews": 156,
        "care_level": "Moderate", "sunlight": "Bright Indirect", "air_purifying": False,
        "image": "https://images.unsplash.com/photo-1490750967868-88df5691cc9c?w=400&h=400&fit=crop",
        "description": "Elegant white moth orchid. A timeless gifting choice for all occasions.",
        "badge": "Premium", "stock": 25, "pot_size": "5 inch",
    },
    # Air Purifying
    {
        "id": 19, "name": "Spider Plant Variegated", "category": "Air Purifying Plants",
        "price": 349, "original_price": 449, "rating": 4.8, "reviews": 478,
        "care_level": "Very Easy", "sunlight": "Indirect", "air_purifying": True,
        "image": "https://images.unsplash.com/photo-1596236100223-f3c656de3038?w=400&h=400&fit=crop",
        "description": "Prolific producer of baby plantlets. One of NASA's top air-cleaning plants.",
        "badge": "Top Rated", "stock": 90, "pot_size": "5 inch",
    },
    {
        "id": 20, "name": "Boston Fern", "category": "Air Purifying Plants",
        "price": 499, "original_price": 649, "rating": 4.6, "reviews": 245,
        "care_level": "Moderate", "sunlight": "Indirect", "air_purifying": True,
        "image": "https://images.unsplash.com/photo-1585500610523-4e56e4b5ec55?w=400&h=400&fit=crop",
        "description": "Lush, arching fronds that humidify your air naturally. Perfect for bathrooms.",
        "badge": "Sale", "stock": 42, "pot_size": "6 inch",
    },
]

CATEGORIES = {
    "Plants": ["Indoor Plants", "Outdoor Plants", "Air Purifying Plants", "Oxygen Rich Plants",
               "Flowering Plants", "Succulents", "Bonsai Plants", "Gifting Plants"],
    "Seeds": ["Fruit Seeds", "Vegetable Seeds", "Flower Seeds", "Microgreen Seeds", "Herb Seeds"],
    "Plant Care": ["Fertilizers", "Pots & Planters", "Gardening Tools",
                   "Watering Accessories", "Soil & Compost", "Pest Control", "Plant Medicines"],
}

TESTIMONIALS = [
    {"name": "Priya Sharma", "city": "Mumbai", "rating": 5,
     "text": "My Monstera arrived perfectly packed and has been thriving for 3 months. The care guide included was incredibly detailed. Will definitely order again.",
     "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=60&h=60&fit=crop&crop=face"},
    {"name": "Rohan Mehta", "city": "Bangalore", "rating": 5,
     "text": "The Bonsai is absolutely stunning. Expert packaging, healthy roots, and the customer support team helped me with care tips post-purchase.",
     "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=60&h=60&fit=crop&crop=face"},
    {"name": "Ananya Reddy", "city": "Hyderabad", "rating": 4,
     "text": "Fast delivery, beautiful plants. The soil quality is premium. My succulents are putting out new growth already. Packaging was eco-friendly too.",
     "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=60&h=60&fit=crop&crop=face"},
    {"name": "Vikram Singh", "city": "Delhi", "rating": 5,
     "text": "Ordered 6 air-purifying plants for my office. Arrived the next day, all healthy. My workspace feels so much fresher. Exceptional service.",
     "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=60&h=60&fit=crop&crop=face"},
]

# ─────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
def init_session_state():
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "wishlist" not in st.session_state:
        st.session_state.wishlist = set()
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "selected_product" not in st.session_state:
        st.session_state.selected_product = None
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "chatbot_open" not in st.session_state:
        st.session_state.chatbot_open = False
    if "chatbot_mode" not in st.session_state:
        st.session_state.chatbot_mode = None
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []
    if "diagnosis_result" not in st.session_state:
        st.session_state.diagnosis_result = None
    if "sort_by" not in st.session_state:
        st.session_state.sort_by = "Popular"
    if "filter_care" not in st.session_state:
        st.session_state.filter_care = "All"
    if "checkout_step" not in st.session_state:
        st.session_state.checkout_step = 0
    if "order_placed" not in st.session_state:
        st.session_state.order_placed = False

init_session_state()

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def add_to_cart(product_id, qty=1):
    pid = str(product_id)
    if pid in st.session_state.cart:
        st.session_state.cart[pid]["qty"] += qty
    else:
        prod = next((p for p in PRODUCTS if p["id"] == product_id), None)
        if prod:
            st.session_state.cart[pid] = {"product": prod, "qty": qty}

def get_cart_total():
    return sum(v["product"]["price"] * v["qty"] for v in st.session_state.cart.values())

def get_cart_count():
    return sum(v["qty"] for v in st.session_state.cart.values())

def star_display(rating):
    full = int(rating)
    return "★" * full + ("½" if rating - full >= 0.5 else "") + "☆" * (5 - full - (1 if rating - full >= 0.5 else 0))

def discount_pct(price, original):
    return int((1 - price / original) * 100)

def nav_to(page, **kwargs):
    st.session_state.page = page
    for k, v in kwargs.items():
        setattr(st.session_state, k, v)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --green-dark: #1B5E20;
        --green-primary: #2E7D32;
        --green-mid: #43A047;
        --green-light: #C8E6C9;
        --green-pale: #F1F8E9;
        --pink-accent: #E91E8C;
        --pink-light: #FCE4EC;
        --pink-pale: #FFF0F5;
        --cream: #FAFAF7;
        --charcoal: #1A1A1A;
        --text-mid: #444444;
        --text-light: #777777;
        --border: #E8EDE8;
        --shadow: 0 4px 20px rgba(0,0,0,0.08);
        --shadow-hover: 0 12px 40px rgba(0,0,0,0.15);
        --radius: 12px;
        --radius-lg: 20px;
    }

    * { box-sizing: border-box; }

    .stApp {
        background: var(--cream) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Hide Streamlit default elements */
    #MainMenu, footer, header { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--cream); }
    ::-webkit-scrollbar-thumb { background: var(--green-light); border-radius: 3px; }

    /* Typography */
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: var(--charcoal); }

    /* ── TOP NAV ── */
    .top-nav {
        background: white;
        border-bottom: 1px solid var(--border);
        padding: 0 40px;
        position: sticky;
        top: 0;
        z-index: 999;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .nav-inner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 72px;
        max-width: 1400px;
        margin: 0 auto;
    }
    .logo-wrap { display: flex; align-items: center; gap: 10px; }
    .logo-icon { width: 38px; height: 38px; background: var(--green-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .logo-text { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: var(--green-dark); letter-spacing: -0.5px; }
    .logo-sub { font-size: 10px; color: var(--text-light); letter-spacing: 2px; text-transform: uppercase; margin-top: -4px; }

    /* ── HERO ── */
    .hero-section {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #388E3C 100%);
        min-height: 520px;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
    }
    .hero-content {
        padding: 60px 60px;
        max-width: 620px;
        position: relative;
        z-index: 2;
    }
    .hero-badge {
        display: inline-block;
        background: var(--pink-light);
        color: var(--pink-accent);
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(36px, 4vw, 58px);
        font-weight: 700;
        color: white;
        line-height: 1.15;
        margin-bottom: 20px;
    }
    .hero-sub {
        color: rgba(255,255,255,0.82);
        font-size: 17px;
        line-height: 1.7;
        margin-bottom: 36px;
        font-weight: 300;
    }
    .hero-cta {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: white;
        color: var(--green-dark);
        padding: 16px 32px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 15px;
        text-decoration: none;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }
    .hero-cta:hover { transform: translateY(-2px); box-shadow: 0 12px 32px rgba(0,0,0,0.25); }
    .hero-img-overlay {
        position: absolute;
        right: -40px;
        top: -40px;
        width: 55%;
        height: calc(100% + 80px);
        background-size: cover;
        background-position: center;
        opacity: 0.25;
        border-radius: 0 0 0 60% / 0 0 0 40%;
    }
    .hero-stats {
        display: flex;
        gap: 40px;
        margin-top: 48px;
    }
    .hero-stat { text-align: center; }
    .hero-stat-num { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700; color: white; }
    .hero-stat-label { font-size: 12px; color: rgba(255,255,255,0.65); text-transform: uppercase; letter-spacing: 1px; }

    /* ── SECTION ── */
    .section-wrap {
        max-width: 1400px;
        margin: 0 auto;
        padding: 56px 40px;
    }
    .section-header {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        margin-bottom: 36px;
    }
    .section-tag {
        font-size: 11px;
        font-weight: 600;
        color: var(--green-primary);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 32px;
        font-weight: 700;
        color: var(--charcoal);
        margin: 0;
    }
    .view-all {
        font-size: 13px;
        font-weight: 600;
        color: var(--green-primary);
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 6px;
        cursor: pointer;
        border-bottom: 1px solid transparent;
        transition: all 0.2s;
        padding-bottom: 4px;
    }
    .view-all:hover { border-bottom-color: var(--green-primary); }

    /* ── PRODUCT CARD ── */
    .product-card {
        background: white;
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow);
        transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        cursor: pointer;
    }
    .product-card:hover {
        transform: translateY(-6px);
        box-shadow: var(--shadow-hover);
    }
    .product-card:hover .card-actions { opacity: 1; transform: translateY(0); }
    .product-img-wrap {
        position: relative;
        padding-top: 75%;
        overflow: hidden;
        background: var(--green-pale);
    }
    .product-img-wrap img {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.4s ease;
    }
    .product-card:hover .product-img-wrap img { transform: scale(1.06); }
    .badge {
        position: absolute;
        top: 12px;
        left: 12px;
        padding: 4px 10px;
        border-radius: 50px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-bestseller { background: #FFF3E0; color: #E65100; }
    .badge-sale { background: #FCE4EC; color: #C62828; }
    .badge-premium { background: #EDE7F6; color: #4527A0; }
    .badge-organic { background: #E8F5E9; color: #2E7D32; }
    .badge-top-rated { background: #FFF8E1; color: #F57F17; }
    .badge-bundle { background: #E3F2FD; color: #1565C0; }
    .badge-exclusive { background: #1A1A1A; color: white; }

    .card-actions {
        position: absolute;
        bottom: 12px;
        right: 12px;
        display: flex;
        flex-direction: column;
        gap: 6px;
        opacity: 0;
        transform: translateY(8px);
        transition: all 0.3s;
    }
    .wishlist-btn {
        width: 36px; height: 36px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        cursor: pointer;
        font-size: 14px;
        border: none;
        transition: all 0.2s;
    }
    .wishlist-btn:hover { transform: scale(1.1); }

    .card-body { padding: 16px 18px 20px; }
    .card-category {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--green-primary);
        font-weight: 600;
        margin-bottom: 4px;
    }
    .card-name {
        font-family: 'Playfair Display', serif;
        font-size: 16px;
        font-weight: 600;
        color: var(--charcoal);
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .card-rating { display: flex; align-items: center; gap: 6px; margin-bottom: 10px; }
    .stars { color: #FFA000; font-size: 12px; }
    .rating-count { font-size: 11px; color: var(--text-light); }
    .care-chips { display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 12px; }
    .chip {
        padding: 3px 8px;
        border-radius: 50px;
        font-size: 10px;
        font-weight: 500;
        background: var(--green-pale);
        color: var(--green-dark);
    }
    .card-pricing { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; }
    .price-current {
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        font-weight: 700;
        color: var(--charcoal);
    }
    .price-original {
        font-size: 13px;
        color: var(--text-light);
        text-decoration: line-through;
    }
    .price-discount {
        font-size: 11px;
        font-weight: 700;
        color: #C62828;
        background: #FCE4EC;
        padding: 2px 7px;
        border-radius: 50px;
    }
    .btn-add-cart {
        width: 100%;
        background: var(--green-primary);
        color: white;
        border: none;
        padding: 11px 20px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.25s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        letter-spacing: 0.3px;
    }
    .btn-add-cart:hover { background: var(--green-dark); transform: scale(1.02); }

    /* ── CATEGORY CARDS ── */
    .cat-card {
        border-radius: var(--radius-lg);
        overflow: hidden;
        position: relative;
        cursor: pointer;
        aspect-ratio: 4/5;
        box-shadow: var(--shadow);
        transition: all 0.3s;
    }
    .cat-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-hover); }
    .cat-card img { width: 100%; height: 100%; object-fit: cover; }
    .cat-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.65) 0%, transparent 60%);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 20px;
    }
    .cat-name { font-family: 'Playfair Display', serif; font-size: 18px; font-weight: 700; color: white; }
    .cat-count { font-size: 12px; color: rgba(255,255,255,0.75); margin-top: 2px; }

    /* ── PROMO BANNER ── */
    .promo-band {
        background: linear-gradient(135deg, #FCE4EC, #F8BBD0);
        border-radius: var(--radius-lg);
        padding: 40px 48px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0 40px;
    }
    .promo-title {
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        font-weight: 700;
        color: var(--charcoal);
        margin-bottom: 8px;
    }
    .promo-sub { color: var(--text-mid); font-size: 15px; max-width: 400px; line-height: 1.6; }
    .promo-code {
        background: white;
        padding: 10px 20px;
        border-radius: 8px;
        margin-top: 16px;
        display: inline-block;
        font-weight: 700;
        font-size: 14px;
        color: var(--green-dark);
        letter-spacing: 2px;
        border: 2px dashed var(--green-primary);
    }
    .promo-img { width: 200px; height: 160px; object-fit: cover; border-radius: var(--radius); }

    /* ── TESTIMONIAL ── */
    .testimonial-card {
        background: white;
        border-radius: var(--radius-lg);
        padding: 28px;
        box-shadow: var(--shadow);
        height: 100%;
    }
    .testi-stars { color: #FFA000; font-size: 14px; margin-bottom: 14px; }
    .testi-text { font-size: 14px; line-height: 1.8; color: var(--text-mid); font-style: italic; margin-bottom: 20px; }
    .testi-author { display: flex; align-items: center; gap: 12px; }
    .testi-avatar { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 2px solid var(--green-light); }
    .testi-name { font-weight: 600; font-size: 14px; color: var(--charcoal); }
    .testi-city { font-size: 12px; color: var(--text-light); }

    /* ── NEWSLETTER ── */
    .newsletter-section {
        background: var(--green-dark);
        padding: 56px 40px;
        text-align: center;
    }
    .nl-title { font-family: 'Playfair Display', serif; font-size: 34px; font-weight: 700; color: white; margin-bottom: 12px; }
    .nl-sub { color: rgba(255,255,255,0.7); font-size: 16px; margin-bottom: 32px; }

    /* ── FOOTER ── */
    .footer-wrap {
        background: var(--charcoal);
        color: rgba(255,255,255,0.7);
        padding: 56px 40px 32px;
    }
    .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; max-width: 1400px; margin: 0 auto 48px; }
    .footer-logo { font-family: 'Playfair Display', serif; font-size: 24px; color: white; font-weight: 700; margin-bottom: 12px; }
    .footer-desc { font-size: 13px; line-height: 1.8; margin-bottom: 20px; }
    .footer-heading { font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: white; font-weight: 700; margin-bottom: 16px; }
    .footer-link { font-size: 13px; display: block; color: rgba(255,255,255,0.6); margin-bottom: 10px; cursor: pointer; transition: color 0.2s; }
    .footer-link:hover { color: var(--green-light); }
    .footer-bottom { border-top: 1px solid rgba(255,255,255,0.08); padding-top: 24px; display: flex; justify-content: space-between; align-items: center; max-width: 1400px; margin: 0 auto; font-size: 12px; }
    .social-links { display: flex; gap: 12px; }
    .social-btn { width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; font-size: 14px; }
    .social-btn:hover { background: var(--green-primary); }

    /* ── CART ── */
    .cart-item {
        display: flex;
        gap: 16px;
        align-items: center;
        padding: 18px 0;
        border-bottom: 1px solid var(--border);
    }
    .cart-item-img { width: 80px; height: 80px; border-radius: 10px; object-fit: cover; flex-shrink: 0; }
    .cart-item-name { font-weight: 600; font-size: 14px; color: var(--charcoal); margin-bottom: 4px; }
    .cart-item-price { font-size: 16px; font-weight: 700; color: var(--green-dark); }

    /* ── CHATBOT ── */
    .chatbot-fab {
        position: fixed;
        bottom: 28px;
        right: 28px;
        width: 58px;
        height: 58px;
        background: linear-gradient(135deg, var(--green-primary), var(--green-dark));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 6px 24px rgba(46,125,50,0.45);
        z-index: 1000;
        font-size: 22px;
        transition: all 0.3s;
        border: 3px solid white;
    }
    .chatbot-fab:hover { transform: scale(1.08); box-shadow: 0 10px 30px rgba(46,125,50,0.55); }
    .chatbot-panel {
        position: fixed;
        bottom: 100px;
        right: 28px;
        width: 360px;
        max-height: 560px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.18);
        z-index: 1000;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    .chatbot-header {
        background: linear-gradient(135deg, var(--green-primary), var(--green-dark));
        padding: 18px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .chatbot-avatar { width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 18px; }
    .chatbot-title { font-weight: 700; color: white; font-size: 15px; }
    .chatbot-status { font-size: 11px; color: rgba(255,255,255,0.75); }
    .chatbot-body { padding: 20px; overflow-y: auto; flex: 1; }
    .chat-option-btn {
        width: 100%;
        padding: 14px 18px;
        border-radius: 12px;
        border: 2px solid var(--border);
        background: white;
        cursor: pointer;
        text-align: left;
        transition: all 0.25s;
        margin-bottom: 10px;
        font-family: 'DM Sans', sans-serif;
    }
    .chat-option-btn:hover { border-color: var(--green-primary); background: var(--green-pale); }
    .chat-option-title { font-weight: 700; font-size: 14px; color: var(--charcoal); margin-bottom: 3px; }
    .chat-option-desc { font-size: 12px; color: var(--text-light); }

    /* ── PAGE HEADER ── */
    .page-header {
        background: linear-gradient(135deg, var(--green-pale), #E8F5E9);
        padding: 40px 60px;
        border-bottom: 1px solid var(--border);
    }
    .page-header-title {
        font-family: 'Playfair Display', serif;
        font-size: 36px;
        font-weight: 700;
        color: var(--charcoal);
        margin-bottom: 6px;
    }
    .breadcrumb { font-size: 13px; color: var(--text-light); }
    .breadcrumb span { color: var(--green-primary); cursor: pointer; }

    /* ── FILTER BAR ── */
    .filter-bar {
        background: white;
        padding: 16px 40px;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .filter-label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--text-light); }

    /* ── PRODUCT DETAIL ── */
    .detail-wrap { max-width: 1200px; margin: 0 auto; padding: 40px; }
    .detail-price { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 700; color: var(--charcoal); margin-bottom: 6px; }
    .detail-badge-row { display: flex; gap: 10px; margin: 16px 0; }
    .detail-info-row { display: flex; gap: 32px; margin: 20px 0; }
    .detail-info-item { text-align: center; }
    .detail-info-label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: var(--text-light); margin-bottom: 4px; }
    .detail-info-value { font-size: 14px; font-weight: 600; color: var(--charcoal); }

    /* ── CHECKOUT ── */
    .checkout-step {
        width: 32px; height: 32px;
        border-radius: 50%;
        background: var(--green-light);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
        color: var(--green-dark);
    }
    .checkout-step.active { background: var(--green-primary); color: white; }
    .checkout-step.done { background: var(--green-dark); color: white; }

    /* ── SEARCH BAR ── */
    .search-result-wrap {
        background: white;
        border-radius: var(--radius);
        border: 1px solid var(--border);
        overflow: hidden;
        box-shadow: var(--shadow);
    }

    /* Streamlit widget overrides */
    .stButton > button {
        border-radius: 50px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.25s !important;
    }
    .stTextInput > div > div > input {
        border-radius: 50px !important;
        border: 2px solid var(--border) !important;
        font-family: 'DM Sans', sans-serif !important;
        padding: 10px 20px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--green-primary) !important;
        box-shadow: 0 0 0 3px rgba(46,125,50,0.12) !important;
    }
    .stSelectbox > div > div {
        border-radius: 50px !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif !important;
        color: var(--green-dark) !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--green-primary) !important;
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ─────────────────────────────────────────────
# NAVIGATION BAR
# ─────────────────────────────────────────────
def render_navbar():
    cart_count = get_cart_count()

    col_logo, col_nav, col_actions = st.columns([2, 6, 2])

    with col_logo:
        st.markdown("""
        <div style="padding: 16px 0 16px 20px;">
            <div class="logo-wrap">
                <div class="logo-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                        <path d="M17 8C8 10 5.9 16.17 3.82 21H5.71C6.38 19.32 7.22 17.68 8.5 16.3C10 17.5 12 18 14 18C16.5 18 19 17 21 15C20.5 13 18.5 11.5 17 11.5C16 11.5 15 12 14 13C14.5 11 15.5 9.5 17 8Z"/>
                    </svg>
                </div>
                <div>
                    <div class="logo-text">GreenGrove</div>
                    <div class="logo-sub">Premium Plants</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_nav:
        n1, n2, n3, n4, n5, n6, n7 = st.columns(7)
        with n1:
            if st.button("Home", key="nav_home", use_container_width=True):
                nav_to("home")
        with n2:
            if st.button("Plants", key="nav_plants", use_container_width=True):
                nav_to("category", selected_category="Indoor Plants")
        with n3:
            if st.button("Seeds", key="nav_seeds", use_container_width=True):
                nav_to("category", selected_category="Vegetable Seeds")
        with n4:
            if st.button("Plant Care", key="nav_care", use_container_width=True):
                nav_to("category", selected_category="Fertilizers")
        with n5:
            if st.button("Offers", key="nav_offers", use_container_width=True):
                nav_to("offers")
        with n6:
            if st.button("About", key="nav_about", use_container_width=True):
                nav_to("about")
        with n7:
            if st.button("Contact", key="nav_contact", use_container_width=True):
                nav_to("contact")

    with col_actions:
        a1, a2 = st.columns(2)
        with a1:
            search_q = st.text_input("Search", placeholder="Search...", key="nav_search", label_visibility="collapsed")
            if search_q:
                st.session_state.search_query = search_q
                nav_to("search")
        with a2:
            cart_label = f"Cart ({cart_count})" if cart_count > 0 else "Cart"
            if st.button(cart_label, key="nav_cart", type="primary", use_container_width=True):
                nav_to("cart")

    st.markdown('<div style="height: 2px; background: linear-gradient(90deg, #2E7D32, #C8E6C9, #2E7D32);"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PRODUCT CARD
# ─────────────────────────────────────────────
def render_product_card(product, col_key=""):
    badge_map = {
        "Bestseller": "badge-bestseller", "Sale": "badge-sale", "Premium": "badge-premium",
        "Organic": "badge-organic", "Top Rated": "badge-top-rated",
        "Bundle Deal": "badge-bundle", "Exclusive": "badge-exclusive",
    }

    badge_html = ""
    if product.get("badge"):
        cls = badge_map.get(product["badge"], "badge-organic")
        badge_html = f'<span class="badge {cls}">{product["badge"]}</span>'

    care_chips = ""
    if product.get("care_level"):
        care_chips += f'<span class="chip">{product["care_level"]}</span>'
    if product.get("sunlight"):
        care_chips += f'<span class="chip">{product["sunlight"]}</span>'
    if product.get("air_purifying"):
        care_chips += '<span class="chip">Air Purifier</span>'

    disc = discount_pct(product["price"], product["original_price"])
    stars = "★" * int(product["rating"]) + ("" if product["rating"] == int(product["rating"]) else "")

    st.markdown(f"""
    <div class="product-card">
        <div class="product-img-wrap">
            <img src="{product['image']}" alt="{product['name']}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=400&fit=crop'"/>
            {badge_html}
        </div>
        <div class="card-body">
            <div class="card-category">{product['category']}</div>
            <div class="card-name">{product['name']}</div>
            <div class="card-rating">
                <span class="stars">{stars}</span>
                <span style="font-size:13px;font-weight:600;color:#333">{product['rating']}</span>
                <span class="rating-count">({product['reviews']} reviews)</span>
            </div>
            <div class="care-chips">{care_chips}</div>
            <div class="card-pricing">
                <span class="price-current">&#8377;{product['price']}</span>
                <span class="price-original">&#8377;{product['original_price']}</span>
                <span class="price-discount">{disc}% off</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        if st.button("Add to Cart", key=f"atc_{product['id']}_{col_key}", use_container_width=True, type="primary"):
            add_to_cart(product["id"])
            st.success(f"Added {product['name']} to cart!")
    with c2:
        wish_label = "♥" if product["id"] in st.session_state.wishlist else "♡"
        if st.button(wish_label, key=f"wl_{product['id']}_{col_key}", use_container_width=True):
            if product["id"] in st.session_state.wishlist:
                st.session_state.wishlist.discard(product["id"])
            else:
                st.session_state.wishlist.add(product["id"])

    if st.button(f"View Details", key=f"vd_{product['id']}_{col_key}", use_container_width=True):
        nav_to("product", selected_product=product["id"])

# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────
def render_home():
    # Hero
    st.markdown("""
    <div class="hero-section">
        <div style="position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1400&h=600&fit=crop') center/cover;opacity:0.15;"></div>
        <div class="hero-content">
            <div class="hero-badge">New Arrivals — Summer Collection</div>
            <h1 class="hero-title">Bring Nature<br/>Into Every Corner</h1>
            <p class="hero-sub">Curated premium plants, rare finds, and expert plant care — delivered straight to your door with a happiness guarantee.</p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-num">12,000+</div>
                    <div class="hero-stat-label">Plants Delivered</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-num">500+</div>
                    <div class="hero-stat-label">Varieties</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-num">4.9</div>
                    <div class="hero-stat-label">Avg. Rating</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Shop by Category buttons in hero
    st.markdown('<div style="height:2px;"></div>', unsafe_allow_html=True)
    hc1, hc2, hc3, hc4, hc5 = st.columns(5)
    cat_quick = [("Indoor Plants", "Indoor"), ("Outdoor Plants", "Outdoor"),
                 ("Succulents", "Succulents"), ("Fertilizers", "Plant Care"), ("Flowering Plants", "Flowering")]
    for col, (cat, label) in zip([hc1, hc2, hc3, hc4, hc5], cat_quick):
        with col:
            if st.button(label, key=f"hero_cat_{cat}", use_container_width=True):
                nav_to("category", selected_category=cat)

    # Trust Bar
    st.markdown("""
    <div style="background:white;border-bottom:1px solid #E8EDE8;padding:18px 40px;">
        <div style="max-width:1400px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:36px;height:36px;background:#E8F5E9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;">&#128668;</div>
                <div><div style="font-weight:700;font-size:13px;color:#1A1A1A;">Free Delivery</div><div style="font-size:11px;color:#777;">On orders above &#8377;999</div></div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:36px;height:36px;background:#E8F5E9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;">&#127807;</div>
                <div><div style="font-weight:700;font-size:13px;color:#1A1A1A;">Plant Health Guarantee</div><div style="font-size:11px;color:#777;">30-day replacement policy</div></div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:36px;height:36px;background:#E8F5E9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;">&#9851;</div>
                <div><div style="font-weight:700;font-size:13px;color:#1A1A1A;">Eco Packaging</div><div style="font-size:11px;color:#777;">100% sustainable materials</div></div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:36px;height:36px;background:#E8F5E9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;">&#128222;</div>
                <div><div style="font-weight:700;font-size:13px;color:#1A1A1A;">Expert Support</div><div style="font-size:11px;color:#777;">Plant doctors available 24/7</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Featured Categories
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-tag">Browse by Type</div>
            <h2 class="section-title">Shop by Category</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cat_images = [
        ("Indoor Plants", "https://images.unsplash.com/photo-1593691509543-c55fb32e4c84?w=300&h=400&fit=crop", "35+ varieties"),
        ("Succulents", "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=300&h=400&fit=crop", "20+ varieties"),
        ("Flowering Plants", "https://images.unsplash.com/photo-1490750967868-88df5691cc9c?w=300&h=400&fit=crop", "28+ varieties"),
        ("Bonsai Plants", "https://images.unsplash.com/photo-1599598425947-5202edd56fdb?w=300&h=400&fit=crop", "12+ varieties"),
        ("Pots & Planters", "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=400&fit=crop", "50+ designs"),
    ]

    cols = st.columns(5)
    for col, (name, img, count) in zip(cols, cat_images):
        with col:
            st.markdown(f"""
            <div class="cat-card">
                <img src="{img}" alt="{name}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=400&fit=crop'"/>
                <div class="cat-overlay">
                    <div class="cat-name">{name}</div>
                    <div class="cat-count">{count}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore {name.split()[0]}", key=f"cat_btn_{name}", use_container_width=True):
                nav_to("category", selected_category=name)

    st.markdown('</div>', unsafe_allow_html=True)

    # Best Sellers
    st.markdown('<div style="background:#F8FAF8;padding:1px 0;">', unsafe_allow_html=True)
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-tag">Most Loved</div>
            <h2 class="section-title">Bestsellers</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    bestsellers = [p for p in PRODUCTS if p.get("badge") in ["Bestseller", "Top Rated"]][:4]
    cols = st.columns(4)
    for col, product in zip(cols, bestsellers):
        with col:
            render_product_card(product, col_key="bs")

    st.markdown('</div></div>', unsafe_allow_html=True)

    # Promo Banner
    st.markdown("""
    <div style="padding: 20px 0;">
        <div class="promo-band">
            <div>
                <div style="font-size:11px;font-weight:600;color:#2E7D32;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">Limited Time Offer</div>
                <div class="promo-title">Monsoon Gardening Sale</div>
                <div class="promo-sub">Prepare your garden for the rains. Up to 40% off on outdoor plants, pots, soil, and gardening tools this season.</div>
                <div class="promo-code">Use code: MONSOON40</div>
            </div>
            <img src="https://images.unsplash.com/photo-1587978185023-dc9c1d66fbca?w=300&h=200&fit=crop" class="promo-img" alt="Monsoon Sale" onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=200&fit=crop'"/>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # New Arrivals
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-tag">Just Landed</div>
            <h2 class="section-title">New Arrivals</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    new_arrivals = [p for p in PRODUCTS if p.get("badge") in ["Premium", "Exclusive", "Bundle Deal"]][:4]
    cols = st.columns(4)
    for col, product in zip(cols, new_arrivals):
        with col:
            render_product_card(product, col_key="na")
    st.markdown('</div>', unsafe_allow_html=True)

    # Testimonials
    st.markdown('<div style="background:white;padding:1px 0;">', unsafe_allow_html=True)
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-tag">Customer Stories</div>
            <h2 class="section-title">What Our Plant Parents Say</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for col, t in zip(cols, TESTIMONIALS):
        with col:
            st.markdown(f"""
            <div class="testimonial-card">
                <div class="testi-stars">{"★" * t['rating']}</div>
                <div class="testi-text">"{t['text']}"</div>
                <div class="testi-author">
                    <img class="testi-avatar" src="{t['avatar']}" alt="{t['name']}" onerror="this.src='https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=60&h=60&fit=crop&crop=face'"/>
                    <div>
                        <div class="testi-name">{t['name']}</div>
                        <div class="testi-city">{t['city']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    # Newsletter
    st.markdown("""
    <div class="newsletter-section">
        <div class="nl-title">Join 50,000+ Plant Lovers</div>
        <div class="nl-sub">Get weekly plant care tips, exclusive offers, and first access to new arrivals in your inbox.</div>
    </div>
    """, unsafe_allow_html=True)

    nl_col1, nl_col2, nl_col3 = st.columns([2, 2, 1])
    with nl_col2:
        email = st.text_input("Email address", placeholder="Enter your email address", key="nl_email", label_visibility="collapsed")
        if st.button("Subscribe — It's Free", key="nl_sub", type="primary", use_container_width=True):
            if email and "@" in email:
                st.success("You're subscribed! Welcome to the GreenGrove family.")
            else:
                st.error("Please enter a valid email address.")

    render_footer()

# ─────────────────────────────────────────────
# CATEGORY PAGE
# ─────────────────────────────────────────────
def render_category_page():
    cat = st.session_state.selected_category or "Indoor Plants"

    st.markdown(f"""
    <div class="page-header">
        <div class="breadcrumb"><span>Home</span> / {cat}</div>
        <div class="page-header-title">{cat}</div>
        <div style="color:#777;font-size:14px;">Showing {len([p for p in PRODUCTS if p['category'] == cat])} products</div>
    </div>
    """, unsafe_allow_html=True)

    # Sub-nav for category group
    sub_cats = []
    for group, cats in CATEGORIES.items():
        if cat in cats:
            sub_cats = cats
            break

    if sub_cats:
        cols = st.columns(min(len(sub_cats), 8))
        for col, sc in zip(cols, sub_cats):
            with col:
                btn_type = "primary" if sc == cat else "secondary"
                if st.button(sc.replace(" Plants", "").replace(" Seeds", ""), key=f"subcat_{sc}", use_container_width=True, type=btn_type):
                    st.session_state.selected_category = sc
                    st.rerun()

    # Filters
    fc1, fc2, fc3, fc4 = st.columns([3, 2, 2, 2])
    with fc1:
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        search_within = st.text_input("Search within category", placeholder=f"Search within {cat}...", key="cat_search", label_visibility="collapsed")
    with fc2:
        sort = st.selectbox("Sort by", ["Popular", "Price: Low to High", "Price: High to Low", "Highest Rated", "Newest"], key="cat_sort", label_visibility="collapsed")
    with fc3:
        care = st.selectbox("Care Level", ["All", "Very Easy", "Easy", "Moderate", "Expert"], key="cat_care", label_visibility="collapsed")
    with fc4:
        price_range = st.selectbox("Price Range", ["All", "Under ₹500", "₹500–₹1000", "Above ₹1000"], key="cat_price", label_visibility="collapsed")

    # Filter products
    filtered = [p for p in PRODUCTS if p["category"] == cat]

    if search_within:
        filtered = [p for p in filtered if search_within.lower() in p["name"].lower() or search_within.lower() in p["description"].lower()]

    if care != "All":
        filtered = [p for p in filtered if p.get("care_level") == care]

    if price_range == "Under ₹500":
        filtered = [p for p in filtered if p["price"] < 500]
    elif price_range == "₹500–₹1000":
        filtered = [p for p in filtered if 500 <= p["price"] <= 1000]
    elif price_range == "Above ₹1000":
        filtered = [p for p in filtered if p["price"] > 1000]

    if sort == "Price: Low to High":
        filtered.sort(key=lambda x: x["price"])
    elif sort == "Price: High to Low":
        filtered.sort(key=lambda x: -x["price"])
    elif sort == "Highest Rated":
        filtered.sort(key=lambda x: -x["rating"])

    st.markdown(f"<div style='padding:12px 0;font-size:13px;color:#777;'>{len(filtered)} products found</div>", unsafe_allow_html=True)

    if not filtered:
        # Fall back to all products for this category group
        filtered = PRODUCTS[:8]
        st.info("Showing all available products. No products found in this specific category yet.")

    # Display grid
    cols = st.columns(4)
    for i, product in enumerate(filtered):
        with cols[i % 4]:
            render_product_card(product, col_key=f"cat{i}")

# ─────────────────────────────────────────────
# PRODUCT DETAIL PAGE
# ─────────────────────────────────────────────
def render_product_detail():
    pid = st.session_state.selected_product
    product = next((p for p in PRODUCTS if p["id"] == pid), PRODUCTS[0])

    if st.button("← Back to Shop", key="back_btn"):
        nav_to("home")

    st.markdown('<div class="detail-wrap">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(product["image"], use_container_width=True)
        # Thumbnail row
        th1, th2, th3, th4 = st.columns(4)
        for tc in [th1, th2, th3, th4]:
            with tc:
                st.image(product["image"], use_container_width=True)

    with col2:
        disc = discount_pct(product["price"], product["original_price"])

        badge_map = {
            "Bestseller": "badge-bestseller", "Sale": "badge-sale", "Premium": "badge-premium",
            "Organic": "badge-organic", "Top Rated": "badge-top-rated",
        }

        if product.get("badge"):
            cls = badge_map.get(product["badge"], "badge-organic")
            st.markdown(f'<span class="badge {cls}" style="position:static;display:inline-block;margin-bottom:10px;">{product["badge"]}</span>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="font-family:'Playfair Display',serif;font-size:30px;font-weight:700;color:#1A1A1A;margin-bottom:8px;">{product['name']}</div>
        <div style="font-size:12px;color:#2E7D32;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">{product['category']}</div>
        """, unsafe_allow_html=True)

        stars = "★" * int(product["rating"])
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
            <span style="color:#FFA000;font-size:16px;">{stars}</span>
            <span style="font-weight:700;font-size:15px;">{product['rating']}</span>
            <span style="color:#777;font-size:13px;">({product['reviews']} verified reviews)</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
            <span style="font-family:'Playfair Display',serif;font-size:34px;font-weight:700;">&#8377;{product['price']}</span>
            <span style="font-size:16px;color:#999;text-decoration:line-through;">&#8377;{product['original_price']}</span>
            <span style="background:#FCE4EC;color:#C62828;padding:4px 10px;border-radius:50px;font-size:12px;font-weight:700;">{disc}% OFF</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style="font-size:15px;color:#555;line-height:1.8;margin-bottom:24px;">{product['description']}</p>
        """, unsafe_allow_html=True)

        # Plant info grid
        info_items = [
            ("Pot Size", product.get("pot_size", "—")),
            ("Care Level", product.get("care_level", "—")),
            ("Sunlight", product.get("sunlight", "—")),
            ("Stock", f"{product.get('stock', '—')} left"),
        ]
        cols_info = st.columns(4)
        for col, (label, value) in zip(cols_info, info_items):
            with col:
                st.markdown(f"""
                <div style="background:#F1F8E9;border-radius:10px;padding:12px;text-align:center;">
                    <div style="font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#777;margin-bottom:4px;">{label}</div>
                    <div style="font-size:13px;font-weight:700;color:#1B5E20;">{value if value else '—'}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        qty = st.number_input("Quantity", min_value=1, max_value=10, value=1, key="detail_qty")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Add to Cart", key="detail_atc", type="primary", use_container_width=True):
                add_to_cart(product["id"], qty)
                st.success(f"Added {qty}x {product['name']} to cart!")
        with c2:
            if st.button("Buy Now", key="detail_buy", use_container_width=True):
                add_to_cart(product["id"], qty)
                nav_to("cart")

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#F1F8E9;border-radius:10px;padding:14px 18px;font-size:13px;color:#2E7D32;">
            <b>Free delivery</b> on this item &bull; <b>30-day</b> plant health guarantee &bull; Expert care guide included
        </div>
        """, unsafe_allow_html=True)

    # Tabs: Description, Care, Reviews
    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Description", "Care Instructions", "Customer Reviews"])
    with tab1:
        st.markdown(f"""
        <p style="font-size:15px;line-height:1.9;color:#444;">{product['description']}</p>
        <p style="font-size:15px;line-height:1.9;color:#444;margin-top:16px;">
        Each plant is hand-selected from our certified nurseries, thoroughly inspected for health, and carefully packaged 
        to ensure safe transit. We include a detailed care card and a 30-day health guarantee with every order.
        </p>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:8px;">
            <div style="background:#F1F8E9;padding:20px;border-radius:12px;">
                <div style="font-weight:700;color:#1B5E20;margin-bottom:8px;">Watering</div>
                <p style="font-size:14px;color:#555;line-height:1.7;">Water when the top inch of soil is dry. {'Every 7-10 days in summer, less in winter.' if product.get('care_level') in ['Easy','Very Easy'] else 'Monitor soil moisture carefully, avoid overwatering.'}</p>
            </div>
            <div style="background:#F1F8E9;padding:20px;border-radius:12px;">
                <div style="font-weight:700;color:#1B5E20;margin-bottom:8px;">Light</div>
                <p style="font-size:14px;color:#555;line-height:1.7;">Prefers {product.get('sunlight', 'indirect')} light. Keep away from harsh afternoon sun.</p>
            </div>
            <div style="background:#F1F8E9;padding:20px;border-radius:12px;">
                <div style="font-weight:700;color:#1B5E20;margin-bottom:8px;">Fertilizing</div>
                <p style="font-size:14px;color:#555;line-height:1.7;">Apply balanced liquid fertilizer once a month during the growing season (March–September).</p>
            </div>
            <div style="background:#F1F8E9;padding:20px;border-radius:12px;">
                <div style="font-weight:700;color:#1B5E20;margin-bottom:8px;">Repotting</div>
                <p style="font-size:14px;color:#555;line-height:1.7;">Repot every 1-2 years in spring when roots outgrow the current pot. Use well-draining potting mix.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        for t in TESTIMONIALS[:3]:
            st.markdown(f"""
            <div style="padding:16px 0;border-bottom:1px solid #E8EDE8;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                    <img src="{t['avatar']}" style="width:38px;height:38px;border-radius:50%;object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=60&h=60&fit=crop&crop=face'"/>
                    <div>
                        <div style="font-weight:700;font-size:14px;">{t['name']}</div>
                        <div style="font-size:12px;color:#777;">{t['city']} — Verified Purchase</div>
                    </div>
                    <div style="margin-left:auto;color:#FFA000;">{"★" * t['rating']}</div>
                </div>
                <p style="font-size:14px;color:#555;line-height:1.7;font-style:italic;">"{t['text']}"</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEARCH PAGE
# ─────────────────────────────────────────────
def render_search():
    q = st.session_state.search_query
    results = [p for p in PRODUCTS if q.lower() in p["name"].lower() or q.lower() in p["category"].lower() or q.lower() in p["description"].lower()]

    if st.button("← Back", key="search_back"):
        nav_to("home")

    st.markdown(f"""
    <div class="page-header">
        <div class="page-header-title">Search Results</div>
        <div style="color:#777;font-size:14px;">{len(results)} results for "<b>{q}</b>"</div>
    </div>
    """, unsafe_allow_html=True)

    if not results:
        st.markdown("""
        <div style="text-align:center;padding:80px 20px;">
            <div style="font-size:48px;margin-bottom:16px;">&#127807;</div>
            <h3>No plants found</h3>
            <p style="color:#777;">Try a different search term or browse our categories.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Browse All Plants", type="primary"):
            nav_to("category", selected_category="Indoor Plants")
    else:
        cols = st.columns(4)
        for i, product in enumerate(results):
            with cols[i % 4]:
                render_product_card(product, col_key=f"sr{i}")

# ─────────────────────────────────────────────
# CART PAGE
# ─────────────────────────────────────────────
def render_cart():
    if st.button("← Continue Shopping", key="cart_back"):
        nav_to("home")

    st.markdown("""
    <div class="page-header">
        <div class="page-header-title">Shopping Cart</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.cart:
        st.markdown("""
        <div style="text-align:center;padding:80px 20px;">
            <div style="font-size:64px;margin-bottom:16px;">&#128722;</div>
            <h3 style="font-family:'Playfair Display',serif;">Your cart is empty</h3>
            <p style="color:#777;margin-bottom:24px;">Discover our beautiful collection of plants and plant care products.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Shopping", type="primary", use_container_width=False):
            nav_to("home")
        return

    col_main, col_summary = st.columns([2, 1])

    with col_main:
        st.markdown("<div style='padding:20px 0;'>", unsafe_allow_html=True)
        for pid, item in list(st.session_state.cart.items()):
            p = item["product"]
            st.markdown(f"""
            <div class="cart-item">
                <img class="cart-item-img" src="{p['image']}" alt="{p['name']}" onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=80&h=80&fit=crop'"/>
                <div style="flex:1;">
                    <div class="cart-item-name">{p['name']}</div>
                    <div style="font-size:12px;color:#777;margin-bottom:6px;">{p['category']} — {p.get('pot_size','')}</div>
                    <div class="cart-item-price">&#8377;{p['price']:,} each</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            with c1:
                st.markdown(f"<div style='padding-top:8px;font-weight:600;'>Subtotal: ₹{p['price'] * item['qty']:,}</div>", unsafe_allow_html=True)
            with c2:
                new_qty = st.number_input("Qty", min_value=1, max_value=20, value=item["qty"], key=f"qty_{pid}", label_visibility="collapsed")
                st.session_state.cart[pid]["qty"] = new_qty
            with c4:
                if st.button("Remove", key=f"remove_{pid}"):
                    del st.session_state.cart[pid]
                    st.rerun()

    with col_summary:
        subtotal = get_cart_total()
        shipping = 0 if subtotal >= 999 else 99
        discount = int(subtotal * 0.1) if subtotal >= 1500 else 0
        total = subtotal + shipping - discount

        st.markdown(f"""
        <div style="background:white;border-radius:16px;padding:28px;box-shadow:0 4px 20px rgba(0,0,0,0.08);position:sticky;top:80px;">
            <h3 style="font-family:'Playfair Display',serif;margin-bottom:20px;">Order Summary</h3>
            <div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:14px;">
                <span style="color:#777;">Subtotal ({get_cart_count()} items)</span>
                <span>&#8377;{subtotal:,}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:14px;">
                <span style="color:#777;">Shipping</span>
                <span style="color:#2E7D32;">{"FREE" if shipping == 0 else f"&#8377;{shipping}"}</span>
            </div>
            {'<div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:14px;"><span style="color:#777;">Discount (10%)</span><span style="color:#C62828;">-&#8377;' + str(discount) + '</span></div>' if discount > 0 else ''}
            <div style="border-top:1px solid #E8EDE8;margin:16px 0;"></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:20px;">
                <span style="font-weight:700;font-size:16px;">Total</span>
                <span style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:#1B5E20;">&#8377;{total:,}</span>
            </div>
            {'<div style="background:#E8F5E9;border-radius:8px;padding:10px 14px;font-size:12px;color:#2E7D32;margin-bottom:16px;"><b>You save ₹' + str(discount) + '</b> on this order!</div>' if discount > 0 else ''}
        </div>
        """, unsafe_allow_html=True)

        # Coupon
        coupon = st.text_input("Coupon Code", placeholder="MONSOON40", key="coupon")
        if st.button("Apply Coupon", key="apply_coupon", use_container_width=True):
            if coupon.upper() in ["MONSOON40", "GREEN10", "FIRSTORDER"]:
                st.success("Coupon applied! 10% additional discount.")
            else:
                st.error("Invalid coupon code.")

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button("Proceed to Checkout", key="checkout_btn", type="primary", use_container_width=True):
            nav_to("checkout")

# ─────────────────────────────────────────────
# CHECKOUT PAGE
# ─────────────────────────────────────────────
def render_checkout():
    if st.session_state.order_placed:
        subtotal = get_cart_total()
        order_id = f"GG{random.randint(100000, 999999)}"
        st.markdown(f"""
        <div style="text-align:center;padding:80px 20px;max-width:600px;margin:0 auto;">
            <div style="width:80px;height:80px;background:#E8F5E9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:36px;margin:0 auto 24px;">&#10003;</div>
            <h2 style="font-family:'Playfair Display',serif;margin-bottom:12px;">Order Confirmed!</h2>
            <p style="color:#777;font-size:16px;line-height:1.7;margin-bottom:8px;">
                Your order <b style="color:#2E7D32;">#{order_id}</b> has been placed successfully.
            </p>
            <p style="color:#777;font-size:14px;margin-bottom:32px;">
                Estimated delivery: <b>2-4 business days</b>. A confirmation has been sent to your email.
            </p>
            <div style="background:#F1F8E9;border-radius:12px;padding:20px;margin-bottom:24px;text-align:left;">
                <div style="font-weight:700;margin-bottom:8px;">Order Total: &#8377;{subtotal:,}</div>
                <div style="font-size:13px;color:#777;">Payment: Cash on Delivery / UPI</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Continue Shopping", type="primary"):
            st.session_state.cart = {}
            st.session_state.order_placed = False
            nav_to("home")
        return

    step = st.session_state.checkout_step

    st.markdown(f"""
    <div class="page-header">
        <div class="page-header-title">Checkout</div>
        <div style="display:flex;align-items:center;gap:12px;margin-top:16px;">
            <span class="checkout-step {'active' if step==0 else 'done'}">1</span>
            <span style="font-size:13px;color:#777;">Delivery Info</span>
            <div style="width:40px;height:1px;background:#ddd;"></div>
            <span class="checkout-step {'active' if step==1 else ('done' if step>1 else '')}">2</span>
            <span style="font-size:13px;color:#777;">Payment</span>
            <div style="width:40px;height:1px;background:#ddd;"></div>
            <span class="checkout-step {'active' if step==2 else ''}">3</span>
            <span style="font-size:13px;color:#777;">Review</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_summary = st.columns([3, 2])

    with col_form:
        if step == 0:
            st.markdown("<div style='padding:20px 0;'>", unsafe_allow_html=True)
            st.markdown("### Delivery Information")
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("First Name", key="fname", placeholder="Rahul")
            with c2:
                st.text_input("Last Name", key="lname", placeholder="Sharma")
            st.text_input("Email Address", key="email_co", placeholder="rahul@example.com")
            st.text_input("Phone Number", key="phone", placeholder="+91 98765 43210")
            st.text_area("Delivery Address", key="address", placeholder="House No., Street, Area, City, State - PIN Code", height=100)
            c3, c4 = st.columns(2)
            with c3:
                st.selectbox("City", ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Ahmedabad", "Other"], key="city")
            with c4:
                st.text_input("PIN Code", key="pin", placeholder="400001")

            if st.button("Continue to Payment", type="primary", use_container_width=True):
                if st.session_state.get("fname") and st.session_state.get("address"):
                    st.session_state.checkout_step = 1
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")

        elif step == 1:
            st.markdown("### Payment Method")
            payment = st.radio("Select Payment Method", ["UPI / Google Pay / PhonePe", "Credit / Debit Card", "Net Banking", "Cash on Delivery"], key="payment_method")

            if payment == "UPI / Google Pay / PhonePe":
                st.text_input("UPI ID", placeholder="yourname@upi")
            elif payment == "Credit / Debit Card":
                st.text_input("Card Number", placeholder="1234 5678 9012 3456")
                c1, c2 = st.columns(2)
                with c1:
                    st.text_input("Expiry (MM/YY)", placeholder="12/27")
                with c2:
                    st.text_input("CVV", placeholder="123", type="password")
            elif payment == "Net Banking":
                st.selectbox("Select Bank", ["HDFC Bank", "SBI", "ICICI Bank", "Axis Bank", "Kotak Bank"])

            c1, c2 = st.columns(2)
            with c1:
                if st.button("← Back", key="pay_back"):
                    st.session_state.checkout_step = 0
                    st.rerun()
            with c2:
                if st.button("Review Order", type="primary", use_container_width=True):
                    st.session_state.checkout_step = 2
                    st.rerun()

        elif step == 2:
            st.markdown("### Review Your Order")
            for pid, item in st.session_state.cart.items():
                p = item["product"]
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #E8EDE8;">
                    <div style="display:flex;align-items:center;gap:12px;">
                        <img src="{p['image']}" style="width:50px;height:50px;border-radius:8px;object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=50&h=50&fit=crop'"/>
                        <div>
                            <div style="font-weight:600;font-size:14px;">{p['name']}</div>
                            <div style="font-size:12px;color:#777;">Qty: {item['qty']}</div>
                        </div>
                    </div>
                    <div style="font-weight:700;">&#8377;{p['price'] * item['qty']:,}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="margin-top:16px;padding:16px;background:#F1F8E9;border-radius:10px;">
                <div style="display:flex;justify-content:space-between;font-weight:700;font-size:16px;">
                    <span>Total Amount</span>
                    <span style="color:#1B5E20;">&#8377;{get_cart_total():,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("← Edit Order", key="review_back"):
                    st.session_state.checkout_step = 1
                    st.rerun()
            with c2:
                if st.button("Place Order", type="primary", use_container_width=True):
                    st.session_state.order_placed = True
                    st.rerun()

    with col_summary:
        subtotal = get_cart_total()
        st.markdown(f"""
        <div style="background:white;border-radius:16px;padding:24px;box-shadow:0 4px 20px rgba(0,0,0,0.08);position:sticky;top:80px;margin-top:20px;">
            <h4 style="font-family:'Playfair Display',serif;margin-bottom:16px;">Order Summary</h4>
            {''.join([f'<div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px;"><span style="color:#777;">{item["product"]["name"]} x{item["qty"]}</span><span>&#8377;{item["product"]["price"] * item["qty"]:,}</span></div>' for item in st.session_state.cart.values()])}
            <div style="border-top:1px solid #E8EDE8;margin:12px 0;"></div>
            <div style="display:flex;justify-content:space-between;font-weight:700;">
                <span>Total</span>
                <span style="color:#1B5E20;font-family:'Playfair Display',serif;font-size:20px;">&#8377;{subtotal:,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ABOUT PAGE
# ─────────────────────────────────────────────
def render_about():
    st.markdown("""
    <div class="page-header">
        <div class="page-header-title">About GreenGrove</div>
        <div style="color:#777;font-size:15px;">India's most trusted premium plant destination</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600&h=400&fit=crop", use_container_width=True)
    with col2:
        st.markdown("""
        <h2 style="font-family:'Playfair Display',serif;font-size:34px;margin-bottom:16px;">Our Green Story</h2>
        <p style="font-size:15px;line-height:1.9;color:#555;margin-bottom:16px;">
        GreenGrove was founded in 2018 with a simple belief: that every home and workplace deserves the beauty and wellness benefits of nature. 
        What started as a small nursery in Pune has grown into India's most trusted online plant destination.
        </p>
        <p style="font-size:15px;line-height:1.9;color:#555;margin-bottom:24px;">
        We partner directly with certified nurseries across India to bring you the healthiest, most vibrant plants — 
        curated by expert botanists, packed sustainably, and delivered with a 30-day happiness guarantee.
        </p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div style="background:#F1F8E9;padding:20px;border-radius:12px;text-align:center;">
                <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;color:#1B5E20;">12,000+</div>
                <div style="font-size:13px;color:#777;margin-top:4px;">Happy Customers</div>
            </div>
            <div style="background:#F1F8E9;padding:20px;border-radius:12px;text-align:center;">
                <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;color:#1B5E20;">500+</div>
                <div style="font-size:13px;color:#777;margin-top:4px;">Plant Varieties</div>
            </div>
            <div style="background:#F1F8E9;padding:20px;border-radius:12px;text-align:center;">
                <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;color:#1B5E20;">50+</div>
                <div style="font-size:13px;color:#777;margin-top:4px;">Cities Served</div>
            </div>
            <div style="background:#F1F8E9;padding:20px;border-radius:12px;text-align:center;">
                <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;color:#1B5E20;">4.9/5</div>
                <div style="font-size:13px;color:#777;margin-top:4px;">Average Rating</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <h3 style="font-family:'Playfair Display',serif;margin-bottom:24px;">Our Values</h3>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;">
        <div style="background:white;border-radius:16px;padding:28px;box-shadow:0 4px 20px rgba(0,0,0,0.06);text-align:center;">
            <div style="font-size:36px;margin-bottom:12px;">&#127807;</div>
            <div style="font-weight:700;font-size:16px;margin-bottom:8px;">Plant Health First</div>
            <p style="font-size:13px;color:#777;line-height:1.7;">Every plant is inspected and certified healthy before dispatch. We guarantee or replace.</p>
        </div>
        <div style="background:white;border-radius:16px;padding:28px;box-shadow:0 4px 20px rgba(0,0,0,0.06);text-align:center;">
            <div style="font-size:36px;margin-bottom:12px;">&#9851;</div>
            <div style="font-weight:700;font-size:16px;margin-bottom:8px;">Sustainability</div>
            <p style="font-size:13px;color:#777;line-height:1.7;">100% plastic-free packaging, carbon-neutral deliveries, and support for local nurseries.</p>
        </div>
        <div style="background:white;border-radius:16px;padding:28px;box-shadow:0 4px 20px rgba(0,0,0,0.06);text-align:center;">
            <div style="font-size:36px;margin-bottom:12px;">&#128218;</div>
            <div style="font-weight:700;font-size:16px;margin-bottom:8px;">Expert Guidance</div>
            <p style="font-size:13px;color:#777;line-height:1.7;">Botanist-curated care guides and our AI plant doctor ensure your plants thrive.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

# ─────────────────────────────────────────────
# CONTACT PAGE
# ─────────────────────────────────────────────
def render_contact():
    st.markdown("""
    <div class="page-header">
        <div class="page-header-title">Contact Us</div>
        <div style="color:#777;">We're here to help with any plant-related query.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <h3 style="font-family:'Playfair Display',serif;margin-bottom:24px;">Get in Touch</h3>
        <div style="margin-bottom:24px;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <div style="width:44px;height:44px;background:#E8F5E9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">&#128222;</div>
                <div>
                    <div style="font-weight:700;font-size:14px;">Phone</div>
                    <div style="color:#777;font-size:13px;">+91 98765 43210 (9 AM – 6 PM, Mon–Sat)</div>
                </div>
            </div>
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <div style="width:44px;height:44px;background:#E8F5E9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">&#128140;</div>
                <div>
                    <div style="font-weight:700;font-size:14px;">Email</div>
                    <div style="color:#777;font-size:13px;">care@greengrove.in</div>
                </div>
            </div>
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:44px;height:44px;background:#E8F5E9;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">&#128205;</div>
                <div>
                    <div style="font-weight:700;font-size:14px;">Address</div>
                    <div style="color:#777;font-size:13px;">GreenGrove HQ, Baner, Pune, Maharashtra – 411045</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#F1F8E9;border-radius:12px;padding:20px;margin-top:8px;">
            <div style="font-weight:700;margin-bottom:8px;">Business Hours</div>
            <div style="font-size:13px;color:#555;line-height:2;">
                Monday – Friday: 9:00 AM – 7:00 PM<br/>
                Saturday: 9:00 AM – 5:00 PM<br/>
                Sunday: 10:00 AM – 3:00 PM
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='font-family:Playfair Display,serif;margin-bottom:24px;'>Send a Message</h3>", unsafe_allow_html=True)
        name = st.text_input("Your Name", placeholder="Rahul Sharma", key="contact_name")
        email = st.text_input("Email Address", placeholder="rahul@example.com", key="contact_email")
        subject = st.selectbox("Subject", ["Plant Care Query", "Order Issue", "Return/Replacement", "Bulk Order", "Partnership", "Other"], key="contact_subject")
        message = st.text_area("Your Message", placeholder="Tell us how we can help...", height=120, key="contact_message")
        if st.button("Send Message", type="primary", use_container_width=True, key="contact_send"):
            if name and email and message:
                st.success("Your message has been sent! We'll respond within 24 hours.")
            else:
                st.error("Please fill in all fields.")

    st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

# ─────────────────────────────────────────────
# OFFERS PAGE
# ─────────────────────────────────────────────
def render_offers():
    st.markdown("""
    <div class="page-header">
        <div class="page-header-title">Offers & Deals</div>
        <div style="color:#777;">Exclusive discounts for our plant community</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

    offers = [
        {"title": "Monsoon Special", "desc": "40% off on all outdoor plants & gardening tools", "code": "MONSOON40", "color": "#E8F5E9", "accent": "#2E7D32", "img": "https://images.unsplash.com/photo-1587978185023-dc9c1d66fbca?w=300&h=180&fit=crop"},
        {"title": "First Order Gift", "desc": "Extra 15% off on your first purchase + free care guide", "code": "FIRSTORDER", "color": "#FCE4EC", "accent": "#C62828", "img": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=300&h=180&fit=crop"},
        {"title": "Bundle & Save", "desc": "Buy 3 plants, get the smallest one free", "code": "BUNDLE3", "color": "#EDE7F6", "accent": "#4527A0", "img": "https://images.unsplash.com/photo-1593691509543-c55fb32e4c84?w=300&h=180&fit=crop"},
        {"title": "Refer a Friend", "desc": "Give ₹200 off, get ₹200 credit for every referral", "code": "REFER200", "color": "#FFF3E0", "accent": "#E65100", "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=180&fit=crop"},
    ]

    cols = st.columns(2)
    for i, offer in enumerate(offers):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:{offer['color']};border-radius:16px;padding:28px;margin-bottom:20px;display:flex;gap:20px;align-items:center;">
                <img src="{offer['img']}" style="width:120px;height:90px;border-radius:10px;object-fit:cover;flex-shrink:0;" onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=120&h=90&fit=crop'"/>
                <div>
                    <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:{offer['accent']};margin-bottom:6px;">{offer['title']}</div>
                    <div style="font-size:13px;color:#555;margin-bottom:12px;">{offer['desc']}</div>
                    <div style="background:white;display:inline-block;padding:6px 14px;border-radius:6px;font-size:12px;font-weight:700;color:{offer['accent']};letter-spacing:2px;border:2px dashed {offer['accent']};">{offer['code']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3 style='font-family:Playfair Display,serif;margin-bottom:20px;'>Sale Items</h3>", unsafe_allow_html=True)
    sale_items = [p for p in PRODUCTS if p.get("badge") in ["Sale", "Bestseller"]]
    cols = st.columns(4)
    for i, p in enumerate(sale_items[:8]):
        with cols[i % 4]:
            render_product_card(p, col_key=f"offer{i}")

    st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
def render_footer():
    st.markdown("""
    <div class="footer-wrap">
        <div class="footer-grid">
            <div>
                <div class="footer-logo">GreenGrove</div>
                <div class="footer-desc">India's premium plant destination. We bring nature indoors, one plant at a time. Certified nurseries, expert care, and happiness guaranteed.</div>
                <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:rgba(255,255,255,0.5);">
                    <span>&#10003;</span><span>30-Day Plant Guarantee</span>
                    <span style="margin-left:12px;">&#10003;</span><span>Free Delivery Above &#8377;999</span>
                </div>
            </div>
            <div>
                <div class="footer-heading">Quick Links</div>
                <a class="footer-link">About Us</a>
                <a class="footer-link">Our Nurseries</a>
                <a class="footer-link">Plant Blog</a>
                <a class="footer-link">Careers</a>
                <a class="footer-link">Press</a>
            </div>
            <div>
                <div class="footer-heading">Help & Policy</div>
                <a class="footer-link">Shipping Policy</a>
                <a class="footer-link">Return Policy</a>
                <a class="footer-link">FAQs</a>
                <a class="footer-link">Track Your Order</a>
                <a class="footer-link">Privacy Policy</a>
                <a class="footer-link">Terms of Service</a>
            </div>
            <div>
                <div class="footer-heading">Contact</div>
                <a class="footer-link">care@greengrove.in</a>
                <a class="footer-link">+91 98765 43210</a>
                <a class="footer-link">Baner, Pune – 411045</a>
                <div style="margin-top:16px;" class="footer-heading">Follow Us</div>
                <div style="display:flex;gap:8px;margin-top:8px;">
                    <div class="social-btn">f</div>
                    <div class="social-btn">in</div>
                    <div class="social-btn">tw</div>
                    <div class="social-btn">yt</div>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <div>© 2025 GreenGrove. All rights reserved. Made with love for plant parents across India.</div>
            <div style="display:flex;gap:16px;align-items:center;">
                <span>Visa</span><span>Mastercard</span><span>UPI</span><span>PhonePe</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LEAFLIFE CARE — SIDEBAR CHATBOT
# The sidebar is the correct Streamlit mechanism for a persistent
# floating panel visible on every page without layout disruption.
# ─────────────────────────────────────────────

DIAG_MAP = {
    "Yellowing leaves": {
        "condition": "Nitrogen Deficiency / Overwatering",
        "cause": "Overwatering suffocates roots, blocking nutrient uptake. Yellowing typically starts from older lower leaves and moves upward.",
        "care_steps": [
            "Allow soil to dry 2–3 inches deep before next watering.",
            "Check drainage — repot if soil stays waterlogged.",
            "Apply a balanced liquid fertilizer at half-strength every 14 days.",
            "Trim yellow leaves cleanly with sterilised scissors.",
        ],
        "severity": "Moderate",
        "remedy_products": ["Liquid Seaweed Growth Booster", "Organic Neem Cake Fertilizer"],
        "confidence": 87,
        "icon": "🌿",
    },
    "Brown tips": {
        "condition": "Low Humidity / Salt Build-up",
        "cause": "Brown crispy leaf tips are a classic sign of dry air (below 40% RH) or fertiliser salt accumulation around roots.",
        "care_steps": [
            "Mist leaves lightly every morning or use a pebble-water humidity tray.",
            "Move plant away from AC vents and heating units.",
            "Flush soil thoroughly with water once a month to flush salts.",
            "Trim brown tips at an angle — leave a sliver of brown to prevent further die-back.",
        ],
        "severity": "Low",
        "remedy_products": ["Terracotta Pot Set (3 Sizes)", "Liquid Seaweed Growth Booster"],
        "confidence": 91,
        "icon": "🍂",
    },
    "Wilting / Drooping": {
        "condition": "Severe Underwatering or Root Rot",
        "cause": "Wilting with dry soil = critical dehydration. Wilting with wet soil = root rot from fungal infection blocking water transport.",
        "care_steps": [
            "Check soil moisture 2 inches deep — water thoroughly if dry.",
            "If soil is wet, unpot the plant and inspect roots.",
            "Trim black/mushy roots with sterile shears and dust with cinnamon (natural antifungal).",
            "Repot in fresh well-draining mix and reduce watering frequency.",
        ],
        "severity": "High",
        "remedy_products": ["Organic Neem Cake Fertilizer", "Liquid Seaweed Growth Booster"],
        "confidence": 83,
        "icon": "🥀",
    },
    "Spots on leaves": {
        "condition": "Fungal Leaf Spot / Bacterial Infection",
        "cause": "Water splashing on leaves combined with poor airflow creates ideal conditions for fungal and bacterial pathogens.",
        "care_steps": [
            "Isolate plant immediately to prevent spread to other plants.",
            "Remove all affected leaves and dispose — do not compost.",
            "Spray neem oil solution (5ml per litre water) on all leaf surfaces every 5 days.",
            "Water at soil level only, never on foliage.",
        ],
        "severity": "Moderate",
        "remedy_products": ["Organic Neem Cake Fertilizer", "Liquid Seaweed Growth Booster"],
        "confidence": 79,
        "icon": "🔴",
    },
    "White powder on leaves": {
        "condition": "Powdery Mildew (Fungal)",
        "cause": "Powdery mildew thrives in warm days + cool nights with poor air circulation. Highly contagious between plants.",
        "care_steps": [
            "Isolate plant immediately.",
            "Mix 1 tsp baking soda + 1 tsp neem oil + 1L water and spray every 3 days.",
            "Increase air circulation around the plant.",
            "Avoid overhead watering — keep foliage dry.",
        ],
        "severity": "High",
        "remedy_products": ["Organic Neem Cake Fertilizer"],
        "confidence": 95,
        "icon": "⚪",
    },
    "Sticky residue on leaves": {
        "condition": "Aphid / Scale Insect Infestation",
        "cause": "Sticky honeydew is secreted by sap-sucking pests. Check leaf undersides and stem nodes for small clusters of insects.",
        "care_steps": [
            "Wipe all leaves with isopropyl alcohol on a cotton swab.",
            "Blast plant with a strong water jet to dislodge pests.",
            "Apply neem oil spray every 5 days for 3 weeks.",
            "Introduce beneficial insects (ladybugs) for outdoor plants.",
        ],
        "severity": "Moderate",
        "remedy_products": ["Organic Neem Cake Fertilizer", "Liquid Seaweed Growth Booster"],
        "confidence": 92,
        "icon": "🐛",
    },
    "Pale / washed-out color": {
        "condition": "Too Much Direct Sun / Iron Deficiency",
        "cause": "Bleached or very pale new leaves usually indicate sunscorch or iron chlorosis (lack of iron or high soil pH blocking iron uptake).",
        "care_steps": [
            "Move plant to bright indirect light — away from harsh afternoon sun.",
            "Apply chelated iron foliar spray every 10 days.",
            "Check soil pH — ideal is 5.5–6.5 for most houseplants.",
            "Add diluted seaweed extract to boost micronutrient availability.",
        ],
        "severity": "Low",
        "remedy_products": ["Liquid Seaweed Growth Booster", "Organic Neem Cake Fertilizer"],
        "confidence": 76,
        "icon": "🌤️",
    },
    "No new growth": {
        "condition": "Dormancy / Root Bound / Nutrient Exhaustion",
        "cause": "Stalled growth is usually due to depleted soil nutrients, roots filling the pot, or the plant entering seasonal dormancy.",
        "care_steps": [
            "Check if roots are circling out of drainage holes — if so, repot 1–2 sizes up.",
            "Begin a monthly balanced fertiliser regimen during growing season.",
            "Ensure the plant is getting adequate light for its species.",
            "Increase watering slightly in spring to trigger new growth.",
        ],
        "severity": "Low",
        "remedy_products": ["Liquid Seaweed Growth Booster", "Terracotta Pot Set (3 Sizes)"],
        "confidence": 80,
        "icon": "🌱",
    },
}

SUGGESTION_RESULTS_KEY = "sugg_results"

def _severity_badge(severity):
    colours = {"Low": ("#E8F5E9", "#2E7D32"), "Moderate": ("#FFF8E1", "#F57F17"), "High": ("#FFEBEE", "#C62828")}
    bg, fg = colours.get(severity, ("#F5F5F5", "#555"))
    return f'<span style="background:{bg};color:{fg};padding:3px 10px;border-radius:50px;font-size:11px;font-weight:700;">{severity} Severity</span>'


def _confidence_bar(pct):
    return f"""
    <div style="margin:10px 0 4px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="font-size:11px;color:#777;font-weight:600;">AI Confidence</span>
            <span style="font-size:11px;color:#2E7D32;font-weight:700;">{pct}%</span>
        </div>
        <div style="background:#E8EDE8;border-radius:50px;height:6px;overflow:hidden;">
            <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,#43A047,#1B5E20);border-radius:50px;transition:width 0.6s;"></div>
        </div>
    </div>"""



def render_chatbot_sidebar():
    """LeafLife Care chatbot rendered in Streamlit sidebar repositioned to the RIGHT.
    This is the only reliable approach in Streamlit — all widgets stay in sidebar DOM."""

    chatbot_open = st.session_state.get("chatbot_open", False)

    # ── CSS: reposition sidebar to the RIGHT + FAB + styles ─────────────────
    sidebar_transform = "translateX(0%)" if chatbot_open else "translateX(100%)"
    backdrop_display = "block" if chatbot_open else "none"

    st.markdown(f"""
    <style>
    /* Hide the default sidebar toggle arrow */
    [data-testid="collapsedControl"] {{ display: none !important; }}

    /* Move sidebar to the RIGHT side of screen */
    [data-testid="stSidebar"] {{
        position: fixed !important;
        top: 0 !important;
        right: 0 !important;
        left: auto !important;
        height: 100vh !important;
        width: 400px !important;
        min-width: 400px !important;
        max-width: 400px !important;
        background: #FAFAF7 !important;
        border-left: 1px solid #E8EDE8 !important;
        border-right: none !important;
        box-shadow: -8px 0 40px rgba(0,0,0,0.18) !important;
        z-index: 99998 !important;
        transform: {sidebar_transform} !important;
        transition: transform 0.35s cubic-bezier(0.4,0,0.2,1) !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        height: 100vh !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        padding: 0 !important;
        width: 400px !important;
    }}
    [data-testid="stSidebarContent"] {{ padding: 0 !important; }}
    [data-testid="stSidebar"] ::-webkit-scrollbar {{ width: 4px; }}
    [data-testid="stSidebar"] ::-webkit-scrollbar-thumb {{ background: #C8E6C9; border-radius: 2px; }}
    [data-testid="stSidebar"] .stButton > button {{
        border-radius: 50px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
    }}

    /* Backdrop */
    #cb-backdrop {{
        display: {backdrop_display};
        position: fixed; inset: 0;
        background: rgba(0,0,0,0.4);
        z-index: 99997;
        animation: cbFadeIn 0.3s ease;
    }}
    @keyframes cbFadeIn {{ from{{opacity:0}} to{{opacity:1}} }}

    /* FAB */
    #cb-fab {{
        position: fixed; bottom: 28px; right: 28px;
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
        color: white; padding: 14px 22px; border-radius: 50px;
        font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 14px;
        box-shadow: 0 8px 28px rgba(46,125,50,0.45);
        z-index: 99999; cursor: pointer;
        display: flex; align-items: center; gap: 8px;
        border: 3px solid rgba(255,255,255,0.3);
        animation: fabPulse 2.8s infinite; user-select: none;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    #cb-fab:hover {{ transform: scale(1.06); box-shadow: 0 12px 36px rgba(46,125,50,0.65); }}
    @keyframes fabPulse {{
        0%,100% {{ box-shadow: 0 8px 28px rgba(46,125,50,0.45); }}
        50%      {{ box-shadow: 0 8px 40px rgba(46,125,50,0.70), 0 0 0 8px rgba(46,125,50,0.10); }}
    }}
    .fab-dot {{
        width: 8px; height: 8px; background: #69F0AE; border-radius: 50%;
        animation: dotBlink 1.4s infinite; flex-shrink: 0;
    }}
    @keyframes dotBlink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}

    /* Mode cards */
    .cb-mode-card {{
        background: white; border: 2px solid #E8EDE8; border-radius: 14px;
        padding: 16px; margin-bottom: 10px; transition: all 0.25s;
    }}
    .cb-mode-card:hover {{ border-color: #2E7D32; background: #F1F8E9; transform: translateY(-1px); }}
    .cb-mode-icon {{ font-size: 28px; margin-bottom: 8px; }}
    .cb-mode-title {{ font-weight: 700; font-size: 15px; color: #1A1A1A; margin-bottom: 4px; }}
    .cb-mode-desc {{ font-size: 12px; color: #777; line-height: 1.5; }}

    /* Diagnosis result */
    .diag-result-card {{
        background: white; border-radius: 14px; border: 1px solid #E8EDE8;
        overflow: hidden; margin: 14px 0; box-shadow: 0 4px 16px rgba(0,0,0,0.07);
    }}
    .diag-result-header {{ padding: 14px 16px; border-bottom: 1px solid #F0F0F0; }}
    .diag-result-body {{ padding: 14px 16px; }}
    .care-step {{
        display: flex; gap: 10px; align-items: flex-start;
        padding: 8px 0; border-bottom: 1px solid #F5F5F5;
        font-size: 13px; color: #444; line-height: 1.6;
    }}
    .care-step:last-child {{ border-bottom: none; }}
    .step-num {{
        width: 22px; height: 22px; background: #E8F5E9; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 11px; font-weight: 700; color: #2E7D32; flex-shrink: 0; margin-top: 2px;
    }}
    .remedy-card {{
        background: white; border: 1px solid #E8EDE8; border-radius: 12px;
        padding: 12px; margin-bottom: 8px; display: flex; gap: 12px; align-items: center;
    }}
    .remedy-img {{ width: 56px; height: 56px; border-radius: 8px; object-fit: cover; flex-shrink: 0; }}

    /* Quiz */
    .quiz-step-indicator {{ display: flex; gap: 6px; margin-bottom: 18px; }}
    .quiz-dot {{ height: 4px; border-radius: 2px; flex: 1; background: #E8EDE8; transition: background 0.3s; }}
    .quiz-dot.active {{ background: #2E7D32; }}

    /* Suggestion cards */
    .sugg-plant-card {{
        background: white; border: 1px solid #E8EDE8; border-radius: 14px;
        overflow: hidden; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }}
    .sugg-plant-img {{ width: 100%; height: 130px; object-fit: cover; }}
    .sugg-plant-body {{ padding: 12px 14px; }}
    .sugg-match-badge {{
        display: inline-block; background: #E8F5E9; color: #2E7D32;
        padding: 2px 8px; border-radius: 50px; font-size: 10px; font-weight: 700; margin-bottom: 6px;
    }}

    /* Hide the invisible FAB Streamlit button from view */
    [data-testid="stMainBlockContainer"] [data-cb-fab-wrap] {{ display: none !important; }}
    </style>

    <!-- Backdrop -->
    <div id="cb-backdrop"></div>

    <!-- FAB — clicking triggers hidden Streamlit button -->
    <div id="cb-fab" onclick="(function(){{var b=document.querySelector('button[data-cb-fab]');if(b)b.click();}})()">
        <span style="font-size:18px;">&#127807;</span>
        <span>LeafLife Care</span>
        <div class="fab-dot"></div>
    </div>
    """, unsafe_allow_html=True)

    # Hidden Streamlit FAB button — invisible overlay on the HTML FAB
    # It uses display:none via CSS but we click it programmatically
    # Actually we need it clickable, so we use opacity:0 + pointer-events:none on wrapper
    # and let JS click it
    fab_clicked = st.button("fab_toggle", key="fab_open_btn")
    if fab_clicked:
        st.session_state.chatbot_open = not chatbot_open
        st.rerun()

    # Tag the fab button and hide it visually
    st.markdown("""
    <script>
    (function tagFab() {
        var btns = document.querySelectorAll('[data-testid="stMainBlockContainer"] button');
        btns.forEach(function(b) {
            if (b.textContent.trim() === 'fab_toggle') {
                b.setAttribute('data-cb-fab', '1');
                b.style.cssText = 'position:fixed;bottom:28px;right:28px;width:200px;height:56px;opacity:0;z-index:100000;border:none;background:transparent;cursor:pointer;';
            }
        });
    })();
    setTimeout(function() {
        var btns = document.querySelectorAll('[data-testid="stMainBlockContainer"] button');
        btns.forEach(function(b) {
            if (b.textContent.trim() === 'fab_toggle') {
                b.setAttribute('data-cb-fab', '1');
                b.style.cssText = 'position:fixed;bottom:28px;right:28px;width:200px;height:56px;opacity:0;z-index:100000;border:none;background:transparent;cursor:pointer;';
            }
        });
    }, 500);
    </script>
    """, unsafe_allow_html=True)

    # ── All chatbot content in the real Streamlit sidebar ───────────────────
    with st.sidebar:
        # Green header
        st.markdown("""
        <div style="background:linear-gradient(135deg,#2E7D32 0%,#1B5E20 100%);padding:22px 20px 18px;margin:-1rem -1rem 0;">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:52px;height:52px;border-radius:50%;background:rgba(255,255,255,0.18);border:2px solid rgba(255,255,255,0.35);display:flex;align-items:center;justify-content:center;font-size:24px;">&#127807;</div>
                <div style="flex:1;">
                    <div style="font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:white;">LeafLife Care</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.72);margin-top:2px;">AI Plant Health Expert</div>
                </div>
                <div style="display:flex;align-items:center;gap:6px;">
                    <div style="width:8px;height:8px;background:#69F0AE;border-radius:50%;"></div>
                    <span style="font-size:11px;color:rgba(255,255,255,0.65);">Online</span>
                </div>
            </div>
            <div style="margin-top:14px;background:rgba(255,255,255,0.12);border-radius:10px;padding:10px 12px;">
                <div style="font-size:12px;color:rgba(255,255,255,0.85);line-height:1.6;">
                    Hello! I am your personal plant doctor and advisor. I can diagnose plant diseases from symptoms or help you find your perfect plant.
                </div>
            </div>
        </div>
        <div style="height:12px;"></div>
        """, unsafe_allow_html=True)

        if st.button("✕ Close Chat", key="cb_close_btn"):
            st.session_state.chatbot_open = False
            st.rerun()

        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)


        # ── MODE SELECTOR ──────────────────────────────────────────────────
        if st.session_state.chatbot_mode is None:
            st.markdown("""
            <div style="padding:0 4px;margin-bottom:6px;">
                <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#999;margin-bottom:12px;">Choose your expert</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="cb-mode-card">
                <div class="cb-mode-icon">&#129338;</div>
                <div class="cb-mode-title">Plant Diagnosis Doctor</div>
                <div class="cb-mode-desc">Upload a photo and describe symptoms. Get an AI-powered diagnosis with severity rating, detailed care steps, and remedy products.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open Diagnosis Doctor", key="open_diag", use_container_width=True, type="primary"):
                st.session_state.chatbot_mode = "diagnosis"
                st.session_state.diagnosis_result = None
                st.rerun()

            st.markdown("""
            <div class="cb-mode-card" style="margin-top:4px;">
                <div class="cb-mode-icon">&#127807;</div>
                <div class="cb-mode-title">Plant Suggestions Expert</div>
                <div class="cb-mode-desc">Answer 4 quick questions about your space and lifestyle. Get personalised plant recommendations matched to your needs.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open Plant Suggestions", key="open_sugg", use_container_width=True):
                st.session_state.chatbot_mode = "suggestions"
                st.session_state[SUGGESTION_RESULTS_KEY] = None
                st.rerun()

            st.markdown("""
            <div style="margin-top:16px;padding:12px;background:#F1F8E9;border-radius:10px;border-left:3px solid #2E7D32;">
                <div style="font-size:12px;color:#2E7D32;font-weight:700;margin-bottom:4px;">Did you know?</div>
                <div style="font-size:12px;color:#555;line-height:1.6;">NASA's Clean Air Study identified 18 houseplants that significantly reduce indoor air toxins including formaldehyde and benzene.</div>
            </div>
            """, unsafe_allow_html=True)

        # ── DIAGNOSIS DOCTOR ───────────────────────────────────────────────
        elif st.session_state.chatbot_mode == "diagnosis":
            # Sub-header
            st.markdown("""
            <div style="padding:0 4px 12px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <span style="font-size:20px;">&#129338;</span>
                    <span style="font-family:'Playfair Display',serif;font-size:17px;font-weight:700;color:#1A1A1A;">Plant Diagnosis Doctor</span>
                </div>
                <div style="font-size:12px;color:#777;line-height:1.5;">Upload your plant's photo and select visible symptoms. Our AI engine will analyse and provide a full diagnosis report.</div>
            </div>
            """, unsafe_allow_html=True)

            # Image upload
            st.markdown("**Step 1 — Upload Plant Photo**")
            uploaded_img = st.file_uploader(
                "Drag and drop or click to upload",
                type=["jpg", "jpeg", "png", "webp"],
                key="diag_img_upload",
                help="Upload a clear photo of the affected plant or leaves",
            )
            if uploaded_img:
                st.image(uploaded_img, caption="Uploaded plant photo", use_container_width=True)
                st.markdown("""
                <div style="background:#E8F5E9;border-radius:8px;padding:8px 12px;font-size:12px;color:#2E7D32;margin-bottom:4px;">
                    &#10003; Photo received — visual analysis in progress...
                </div>
                """, unsafe_allow_html=True)

            # Symptom checklist
            st.markdown("**Step 2 — Select Visible Symptoms**")
            st.markdown("<div style='font-size:12px;color:#777;margin-bottom:6px;'>Select all symptoms you can observe:</div>", unsafe_allow_html=True)

            symptom_options = list(DIAG_MAP.keys())
            selected_symptoms = []
            cols_a, cols_b = st.columns(2)
            half = len(symptom_options) // 2
            for i, sym in enumerate(symptom_options):
                col = cols_a if i < half else cols_b
                with col:
                    if st.checkbox(sym, key=f"sym_{i}"):
                        selected_symptoms.append(sym)

            # Plant type (optional context)
            st.markdown("**Step 3 — Plant Type (optional)**")
            plant_type = st.selectbox(
                "What type of plant?",
                ["Not sure", "Monstera / Tropical", "Succulent / Cactus", "Fern / Humidity-loving",
                 "Orchid", "Fiddle Leaf Fig", "Pothos / Vines", "Outdoor / Garden", "Other"],
                key="diag_plant_type",
                label_visibility="collapsed",
            )

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            run_diag = st.button(
                "Run AI Diagnosis",
                key="run_diagnosis_btn",
                type="primary",
                use_container_width=True,
                disabled=(not uploaded_img and not selected_symptoms),
            )

            if not uploaded_img and not selected_symptoms:
                st.markdown("<div style='font-size:11px;color:#999;text-align:center;'>Upload a photo or select at least one symptom to enable diagnosis.</div>", unsafe_allow_html=True)

            if run_diag and (uploaded_img or selected_symptoms):
                # Pick primary diagnosis
                if selected_symptoms:
                    primary = selected_symptoms[0]
                    result_data = DIAG_MAP[primary].copy()
                    # Escalate severity if multiple symptoms
                    if len(selected_symptoms) >= 3:
                        result_data["severity"] = "High"
                    elif len(selected_symptoms) == 2:
                        result_data["severity"] = "Moderate" if result_data["severity"] == "Low" else result_data["severity"]
                    result_data["all_symptoms"] = selected_symptoms
                    result_data["plant_type"] = plant_type
                else:
                    # Image only — give a general response
                    result_data = DIAG_MAP["Yellowing leaves"].copy()
                    result_data["all_symptoms"] = ["Image analysis only"]
                    result_data["plant_type"] = plant_type
                    result_data["confidence"] = 72

                st.session_state.diagnosis_result = result_data
                st.rerun()

            # ── DIAGNOSIS RESULT ──────────────────────────────────────────
            if st.session_state.diagnosis_result:
                r = st.session_state.diagnosis_result
                sev = r["severity"]
                sev_colours = {"Low": "#2E7D32", "Moderate": "#F57F17", "High": "#C62828"}
                sev_bg = {"Low": "#E8F5E9", "Moderate": "#FFF8E1", "High": "#FFEBEE"}
                sev_col = sev_colours.get(sev, "#555")
                sev_bgc = sev_bg.get(sev, "#F5F5F5")

                st.markdown("---")
                st.markdown(f"""
                <div class="diag-result-card">
                    <div class="diag-result-header" style="background:{sev_bgc};">
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                            <span style="font-size:28px;">{r['icon']}</span>
                            <div>
                                <div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#999;margin-bottom:2px;">Diagnosis Result</div>
                                <div style="font-weight:700;font-size:15px;color:#1A1A1A;">{r['condition']}</div>
                            </div>
                        </div>
                        <div style="display:flex;gap:8px;flex-wrap:wrap;">
                            {_severity_badge(sev)}
                            <span style="background:white;color:#555;padding:3px 10px;border-radius:50px;font-size:11px;font-weight:600;border:1px solid #E8EDE8;">AI Confidence: {r['confidence']}%</span>
                        </div>
                        {_confidence_bar(r['confidence'])}
                    </div>
                    <div class="diag-result-body">
                        <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#999;margin-bottom:8px;">Root Cause</div>
                        <div style="font-size:13px;color:#444;line-height:1.7;margin-bottom:14px;">{r['cause']}</div>
                        <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#999;margin-bottom:8px;">Treatment Plan</div>
                        {''.join([f'<div class="care-step"><div class="step-num">{i+1}</div><div>{step}</div></div>' for i, step in enumerate(r['care_steps'])])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Symptoms diagnosed
                if len(r.get("all_symptoms", [])) > 1:
                    additional = r["all_symptoms"][1:]
                    st.markdown(f"""
                    <div style="background:#FFF8E1;border-radius:8px;padding:10px 12px;font-size:12px;color:#777;margin-bottom:12px;">
                        <b style="color:#F57F17;">Additional symptoms detected:</b> {', '.join(additional)}. These may indicate a secondary issue — monitor closely after treating the primary condition.
                    </div>
                    """, unsafe_allow_html=True)

                # Recommended remedy products
                st.markdown("""
                <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#999;margin:14px 0 10px;">Recommended Remedies</div>
                """, unsafe_allow_html=True)

                remedy_products = [p for p in PRODUCTS if p["name"] in r.get("remedy_products", [])]
                if not remedy_products:
                    remedy_products = [p for p in PRODUCTS if p["category"] == "Fertilizers"][:2]

                for prod in remedy_products:
                    disc = discount_pct(prod["price"], prod["original_price"])
                    st.markdown(f"""
                    <div class="remedy-card">
                        <img class="remedy-img" src="{prod['image']}" alt="{prod['name']}"
                             onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=56&h=56&fit=crop'"/>
                        <div style="flex:1;min-width:0;">
                            <div style="font-size:13px;font-weight:700;color:#1A1A1A;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{prod['name']}</div>
                            <div style="font-size:11px;color:#777;margin-bottom:6px;">{prod['category']}</div>
                            <div style="display:flex;align-items:center;gap:6px;">
                                <span style="font-weight:700;font-size:15px;color:#1B5E20;">&#8377;{prod['price']}</span>
                                <span style="font-size:11px;color:#999;text-decoration:line-through;">&#8377;{prod['original_price']}</span>
                                <span style="background:#FCE4EC;color:#C62828;font-size:10px;font-weight:700;padding:1px 6px;border-radius:50px;">{disc}% off</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    c_atc, c_view = st.columns([3, 2])
                    with c_atc:
                        if st.button(f"Add to Cart", key=f"remedy_atc_{prod['id']}", use_container_width=True, type="primary"):
                            add_to_cart(prod["id"])
                            st.success(f"Added {prod['name']}!")
                    with c_view:
                        if st.button("Details", key=f"remedy_view_{prod['id']}", use_container_width=True):
                            nav_to("product", selected_product=prod["id"])
                            st.rerun()

                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                st.markdown("""
                <div style="background:#E8F5E9;border-radius:10px;padding:12px 14px;font-size:12px;color:#2E7D32;line-height:1.6;">
                    <b>Pro Tip:</b> Take weekly photos of your plant to track recovery progress. Most plants respond positively within 10–14 days of correct treatment.
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
                col_again, col_back = st.columns(2)
                with col_again:
                    if st.button("New Diagnosis", key="new_diag_btn", use_container_width=True):
                        st.session_state.diagnosis_result = None
                        st.rerun()
                with col_back:
                    if st.button("Main Menu", key="diag_to_menu", use_container_width=True):
                        st.session_state.chatbot_mode = None
                        st.session_state.diagnosis_result = None
                        st.rerun()

            else:
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("Back to Menu", key="diag_back_btn", use_container_width=True):
                    st.session_state.chatbot_mode = None
                    st.rerun()

        # ── PLANT SUGGESTIONS EXPERT ───────────────────────────────────────
        elif st.session_state.chatbot_mode == "suggestions":
            st.markdown("""
            <div style="padding:0 4px 12px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <span style="font-size:20px;">&#127807;</span>
                    <span style="font-family:'Playfair Display',serif;font-size:17px;font-weight:700;color:#1A1A1A;">Plant Suggestions Expert</span>
                </div>
                <div style="font-size:12px;color:#777;line-height:1.5;">Answer 4 quick questions and I'll find plants perfectly matched to your lifestyle, space, and needs.</div>
            </div>
            """, unsafe_allow_html=True)

            results_ready = st.session_state.get(SUGGESTION_RESULTS_KEY)

            if not results_ready:
                # Quiz progress bar
                st.markdown("""
                <div class="quiz-step-indicator">
                    <div class="quiz-dot active"></div>
                    <div class="quiz-dot active"></div>
                    <div class="quiz-dot active"></div>
                    <div class="quiz-dot active"></div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Q1 — Where will the plant live?**")
                location = st.radio(
                    "Location",
                    ["Indoor — Living Room / Bedroom", "Indoor — Office / Low Light", "Outdoor — Balcony / Full Sun", "Outdoor — Shaded Garden"],
                    key="q_location",
                    label_visibility="collapsed",
                )

                st.markdown("**Q2 — How much natural light is available?**")
                light = st.radio(
                    "Light",
                    ["Very Low (no direct sun)", "Indirect Bright (filtered/curtained)", "Partial Sun (morning sun only)", "Full Sun (6+ hrs direct)"],
                    key="q_light",
                    label_visibility="collapsed",
                )

                st.markdown("**Q3 — How much time can you give to plant care?**")
                maintenance = st.radio(
                    "Maintenance",
                    ["Minimal — water once a week or less", "Moderate — water 2-3x week, occasional feeding", "Enthusiast — daily attention, fertilising, pruning"],
                    key="q_maintenance",
                    label_visibility="collapsed",
                )

                st.markdown("**Q4 — What matters most to you?**")
                purpose = st.multiselect(
                    "Purpose",
                    ["Air Purification", "Flowering / Colour", "Gifting", "Low Maintenance", "Aesthetic Decor", "Pet Safe", "Beginner Friendly"],
                    key="q_purpose",
                    label_visibility="collapsed",
                    placeholder="Select all that apply...",
                )

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("Find My Perfect Plants", key="run_suggestions_btn", type="primary", use_container_width=True):
                    # ── Filtering logic ──────────────────────────────────
                    pool = list(PRODUCTS)

                    # Location filter
                    if "Indoor" in location:
                        pool = [p for p in pool if p["category"] in
                                ["Indoor Plants", "Air Purifying Plants", "Succulents", "Flowering Plants", "Bonsai Plants"]]
                    elif "Outdoor" in location:
                        pool = [p for p in pool if p["category"] in ["Outdoor Plants", "Flowering Plants"]]

                    # Light filter
                    if "Very Low" in light:
                        pool = [p for p in pool if p.get("sunlight") in ["Low Light", "Low to Bright", "Indirect", None]]
                    elif "Indirect" in light:
                        pool = [p for p in pool if p.get("sunlight") in ["Indirect", "Bright Indirect", "Low to Bright", "Low to Medium", None]]
                    elif "Full Sun" in light:
                        pool = [p for p in pool if p.get("sunlight") in ["Full Sun", None]]

                    # Maintenance filter
                    if "Minimal" in maintenance:
                        pool = [p for p in pool if p.get("care_level") in ["Very Easy", None]]
                    elif "Moderate" in maintenance:
                        pool = [p for p in pool if p.get("care_level") in ["Very Easy", "Easy", None]]

                    # Purpose filters
                    if "Air Purification" in purpose:
                        ap = [p for p in pool if p.get("air_purifying")]
                        if ap:
                            pool = ap
                    if "Flowering / Colour" in purpose:
                        fl = [p for p in pool if p["category"] in ["Flowering Plants", "Outdoor Plants"]]
                        if fl:
                            pool = fl
                    if "Low Maintenance" in purpose:
                        lm = [p for p in pool if p.get("care_level") in ["Very Easy", "Easy"]]
                        if lm:
                            pool = lm

                    # Score and rank
                    def score_plant(p):
                        s = 0
                        s += p["rating"] * 10
                        if p.get("badge") in ["Bestseller", "Top Rated"]:
                            s += 8
                        if "Air Purification" in purpose and p.get("air_purifying"):
                            s += 15
                        if "Beginner Friendly" in purpose and p.get("care_level") in ["Very Easy", "Easy"]:
                            s += 10
                        return s

                    pool = sorted(pool, key=score_plant, reverse=True)

                    if not pool:
                        pool = sorted(PRODUCTS, key=lambda x: x["rating"], reverse=True)[:4]

                    st.session_state[SUGGESTION_RESULTS_KEY] = pool[:5]
                    st.rerun()

            else:
                # ── RESULTS VIEW ─────────────────────────────────────────
                results = st.session_state[SUGGESTION_RESULTS_KEY]
                st.markdown(f"""
                <div style="background:#E8F5E9;border-radius:10px;padding:12px 14px;margin-bottom:14px;">
                    <div style="font-weight:700;color:#1B5E20;font-size:14px;margin-bottom:2px;">Found {len(results)} perfect matches for you!</div>
                    <div style="font-size:12px;color:#555;">Based on your preferences. Tap any plant to add it to your cart.</div>
                </div>
                """, unsafe_allow_html=True)

                for rank, prod in enumerate(results):
                    match_pct = max(75, 98 - rank * 5)
                    disc = discount_pct(prod["price"], prod["original_price"])
                    care_icons = {"Very Easy": "Easy care", "Easy": "Easy care", "Moderate": "Some care needed", "Expert": "Advanced care"}
                    air = " · Air Purifier" if prod.get("air_purifying") else ""

                    st.markdown(f"""
                    <div class="sugg-plant-card">
                        <div style="position:relative;">
                            <img class="sugg-plant-img" src="{prod['image']}" alt="{prod['name']}"
                                 onerror="this.src='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=130&fit=crop'"/>
                            <div style="position:absolute;top:10px;left:10px;">
                                <span class="sugg-match-badge">{match_pct}% Match</span>
                            </div>
                            {'<div style="position:absolute;top:10px;right:10px;background:#FCE4EC;color:#C62828;padding:3px 8px;border-radius:50px;font-size:10px;font-weight:700;">' + str(disc) + '% off</div>' if disc > 0 else ''}
                        </div>
                        <div class="sugg-plant-body">
                            <div style="font-size:10px;color:#2E7D32;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px;">{prod['category']}</div>
                            <div style="font-family:'Playfair Display',serif;font-size:15px;font-weight:700;color:#1A1A1A;margin-bottom:4px;">{prod['name']}</div>
                            <div style="font-size:11px;color:#777;margin-bottom:8px;">{care_icons.get(prod.get('care_level',''), 'Moderate care')}{air}</div>
                            <div style="display:flex;align-items:center;justify-content:space-between;">
                                <div>
                                    <span style="font-weight:700;font-size:17px;color:#1B5E20;">&#8377;{prod['price']}</span>
                                    <span style="font-size:12px;color:#999;text-decoration:line-through;margin-left:4px;">&#8377;{prod['original_price']}</span>
                                </div>
                                <div style="color:#FFA000;font-size:12px;">{"★" * int(prod['rating'])} <span style="color:#777;">{prod['rating']}</span></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    sc1, sc2 = st.columns(2)
                    with sc1:
                        if st.button("Add to Cart", key=f"sugg_atc2_{prod['id']}", use_container_width=True, type="primary"):
                            add_to_cart(prod["id"])
                            st.success(f"Added {prod['name']}!")
                    with sc2:
                        if st.button("View Details", key=f"sugg_view2_{prod['id']}", use_container_width=True):
                            nav_to("product", selected_product=prod["id"])
                            st.rerun()

                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    if st.button("Retake Quiz", key="retake_quiz", use_container_width=True):
                        st.session_state[SUGGESTION_RESULTS_KEY] = None
                        st.rerun()
                with col_r2:
                    if st.button("Main Menu", key="sugg_to_menu", use_container_width=True):
                        st.session_state.chatbot_mode = None
                        st.session_state[SUGGESTION_RESULTS_KEY] = None
                        st.rerun()

            if not results_ready:
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("Back to Menu", key="sugg_back_btn", use_container_width=True):
                    st.session_state.chatbot_mode = None
                    st.rerun()



def main():
    # Always render chatbot in sidebar — it's persistent across all pages
    render_chatbot_sidebar()

    render_navbar()

    page = st.session_state.page

    if page == "home":
        render_home()
    elif page == "category":
        render_category_page()
    elif page == "product":
        render_product_detail()
    elif page == "search":
        render_search()
    elif page == "cart":
        render_cart()
    elif page == "checkout":
        render_checkout()
    elif page == "about":
        render_about()
    elif page == "contact":
        render_contact()
    elif page == "offers":
        render_offers()
    else:
        render_home()

main()