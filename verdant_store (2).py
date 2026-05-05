"""
Verdant - Premium Plant E-Commerce Platform
A single-file Streamlit application inspired by premium plant e-commerce design.
"""

import streamlit as st
import pandas as pd
import random
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Verdant | Premium Plants & Care",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "wishlist" not in st.session_state:
    st.session_state.wishlist = set()
if "chatbot_open" not in st.session_state:
    st.session_state.chatbot_open = False
if "chatbot_mode" not in st.session_state:
    st.session_state.chatbot_mode = None
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "active_category" not in st.session_state:
    st.session_state.active_category = None
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "chatbot_diagnosis_done" not in st.session_state:
    st.session_state.chatbot_diagnosis_done = False
if "chatbot_suggestions_done" not in st.session_state:
    st.session_state.chatbot_suggestions_done = False
if "suggestion_answers" not in st.session_state:
    st.session_state.suggestion_answers = {}
if "checkout_done" not in st.session_state:
    st.session_state.checkout_done = False
# PlantPal chatbot state
if "pp_step" not in st.session_state:
    st.session_state.pp_step = "greeting"
if "pp_flow" not in st.session_state:
    st.session_state.pp_flow = None
if "pp_answers" not in st.session_state:
    st.session_state.pp_answers = {}
if "pp_result" not in st.session_state:
    st.session_state.pp_result = None
if "pp_upload_key" not in st.session_state:
    st.session_state.pp_upload_key = 0
if "pp_suggested" not in st.session_state:
    st.session_state.pp_suggested = []
if "plantpal_messages" not in st.session_state:
    st.session_state.plantpal_messages = []
if "plantpal_uploaded_image" not in st.session_state:
    st.session_state.plantpal_uploaded_image = None
if "plantpal_analyzing" not in st.session_state:
    st.session_state.plantpal_analyzing = False

# ─────────────────────────────────────────────
# PRODUCT DATABASE
# ─────────────────────────────────────────────
PRODUCTS = [
    # Indoor Plants
    {"id": 1, "name": "Monstera Deliciosa", "category": "Indoor Plants", "price": 649, "original_price": 899, "rating": 4.8, "reviews": 234, "care_level": "Easy", "image": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400&q=80", "description": "The iconic Swiss cheese plant with dramatic split leaves. Perfect for bright indirect light.", "tags": ["trending", "bestseller"], "stock": 15, "air_purifying": True},
    {"id": 2, "name": "Peace Lily", "category": "Indoor Plants", "price": 399, "original_price": 499, "rating": 4.7, "reviews": 189, "care_level": "Easy", "image": "https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=400&q=80", "description": "Elegant white blooms with glossy dark leaves. Thrives in low light conditions.", "tags": ["air purifying"], "stock": 22, "air_purifying": True},
    {"id": 3, "name": "Fiddle Leaf Fig", "category": "Indoor Plants", "price": 1299, "original_price": 1599, "rating": 4.5, "reviews": 156, "care_level": "Moderate", "image": "https://images.unsplash.com/photo-1631377819268-d716cd610cd2?w=400&q=80", "description": "A statement plant with large violin-shaped leaves. Ideal for bright corners.", "tags": ["premium"], "stock": 8, "air_purifying": False},
    {"id": 4, "name": "Snake Plant", "category": "Indoor Plants", "price": 349, "original_price": 449, "rating": 4.9, "reviews": 412, "care_level": "Very Easy", "image": "https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=400&q=80", "description": "Nearly indestructible with striking upright leaves. Perfect for beginners.", "tags": ["bestseller", "air purifying"], "stock": 35, "air_purifying": True},
    {"id": 5, "name": "Pothos Golden", "category": "Indoor Plants", "price": 199, "original_price": 249, "rating": 4.8, "reviews": 523, "care_level": "Very Easy", "image": "https://images.unsplash.com/photo-1602923668104-8f9e03e77e62?w=400&q=80", "description": "Trailing vines with heart-shaped golden-green leaves. Great for shelves.", "tags": ["bestseller"], "stock": 40, "air_purifying": True},
    {"id": 6, "name": "ZZ Plant", "category": "Indoor Plants", "price": 549, "original_price": 699, "rating": 4.7, "reviews": 198, "care_level": "Very Easy", "image": "https://images.unsplash.com/photo-1632207691143-643e2a9a9361?w=400&q=80", "description": "Glossy dark green leaves on arching stems. Drought tolerant and low maintenance.", "tags": [], "stock": 18, "air_purifying": False},
    # Outdoor Plants
    {"id": 7, "name": "Bougainvillea", "category": "Outdoor Plants", "price": 449, "original_price": 599, "rating": 4.6, "reviews": 167, "care_level": "Moderate", "image": "https://images.unsplash.com/photo-1524146128017-b9dd0bfd2778?w=400&q=80", "description": "Vibrant magenta bracts that bloom profusely in full sun. A garden showstopper.", "tags": ["trending"], "stock": 20, "air_purifying": False},
    {"id": 8, "name": "Hibiscus Red", "category": "Outdoor Plants", "price": 379, "original_price": 499, "rating": 4.5, "reviews": 143, "care_level": "Easy", "image": "https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=400&q=80", "description": "Large trumpet-shaped blooms in brilliant red. Attracts pollinators.", "tags": [], "stock": 25, "air_purifying": False},
    {"id": 9, "name": "Jasmine Climber", "category": "Outdoor Plants", "price": 299, "original_price": 399, "rating": 4.8, "reviews": 201, "care_level": "Easy", "image": "https://images.unsplash.com/photo-1587530285270-76e3c3df0e43?w=400&q=80", "description": "Fragrant white star-shaped flowers on vigorous climbing vines.", "tags": ["bestseller"], "stock": 30, "air_purifying": False},
    # Air Purifying
    {"id": 10, "name": "Spider Plant", "category": "Air Purifying Plants", "price": 249, "original_price": 299, "rating": 4.7, "reviews": 334, "care_level": "Very Easy", "image": "https://images.unsplash.com/photo-1509423350716-97f9360b4e09?w=400&q=80", "description": "Arching green-white striped leaves with baby plantlets. NASA approved air purifier.", "tags": ["air purifying", "bestseller"], "stock": 45, "air_purifying": True},
    {"id": 11, "name": "Areca Palm", "category": "Air Purifying Plants", "price": 799, "original_price": 999, "rating": 4.6, "reviews": 178, "care_level": "Moderate", "image": "https://images.unsplash.com/photo-1604176354204-9268737828e4?w=400&q=80", "description": "Feathery arching fronds that add tropical elegance. Excellent humidity regulator.", "tags": ["air purifying"], "stock": 12, "air_purifying": True},
    {"id": 12, "name": "Rubber Plant", "category": "Air Purifying Plants", "price": 599, "original_price": 749, "rating": 4.5, "reviews": 145, "care_level": "Easy", "image": "https://images.unsplash.com/photo-1545241047-6083a3684587?w=400&q=80", "description": "Bold burgundy-green leaves with a waxy sheen. Powerful formaldehyde remover.", "tags": ["air purifying"], "stock": 16, "air_purifying": True},
    # Succulents
    {"id": 13, "name": "Echeveria Collection", "category": "Succulents", "price": 349, "original_price": 449, "rating": 4.8, "reviews": 267, "care_level": "Very Easy", "image": "https://images.unsplash.com/photo-1559043099-b9d6e41e50f8?w=400&q=80", "description": "A curated set of rosette-forming echeverias in pastel hues. Minimal water needed.", "tags": ["trending", "gifting"], "stock": 30, "air_purifying": False},
    {"id": 14, "name": "Cactus Trio", "category": "Succulents", "price": 299, "original_price": 399, "rating": 4.6, "reviews": 189, "care_level": "Very Easy", "image": "https://images.unsplash.com/photo-1520302519878-3592f1048ffc?w=400&q=80", "description": "Three sculptural cacti in earthy ceramic pots. Desert beauty for windowsills.", "tags": ["gifting"], "stock": 28, "air_purifying": False},
    {"id": 15, "name": "Aloe Vera", "category": "Succulents", "price": 199, "original_price": 249, "rating": 4.9, "reviews": 456, "care_level": "Very Easy", "image": "https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?w=400&q=80", "description": "The ultimate healing plant. Soothing gel for burns and skincare.", "tags": ["bestseller", "medicinal"], "stock": 50, "air_purifying": True},
    # Bonsai
    {"id": 16, "name": "Ficus Bonsai", "category": "Bonsai Plants", "price": 1899, "original_price": 2499, "rating": 4.7, "reviews": 89, "care_level": "Expert", "image": "https://images.unsplash.com/photo-1599598425947-5202edd56bdc?w=400&q=80", "description": "A masterfully shaped Ficus bonsai. Each piece is a living work of art.", "tags": ["premium", "gifting"], "stock": 6, "air_purifying": False},
    {"id": 17, "name": "Jade Bonsai", "category": "Bonsai Plants", "price": 1499, "original_price": 1999, "rating": 4.6, "reviews": 67, "care_level": "Moderate", "image": "https://images.unsplash.com/photo-1598880940080-ff9a29891b85?w=400&q=80", "description": "Gnarled trunk with thick succulent leaves. Symbol of prosperity and good fortune.", "tags": ["premium", "gifting"], "stock": 8, "air_purifying": False},
    # Flowering
    {"id": 18, "name": "Anthurium Red", "category": "Flowering Plants", "price": 549, "original_price": 699, "rating": 4.7, "reviews": 213, "care_level": "Moderate", "image": "https://images.unsplash.com/photo-1616499370260-485b3e5ed653?w=400&q=80", "description": "Waxy heart-shaped red spathes that last for months. Long-lasting indoor bloomer.", "tags": ["gifting", "trending"], "stock": 20, "air_purifying": False},
    {"id": 19, "name": "Orchid White", "category": "Flowering Plants", "price": 799, "original_price": 999, "rating": 4.8, "reviews": 178, "care_level": "Moderate", "image": "https://images.unsplash.com/photo-1566907225472-514215c10e38?w=400&q=80", "description": "Elegant Phalaenopsis with cascading white blooms. The queen of indoor plants.", "tags": ["premium", "gifting"], "stock": 14, "air_purifying": False},
    # Seeds
    {"id": 20, "name": "Tomato Seeds Pack", "category": "Vegetable Seeds", "price": 99, "original_price": 149, "rating": 4.6, "reviews": 312, "care_level": "Easy", "image": "https://images.unsplash.com/photo-1592921870789-04563d55041c?w=400&q=80", "description": "Premium hybrid tomato seeds with 95% germination rate. 4 varieties included.", "tags": ["bestseller"], "stock": 100, "air_purifying": False},
    {"id": 21, "name": "Sunflower Seeds", "category": "Flower Seeds", "price": 79, "original_price": 99, "rating": 4.8, "reviews": 445, "care_level": "Very Easy", "image": "https://images.unsplash.com/photo-1596360415045-c47ce93c27c7?w=400&q=80", "description": "Giant sunflower variety reaching 6 feet. Perfect for cut flowers.", "tags": ["bestseller"], "stock": 80, "air_purifying": False},
    {"id": 22, "name": "Herb Garden Seeds Kit", "category": "Herb Seeds", "price": 249, "original_price": 349, "rating": 4.7, "reviews": 267, "care_level": "Easy", "image": "https://images.unsplash.com/photo-1466637574441-749b8f19452f?w=400&q=80", "description": "Basil, mint, coriander, parsley — everything for a kitchen herb garden.", "tags": ["trending", "gifting"], "stock": 60, "air_purifying": False},
    {"id": 23, "name": "Microgreens Mix", "category": "Microgreen Seeds", "price": 149, "original_price": 199, "rating": 4.5, "reviews": 189, "care_level": "Very Easy", "image": "https://images.unsplash.com/photo-1556760544-74068565f05c?w=400&q=80", "description": "Nutrient-dense microgreen blend ready to harvest in 7 days.", "tags": ["trending"], "stock": 75, "air_purifying": False},
    # Plant Care
    {"id": 24, "name": "NPK Granular Fertilizer", "category": "Fertilizers", "price": 299, "original_price": 399, "rating": 4.7, "reviews": 234, "care_level": None, "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&q=80", "description": "Slow-release balanced fertilizer for all plants. 3-month formula.", "tags": ["bestseller"], "stock": 50, "air_purifying": False},
    {"id": 25, "name": "Terracotta Planter Set", "category": "Pots & Planters", "price": 599, "original_price": 799, "rating": 4.8, "reviews": 178, "care_level": None, "image": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=400&q=80", "description": "Handcrafted terracotta pots in 3 sizes with saucers. Natural clay finish.", "tags": ["trending"], "stock": 25, "air_purifying": False},
    {"id": 26, "name": "Premium Potting Mix", "category": "Soil & Compost", "price": 349, "original_price": 449, "rating": 4.9, "reviews": 345, "care_level": None, "image": "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=400&q=80", "description": "pH balanced potting mix with perlite and coconut coir. For all indoor plants.", "tags": ["bestseller"], "stock": 40, "air_purifying": False},
    {"id": 27, "name": "Neem Oil Spray", "category": "Pest Control", "price": 199, "original_price": 249, "rating": 4.6, "reviews": 267, "care_level": None, "image": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400&q=80", "description": "Pure cold-pressed neem oil for organic pest management. Ready to use.", "tags": ["bestseller"], "stock": 60, "air_purifying": False},
    {"id": 28, "name": "Copper Watering Can", "category": "Watering Accessories", "price": 899, "original_price": 1199, "rating": 4.8, "reviews": 134, "care_level": None, "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&q=80", "description": "Elegant 2L copper-finish watering can with long spout for precise watering.", "tags": ["premium", "gifting"], "stock": 15, "air_purifying": False},
    {"id": 29, "name": "Garden Tool Set", "category": "Gardening Tools", "price": 749, "original_price": 999, "rating": 4.7, "reviews": 189, "care_level": None, "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&q=80", "description": "5-piece stainless steel tool set: trowel, cultivator, weeder, fork, transplanter.", "tags": ["trending"], "stock": 20, "air_purifying": False},
    {"id": 30, "name": "Seaweed Plant Tonic", "category": "Plant Medicines", "price": 249, "original_price": 299, "rating": 4.5, "reviews": 156, "care_level": None, "image": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400&q=80", "description": "Organic seaweed extract that boosts root growth and plant immunity.", "tags": [], "stock": 45, "air_purifying": False},
]

PRODUCTS_DF = pd.DataFrame(PRODUCTS)

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def add_to_cart(product_id, quantity=1):
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += quantity
    else:
        st.session_state.cart[product_id] = quantity

def remove_from_cart(product_id):
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]

def get_cart_total():
    total = 0
    for pid, qty in st.session_state.cart.items():
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if product:
            total += product["price"] * qty
    return total

def get_cart_count():
    return sum(st.session_state.cart.values())

def get_product_by_id(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)

def star_rating(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "½" * half + "☆" * empty

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --green-dark:   #1B5E20;
        --green-main:   #2E7D32;
        --green-mid:    #388E3C;
        --green-light:  #C8E6C9;
        --green-xlight: #F1F8F1;
        --pink-main:    #F8BBD0;
        --pink-dark:    #E91E63;
        --cream:        #FAFAF7;
        --neutral-100:  #F5F5F0;
        --neutral-200:  #E8E8E0;
        --neutral-600:  #6B6B6B;
        --neutral-800:  #2A2A2A;
        --gold:         #D4A853;
        --shadow-sm:    0 2px 8px rgba(0,0,0,0.08);
        --shadow-md:    0 4px 20px rgba(0,0,0,0.12);
        --shadow-lg:    0 8px 40px rgba(0,0,0,0.16);
        --radius-sm:    8px;
        --radius-md:    12px;
        --radius-lg:    20px;
        --radius-xl:    32px;
    }

    /* ── Reset & Base ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--neutral-800);
    }
    .stApp {
        background: var(--cream);
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    section[data-testid="stSidebar"] { display: none !important; }
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ── Hide default Streamlit padding ── */
    .main > div { padding-top: 0 !important; }

    /* ── Top Navigation Bar ── */
    .navbar {
        background: #ffffff;
        border-bottom: 1px solid var(--neutral-200);
        padding: 0 40px;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: var(--shadow-sm);
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 72px;
    }
    .nav-brand {
        font-family: 'Playfair Display', serif;
        font-size: 26px;
        font-weight: 700;
        color: var(--green-main);
        letter-spacing: -0.5px;
        text-decoration: none;
    }
    .nav-brand span { color: var(--green-dark); }
    .nav-tagline {
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--neutral-600);
        display: block;
        margin-top: -4px;
    }
    .nav-links {
        display: flex;
        gap: 32px;
        align-items: center;
    }
    .nav-link {
        font-size: 14px;
        font-weight: 500;
        color: var(--neutral-800);
        text-decoration: none;
        letter-spacing: 0.3px;
        cursor: pointer;
        transition: color 0.2s;
    }
    .nav-link:hover { color: var(--green-main); }
    .nav-actions { display: flex; align-items: center; gap: 16px; }
    .cart-badge {
        background: var(--green-main);
        color: white;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 20px;
        margin-left: 4px;
    }

    /* ── Hero Banner ── */
    .hero {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 40%, #388E3C 70%, #43A047 100%);
        padding: 80px 80px;
        position: relative;
        overflow: hidden;
        min-height: 500px;
        display: flex;
        align-items: center;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: 30%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(248,187,208,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-content { position: relative; z-index: 2; max-width: 600px; }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 6px 16px;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 52px;
        font-weight: 700;
        color: white;
        line-height: 1.15;
        margin: 0 0 16px 0;
    }
    .hero-title em { font-style: italic; color: var(--pink-main); }
    .hero-subtitle {
        font-size: 17px;
        color: rgba(255,255,255,0.85);
        line-height: 1.6;
        margin-bottom: 36px;
    }
    .hero-cta {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: white;
        color: var(--green-main);
        padding: 14px 32px;
        border-radius: 40px;
        font-size: 15px;
        font-weight: 600;
        text-decoration: none;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        cursor: pointer;
        transition: all 0.2s;
        border: none;
    }
    .hero-cta:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    }
    .hero-cta-secondary {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: transparent;
        color: white;
        padding: 14px 32px;
        border-radius: 40px;
        font-size: 15px;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.4);
        cursor: pointer;
        margin-left: 12px;
        transition: all 0.2s;
    }
    .hero-cta-secondary:hover { background: rgba(255,255,255,0.1); }
    .hero-stats {
        display: flex;
        gap: 40px;
        margin-top: 40px;
    }
    .hero-stat-number {
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        font-weight: 700;
        color: white;
    }
    .hero-stat-label {
        font-size: 12px;
        color: rgba(255,255,255,0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .hero-image-side {
        position: absolute;
        right: 0;
        top: 0;
        width: 50%;
        height: 100%;
        overflow: hidden;
    }
    .hero-image-side img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.35;
        mix-blend-mode: luminosity;
    }

    /* ── Section Titles ── */
    .section-wrap { padding: 60px 60px; }
    .section-wrap-tight { padding: 40px 60px; }
    .section-header { margin-bottom: 36px; }
    .section-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: var(--green-main);
        margin-bottom: 8px;
    }
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 36px;
        font-weight: 700;
        color: var(--neutral-800);
        line-height: 1.2;
        margin: 0;
    }
    .section-subtitle {
        font-size: 16px;
        color: var(--neutral-600);
        margin-top: 10px;
        max-width: 520px;
    }

    /* ── Category Cards ── */
    .cat-card {
        border-radius: var(--radius-lg);
        overflow: hidden;
        position: relative;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        aspect-ratio: 3/4;
        background: var(--green-light);
    }
    .cat-card:hover {
        transform: translateY(-6px);
        box-shadow: var(--shadow-lg);
    }
    .cat-card img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
    }
    .cat-card:hover img { transform: scale(1.05); }
    .cat-card-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(transparent, rgba(0,0,0,0.65));
        padding: 20px 16px 16px;
        color: white;
    }
    .cat-card-name {
        font-family: 'Playfair Display', serif;
        font-size: 18px;
        font-weight: 600;
    }
    .cat-card-count { font-size: 12px; opacity: 0.8; }

    /* ── Product Cards ── */
    .product-card {
        background: white;
        border-radius: var(--radius-md);
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        border: 1px solid var(--neutral-200);
        height: 100%;
    }
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
        border-color: var(--green-light);
    }
    .product-img-wrap {
        position: relative;
        overflow: hidden;
        aspect-ratio: 1/1;
        background: var(--neutral-100);
    }
    .product-img-wrap img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.4s ease;
    }
    .product-card:hover .product-img-wrap img { transform: scale(1.06); }
    .product-badge {
        position: absolute;
        top: 10px;
        left: 10px;
        background: var(--green-main);
        color: white;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.5px;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    .product-badge-sale {
        background: #E53935;
    }
    .product-badge-new {
        background: var(--pink-dark);
    }
    .product-body { padding: 16px; }
    .product-category {
        font-size: 11px;
        color: var(--green-main);
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .product-name {
        font-family: 'Playfair Display', serif;
        font-size: 17px;
        font-weight: 600;
        color: var(--neutral-800);
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .product-description {
        font-size: 13px;
        color: var(--neutral-600);
        line-height: 1.5;
        margin-bottom: 10px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .product-rating { font-size: 13px; color: #F9A825; margin-bottom: 10px; }
    .product-review-count { color: var(--neutral-600); font-size: 12px; margin-left: 4px; }
    .product-price-row { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
    .product-price {
        font-size: 20px;
        font-weight: 700;
        color: var(--neutral-800);
    }
    .product-price-original {
        font-size: 14px;
        color: var(--neutral-600);
        text-decoration: line-through;
    }
    .product-discount {
        font-size: 12px;
        font-weight: 600;
        color: #E53935;
        background: #FFEBEE;
        padding: 2px 6px;
        border-radius: 4px;
    }
    .product-care {
        font-size: 11px;
        color: var(--neutral-600);
        background: var(--green-xlight);
        border: 1px solid var(--green-light);
        display: inline-block;
        padding: 2px 8px;
        border-radius: 20px;
        margin-bottom: 12px;
    }
    .btn-cart {
        width: 100%;
        background: var(--green-main);
        color: white;
        border: none;
        border-radius: var(--radius-sm);
        padding: 10px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0.3px;
        transition: background 0.2s ease;
    }
    .btn-cart:hover { background: var(--green-dark); }
    .btn-cart-outline {
        width: 100%;
        background: white;
        color: var(--green-main);
        border: 1.5px solid var(--green-main);
        border-radius: var(--radius-sm);
        padding: 9px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        font-family: 'DM Sans', sans-serif;
        transition: all 0.2s ease;
    }
    .btn-cart-outline:hover {
        background: var(--green-xlight);
    }

    /* ── Promo Banner ── */
    .promo-banner {
        background: linear-gradient(120deg, var(--pink-main) 0%, #FCE4EC 50%, var(--pink-main) 100%);
        border-radius: var(--radius-lg);
        padding: 32px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0 60px 60px;
    }
    .promo-title {
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        font-weight: 700;
        color: var(--neutral-800);
    }
    .promo-subtitle { font-size: 15px; color: var(--neutral-600); margin-top: 6px; }
    .promo-btn {
        background: var(--green-main);
        color: white;
        padding: 12px 28px;
        border-radius: 40px;
        font-size: 14px;
        font-weight: 600;
        border: none;
        cursor: pointer;
        font-family: 'DM Sans', sans-serif;
        transition: background 0.2s;
        white-space: nowrap;
    }
    .promo-btn:hover { background: var(--green-dark); }

    /* ── Trust Strip ── */
    .trust-strip {
        background: var(--green-xlight);
        border-top: 1px solid var(--green-light);
        border-bottom: 1px solid var(--green-light);
        padding: 20px 60px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }
    .trust-item { text-align: center; }
    .trust-icon { font-size: 22px; margin-bottom: 6px; color: var(--green-main); }
    .trust-title { font-size: 14px; font-weight: 600; color: var(--neutral-800); }
    .trust-desc { font-size: 12px; color: var(--neutral-600); }

    /* ── Testimonials ── */
    .testimonial-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 24px;
        border: 1px solid var(--neutral-200);
        transition: box-shadow 0.2s;
    }
    .testimonial-card:hover { box-shadow: var(--shadow-md); }
    .testimonial-stars { color: #F9A825; font-size: 14px; margin-bottom: 12px; }
    .testimonial-text {
        font-size: 14px;
        color: var(--neutral-600);
        line-height: 1.6;
        font-style: italic;
        margin-bottom: 16px;
    }
    .testimonial-author {
        font-size: 14px;
        font-weight: 600;
        color: var(--neutral-800);
    }
    .testimonial-location { font-size: 12px; color: var(--neutral-600); }

    /* ── Newsletter ── */
    .newsletter-section {
        background: linear-gradient(135deg, var(--green-dark), var(--green-main));
        padding: 60px;
        text-align: center;
        color: white;
    }
    .newsletter-title {
        font-family: 'Playfair Display', serif;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .newsletter-subtitle { font-size: 16px; opacity: 0.85; margin-bottom: 32px; }
    .newsletter-input-wrap {
        display: flex;
        max-width: 480px;
        margin: 0 auto;
        border-radius: 40px;
        overflow: hidden;
        box-shadow: var(--shadow-md);
    }

    /* ── Footer ── */
    .footer {
        background: #0D2B0F;
        color: rgba(255,255,255,0.7);
        padding: 60px;
    }
    .footer-brand {
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        font-weight: 700;
        color: white;
        margin-bottom: 12px;
    }
    .footer-brand-desc { font-size: 14px; line-height: 1.6; max-width: 280px; margin-bottom: 20px; }
    .footer-heading { font-size: 13px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: white; margin-bottom: 16px; }
    .footer-link { font-size: 13px; color: rgba(255,255,255,0.6); display: block; margin-bottom: 8px; cursor: pointer; transition: color 0.2s; }
    .footer-link:hover { color: var(--green-light); }
    .footer-bottom {
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 24px;
        margin-top: 40px;
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        color: rgba(255,255,255,0.4);
    }

    /* ── Cart Page ── */
    .cart-item {
        background: white;
        border-radius: var(--radius-md);
        padding: 20px;
        border: 1px solid var(--neutral-200);
        margin-bottom: 12px;
        display: flex;
        gap: 16px;
        align-items: center;
    }
    .cart-item img { width: 80px; height: 80px; object-fit: cover; border-radius: var(--radius-sm); }
    .cart-item-info { flex: 1; }
    .cart-item-name { font-weight: 600; font-size: 15px; margin-bottom: 4px; }
    .cart-item-price { color: var(--green-main); font-weight: 700; }

    /* ── Order Summary ── */
    .order-summary {
        background: white;
        border-radius: var(--radius-md);
        padding: 28px;
        border: 1px solid var(--neutral-200);
        position: sticky;
        top: 90px;
    }
    .order-row {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        margin-bottom: 12px;
        color: var(--neutral-600);
    }
    .order-total {
        display: flex;
        justify-content: space-between;
        font-size: 18px;
        font-weight: 700;
        color: var(--neutral-800);
        border-top: 1px solid var(--neutral-200);
        padding-top: 16px;
        margin-top: 8px;
    }

    /* ── Search Results ── */
    .search-result-info {
        background: var(--green-xlight);
        border-left: 3px solid var(--green-main);
        padding: 12px 20px;
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        margin-bottom: 24px;
        font-size: 14px;
        color: var(--neutral-600);
    }

    /* ── Chatbot ── */
    .chatbot-container {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 12px;
    }
    .chatbot-window {
        width: 380px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 12px 48px rgba(0,0,0,0.18), 0 0 0 1px rgba(46,125,50,0.08);
        overflow: hidden;
        animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        border: 1px solid var(--neutral-200);
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px) scale(0.96); }
        to   { opacity: 1; transform: translateY(0)    scale(1);    }
    }
    .chatbot-header {
        background: linear-gradient(135deg, var(--green-dark), var(--green-main));
        padding: 18px 20px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .chatbot-header-title {
        font-family: 'Playfair Display', serif;
        font-size: 17px;
        font-weight: 700;
    }
    .chatbot-header-sub { font-size: 11px; opacity: 0.8; }
    .chatbot-body { padding: 20px; max-height: 480px; overflow-y: auto; }
    .chatbot-option {
        background: var(--green-xlight);
        border: 1.5px solid var(--green-light);
        border-radius: var(--radius-md);
        padding: 16px;
        cursor: pointer;
        margin-bottom: 10px;
        transition: all 0.2s;
        text-align: left;
    }
    .chatbot-option:hover {
        background: var(--green-light);
        border-color: var(--green-main);
        transform: translateX(4px);
    }
    .chatbot-option-title { font-weight: 600; font-size: 14px; color: var(--neutral-800); }
    .chatbot-option-desc { font-size: 12px; color: var(--neutral-600); margin-top: 3px; }
    .chatbot-fab {
        width: 58px;
        height: 58px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--green-dark), var(--green-main));
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(46,125,50,0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        color: white;
        font-family: 'DM Sans', sans-serif;
    }
    .chatbot-fab:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 28px rgba(46,125,50,0.5);
    }

    /* ── Page Header ── */
    .page-header {
        background: linear-gradient(135deg, var(--green-dark), var(--green-main));
        padding: 48px 60px;
        color: white;
    }
    .page-header-title {
        font-family: 'Playfair Display', serif;
        font-size: 40px;
        font-weight: 700;
        margin: 0;
    }
    .page-header-breadcrumb {
        font-size: 13px;
        opacity: 0.7;
        margin-top: 8px;
    }

    /* ── Filter Sidebar ── */
    .filter-panel {
        background: white;
        border-radius: var(--radius-md);
        padding: 24px;
        border: 1px solid var(--neutral-200);
        position: sticky;
        top: 90px;
    }
    .filter-heading {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: var(--neutral-800);
        margin-bottom: 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--neutral-200);
    }

    /* ── About ── */
    .about-hero {
        background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
        padding: 80px 60px;
        border-radius: 0;
    }
    .about-value-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 24px;
        border: 1px solid var(--green-light);
        text-align: center;
        transition: box-shadow 0.2s;
    }
    .about-value-card:hover { box-shadow: var(--shadow-md); }
    .about-value-icon { font-size: 32px; margin-bottom: 12px; }
    .about-value-title { font-weight: 700; font-size: 16px; margin-bottom: 8px; }

    /* ── Contact ── */
    .contact-info-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 28px;
        border: 1px solid var(--neutral-200);
        text-align: center;
        transition: box-shadow 0.2s;
    }
    .contact-info-card:hover { box-shadow: var(--shadow-md); }

    /* ── Streamlit Overrides ── */
    .stButton button {
        border-radius: var(--radius-sm) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    .stButton button[kind="primary"] {
        background: var(--green-main) !important;
        border-color: var(--green-main) !important;
        color: white !important;
    }
    .stButton button[kind="primary"]:hover {
        background: var(--green-dark) !important;
        border-color: var(--green-dark) !important;
    }
    .stTextInput input {
        border-radius: var(--radius-sm) !important;
        border-color: var(--neutral-200) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stSelectbox select {
        border-radius: var(--radius-sm) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    div[data-testid="stExpander"] {
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--neutral-200) !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--green-main) !important;
    }
    .stSuccess {
        border-radius: var(--radius-sm) !important;
    }
    .stAlert {
        border-radius: var(--radius-sm) !important;
    }
    div[data-testid="column"] > div { height: 100%; }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────
def render_navbar():
    cart_count = get_cart_count()
    cart_badge = f'<span class="cart-badge">{cart_count}</span>' if cart_count > 0 else ""

    st.markdown(f"""
    <div class="navbar">
        <div>
            <a class="nav-brand">Verdant<span>.</span></a>
            <span class="nav-tagline">Premium Plant Boutique</span>
        </div>
        <div class="nav-links">
            <span class="nav-link">Home</span>
            <span class="nav-link">Plants</span>
            <span class="nav-link">Seeds</span>
            <span class="nav-link">Plant Care</span>
            <span class="nav-link" style="color:#E53935;font-weight:600;">Offers</span>
            <span class="nav-link">About Us</span>
            <span class="nav-link">Contact</span>
        </div>
        <div class="nav-actions">
            <span style="font-size:20px;cursor:pointer;color:#2E7D32;">&#128269;</span>
            <span style="font-size:20px;cursor:pointer;color:#2E7D32;">&#10084;</span>
            <span style="font-size:20px;cursor:pointer;color:#2E7D32;">&#128722;{cart_badge}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Actual navigation using columns
    cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1.5, 2])
    pages = ["Home", "Plants", "Seeds", "Plant Care", "Offers", "About Us", "Contact", "Cart", "PlantPal 🌿"]
    for i, (col, page) in enumerate(zip(cols[:9], pages)):
        with col:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page.replace(" 🌿", "")
                st.session_state.active_category = None
                st.rerun()

    with cols[9]:
        st.text_input("Search plants...", key="nav_search",
                      placeholder="Search plants...",
                      label_visibility="collapsed")
        if st.session_state.get("nav_search"):
            st.session_state.search_query = st.session_state.nav_search
            st.session_state.page = "Search"
            st.rerun()

# ─────────────────────────────────────────────
# PRODUCT CARD COMPONENT
# ─────────────────────────────────────────────
def render_product_card(product, key_suffix=""):
    discount = int((1 - product["price"] / product["original_price"]) * 100)
    tag = ""
    if "bestseller" in product["tags"]:
        tag = '<span class="product-badge">Bestseller</span>'
    elif discount >= 20:
        tag = f'<span class="product-badge product-badge-sale">-{discount}%</span>'
    elif "trending" in product["tags"]:
        tag = '<span class="product-badge product-badge-new">Trending</span>'

    care_html = ""
    if product.get("care_level"):
        care_html = f'<span class="product-care">Care: {product["care_level"]}</span><br>'

    stars = "★" * int(product["rating"]) + ("½" if product["rating"] % 1 >= 0.5 else "")

    st.markdown(f"""
    <div class="product-card">
        <div class="product-img-wrap">
            <img src="{product['image']}" alt="{product['name']}" loading="lazy" />
            {tag}
        </div>
        <div class="product-body">
            <div class="product-category">{product['category']}</div>
            <div class="product-name">{product['name']}</div>
            <div class="product-description">{product['description']}</div>
            <div class="product-rating">
                {stars} <span class="product-review-count">({product['reviews']} reviews)</span>
            </div>
            {care_html}
            <div class="product-price-row">
                <span class="product-price">&#8377;{product['price']:,}</span>
                <span class="product-price-original">&#8377;{product['original_price']:,}</span>
                <span class="product-discount">-{discount}%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Add to Cart", key=f"cart_{product['id']}_{key_suffix}", use_container_width=True, type="primary"):
            add_to_cart(product["id"])
            st.success(f"'{product['name']}' added to cart!")
            st.rerun()
    with col2:
        heart = "♥" if product["id"] in st.session_state.wishlist else "♡"
        if st.button(heart, key=f"wish_{product['id']}_{key_suffix}", use_container_width=True):
            if product["id"] in st.session_state.wishlist:
                st.session_state.wishlist.remove(product["id"])
            else:
                st.session_state.wishlist.add(product["id"])
            st.rerun()

# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────
def render_home():
    # Hero
    st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <div class="hero-badge">New Arrivals 2025</div>
            <h1 class="hero-title">
                Bring <em>Nature</em><br>Into Your Space
            </h1>
            <p class="hero-subtitle">
                Handpicked premium plants delivered with care.<br>
                Transform your home into a living sanctuary.
            </p>
            <div class="hero-stats">
                <div>
                    <div class="hero-stat-number">500+</div>
                    <div class="hero-stat-label">Plant Varieties</div>
                </div>
                <div>
                    <div class="hero-stat-number">50K+</div>
                    <div class="hero-stat-label">Happy Customers</div>
                </div>
                <div>
                    <div class="hero-stat-number">4.9</div>
                    <div class="hero-stat-label">Average Rating</div>
                </div>
            </div>
        </div>
        <div class="hero-image-side">
            <img src="https://images.unsplash.com/photo-1545239351-ef35f43d514b?w=800&q=80" alt="Plants" />
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Trust Strip
    st.markdown("""
    <div class="trust-strip">
        <div class="trust-item">
            <div class="trust-icon">&#9989;</div>
            <div class="trust-title">Expert Curated</div>
            <div class="trust-desc">Every plant selected by botanists</div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">&#128666;</div>
            <div class="trust-title">Safe Delivery</div>
            <div class="trust-desc">Eco-friendly protective packaging</div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">&#128218;</div>
            <div class="trust-title">Care Guides</div>
            <div class="trust-desc">Expert growing instructions included</div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">&#128260;</div>
            <div class="trust-title">30-Day Guarantee</div>
            <div class="trust-desc">Plant replacement promise</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Featured Categories
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-label">Shop by Category</div>
        <h2 class="section-title">Find Your Perfect Plant</h2>
        <p class="section-subtitle">Browse our carefully organized collections to discover plants that suit your lifestyle and space.</p>
    </div>
    """, unsafe_allow_html=True)

    cat_data = [
        {"name": "Indoor Plants", "count": "120+ varieties", "img": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80"},
        {"name": "Air Purifying", "count": "45+ varieties", "img": "https://images.unsplash.com/photo-1620127807580-990c3eceChronicles4?w=400&q=80"},
        {"name": "Succulents", "count": "80+ varieties", "img": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&q=80"},
        {"name": "Bonsai Plants", "count": "30+ varieties", "img": "https://images.unsplash.com/photo-1599598425947-5202edd56bdc?w=400&q=80"},
        {"name": "Flowering Plants", "count": "95+ varieties", "img": "https://images.unsplash.com/photo-1462275646964-a0e3386b89fa?w=400&q=80"},
        {"name": "Outdoor Plants", "count": "110+ varieties", "img": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&q=80"},
    ]
    cols = st.columns(6)
    for col, cat in zip(cols, cat_data):
        with col:
            st.markdown(f"""
            <div class="cat-card" onclick="">
                <img src="{cat['img']}" alt="{cat['name']}" loading="lazy" />
                <div class="cat-card-overlay">
                    <div class="cat-card-name">{cat['name']}</div>
                    <div class="cat-card-count">{cat['count']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(cat["name"], key=f"cat_btn_{cat['name']}", use_container_width=True):
                st.session_state.page = "Plants"
                st.session_state.active_category = cat["name"]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Promo Banner
    st.markdown("""
    <div class="promo-banner">
        <div>
            <div class="promo-title">Summer Sale — Up to 40% Off</div>
            <div class="promo-subtitle">Limited time offer on our bestselling indoor plants and care products.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Shop the Sale", key="promo_shop", type="primary", use_container_width=True):
            st.session_state.page = "Offers"
            st.rerun()

    # Best Sellers
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-label">Most Loved</div>
        <h2 class="section-title">Bestselling Plants</h2>
        <p class="section-subtitle">Plants our community loves most — proven growers with excellent care guides.</p>
    </div>
    """, unsafe_allow_html=True)

    bestsellers = [p for p in PRODUCTS if "bestseller" in p.get("tags", [])][:4]
    cols = st.columns(4)
    for col, product in zip(cols, bestsellers):
        with col:
            render_product_card(product, key_suffix="home_bs")
    st.markdown('</div>', unsafe_allow_html=True)

    # Trending Section
    st.markdown('<div class="section-wrap" style="background:var(--green-xlight);padding:60px;">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-label">Right Now</div>
        <h2 class="section-title">Trending This Season</h2>
    </div>
    """, unsafe_allow_html=True)

    trending = [p for p in PRODUCTS if "trending" in p.get("tags", [])][:4]
    cols = st.columns(4)
    for col, product in zip(cols, trending):
        with col:
            render_product_card(product, key_suffix="home_tr")
    st.markdown('</div>', unsafe_allow_html=True)

    # Testimonials
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-label">Customer Love</div>
        <h2 class="section-title">What Our Plant Parents Say</h2>
    </div>
    """, unsafe_allow_html=True)

    testimonials = [
        {"stars": 5, "text": "The Monstera I ordered arrived in perfect condition with detailed care instructions. It has been thriving for three months now. The packaging was thoughtful and eco-friendly.", "author": "Priya Sharma", "location": "Mumbai, Maharashtra"},
        {"stars": 5, "text": "Absolutely love the quality of plants from Verdant. My air-purifying collection has transformed my apartment's air quality noticeably. Will definitely order again.", "author": "Aditya Mehta", "location": "Bangalore, Karnataka"},
        {"stars": 5, "text": "The bonsai I gifted my mother on her birthday was stunning. The presentation box was premium and she was thrilled. Excellent customer service throughout.", "author": "Sneha Patel", "location": "Ahmedabad, Gujarat"},
        {"stars": 5, "text": "As someone new to gardening, the care guides included with every plant have been invaluable. My succulents are thriving and I am hooked on growing my collection.", "author": "Rohan Gupta", "location": "Delhi, NCR"},
    ]
    cols = st.columns(4)
    for col, t in zip(cols, testimonials):
        with col:
            st.markdown(f"""
            <div class="testimonial-card">
                <div class="testimonial-stars">{"★" * t['stars']}</div>
                <div class="testimonial-text">"{t['text']}"</div>
                <div class="testimonial-author">{t['author']}</div>
                <div class="testimonial-location">{t['location']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Newsletter
    st.markdown("""
    <div class="newsletter-section">
        <div class="newsletter-title">Join the Verdant Community</div>
        <div class="newsletter-subtitle">Get exclusive plant care tips, early access to new arrivals, and seasonal offers delivered to your inbox.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("Your email address", placeholder="Enter your email address", label_visibility="collapsed")
        if st.button("Subscribe — It is Free", key="newsletter_sub", type="primary", use_container_width=True):
            if email:
                st.success("Welcome to Verdant! Your first discount code has been sent.")
            else:
                st.warning("Please enter a valid email address.")

    render_footer()

# ─────────────────────────────────────────────
# PLANTS PAGE
# ─────────────────────────────────────────────
def render_plants_page():
    plant_categories = ["All", "Indoor Plants", "Outdoor Plants", "Air Purifying Plants",
                        "Oxygen Rich Plants", "Flowering Plants", "Succulents",
                        "Bonsai Plants", "Gifting Plants"]

    active_cat = st.session_state.get("active_category") or "All"

    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-header-title">Plants Collection</h1>
        <div class="page-header-breadcrumb">Home / Plants / {active_cat}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:40px 60px;">', unsafe_allow_html=True)

    sidebar_col, main_col = st.columns([1, 4])

    with sidebar_col:
        st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
        st.markdown('<div class="filter-heading">Categories</div>', unsafe_allow_html=True)
        selected_cat = st.radio("Category", plant_categories, index=plant_categories.index(active_cat) if active_cat in plant_categories else 0, label_visibility="collapsed")
        st.session_state.active_category = selected_cat if selected_cat != "All" else None

        st.markdown('<div class="filter-heading" style="margin-top:20px;">Price Range</div>', unsafe_allow_html=True)
        price_range = st.slider("Price", 100, 2500, (100, 2500), step=50, label_visibility="collapsed")

        st.markdown('<div class="filter-heading" style="margin-top:20px;">Care Level</div>', unsafe_allow_html=True)
        care_options = st.multiselect("Care Level", ["Very Easy", "Easy", "Moderate", "Expert"], label_visibility="collapsed")

        st.markdown('<div class="filter-heading" style="margin-top:20px;">Features</div>', unsafe_allow_html=True)
        air_purify = st.checkbox("Air Purifying")
        gifting = st.checkbox("Good for Gifting")

        st.markdown('</div>', unsafe_allow_html=True)

    with main_col:
        # Sort and filter
        sort_col, count_col = st.columns([2, 2])
        with sort_col:
            sort_by = st.selectbox("Sort by", ["Popular", "Price: Low to High", "Price: High to Low", "Newest", "Rating"], label_visibility="visible")
        
        # Filter products
        filtered = [p for p in PRODUCTS if p["category"] in [
            "Indoor Plants", "Outdoor Plants", "Air Purifying Plants",
            "Flowering Plants", "Succulents", "Bonsai Plants"
        ]]

        if selected_cat != "All":
            filtered = [p for p in filtered if p["category"] == selected_cat]
        filtered = [p for p in filtered if price_range[0] <= p["price"] <= price_range[1]]
        if care_options:
            filtered = [p for p in filtered if p.get("care_level") in care_options]
        if air_purify:
            filtered = [p for p in filtered if p.get("air_purifying")]
        if gifting:
            filtered = [p for p in filtered if "gifting" in p.get("tags", [])]

        # Sort
        if sort_by == "Price: Low to High":
            filtered.sort(key=lambda x: x["price"])
        elif sort_by == "Price: High to Low":
            filtered.sort(key=lambda x: x["price"], reverse=True)
        elif sort_by == "Rating":
            filtered.sort(key=lambda x: x["rating"], reverse=True)

        with count_col:
            st.markdown(f'<div style="padding-top:32px;color:var(--neutral-600);font-size:14px;">Showing {len(filtered)} results</div>', unsafe_allow_html=True)

        if not filtered:
            st.info("No plants match your selected filters. Try adjusting your criteria.")
        else:
            for i in range(0, len(filtered), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(filtered):
                        with col:
                            render_product_card(filtered[i + j], key_suffix=f"plants_{i}_{j}")
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEEDS PAGE
# ─────────────────────────────────────────────
def render_seeds_page():
    st.markdown("""
    <div class="page-header">
        <h1 class="page-header-title">Seeds Collection</h1>
        <div class="page-header-breadcrumb">Home / Seeds</div>
    </div>
    """, unsafe_allow_html=True)

    seed_categories = ["Fruit Seeds", "Vegetable Seeds", "Flower Seeds", "Microgreen Seeds", "Herb Seeds"]
    tabs = st.tabs(seed_categories)

    seed_products = [p for p in PRODUCTS if p["category"] in seed_categories]

    for tab, cat in zip(tabs, seed_categories):
        with tab:
            cat_prods = [p for p in seed_products if p["category"] == cat]
            if cat_prods:
                cols = st.columns(min(len(cat_prods), 4))
                for col, product in zip(cols, cat_prods):
                    with col:
                        render_product_card(product, key_suffix=f"seed_{cat[:4]}")
            else:
                st.info(f"No {cat} listed currently. Check back soon!")

# ─────────────────────────────────────────────
# PLANT CARE PAGE
# ─────────────────────────────────────────────
def render_plant_care_page():
    st.markdown("""
    <div class="page-header">
        <h1 class="page-header-title">Plant Care</h1>
        <div class="page-header-breadcrumb">Home / Plant Care</div>
    </div>
    """, unsafe_allow_html=True)

    care_categories = ["Fertilizers", "Pots & Planters", "Gardening Tools",
                       "Watering Accessories", "Soil & Compost", "Pest Control", "Plant Medicines"]
    tabs = st.tabs(care_categories)
    care_products = [p for p in PRODUCTS if p["category"] in care_categories]

    for tab, cat in zip(tabs, care_categories):
        with tab:
            cat_prods = [p for p in care_products if p["category"] == cat]
            if cat_prods:
                cols = st.columns(min(len(cat_prods), 4))
                for col, product in zip(cols, cat_prods):
                    with col:
                        render_product_card(product, key_suffix=f"care_{cat[:4]}")
            else:
                st.info(f"More {cat} products coming soon!")

# ─────────────────────────────────────────────
# OFFERS PAGE
# ─────────────────────────────────────────────
def render_offers_page():
    st.markdown("""
    <div class="page-header" style="background:linear-gradient(135deg,#B71C1C,#E53935);">
        <h1 class="page-header-title">Exclusive Offers</h1>
        <div class="page-header-breadcrumb">Home / Offers — Limited time deals</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-label" style="color:#E53935;">Summer Sale 2025</div>
        <h2 class="section-title">Up to 40% Off</h2>
        <p class="section-subtitle">Handpicked deals on our most popular plants and care products.</p>
    </div>
    """, unsafe_allow_html=True)

    sale_products = sorted(PRODUCTS, key=lambda x: x["original_price"] - x["price"], reverse=True)[:8]
    for i in range(0, len(sale_products), 4):
        cols = st.columns(4)
        for j, col in enumerate(cols):
            if i + j < len(sale_products):
                with col:
                    render_product_card(sale_products[i + j], key_suffix=f"offers_{i}_{j}")
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ABOUT PAGE
# ─────────────────────────────────────────────
def render_about_page():
    st.markdown("""
    <div class="about-hero">
        <div style="max-width:700px;margin:0 auto;text-align:center;">
            <div class="section-label" style="text-align:center;">Our Story</div>
            <h1 style="font-family:'Playfair Display',serif;font-size:48px;font-weight:700;color:var(--green-dark);margin:12px 0 20px;">
                Growing More Than Plants
            </h1>
            <p style="font-size:17px;color:var(--neutral-600);line-height:1.8;">
                Founded in 2019 by passionate botanists and designers, Verdant was born from a simple belief:
                every home deserves the healing presence of nature. We work directly with certified nurseries
                across India to bring you the healthiest, most beautiful plants — delivered with the care they deserve.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header" style="text-align:center;">
        <div class="section-label">Our Values</div>
        <h2 class="section-title">What Drives Us</h2>
    </div>
    """, unsafe_allow_html=True)

    values = [
        {"icon": "&#127807;", "title": "Sustainable Sourcing", "desc": "All plants are ethically sourced from certified nurseries with sustainable practices."},
        {"icon": "&#128226;", "title": "Expert Guidance", "desc": "Every product ships with botanist-written care guides to ensure your plants thrive."},
        {"icon": "&#127758;", "title": "Eco Packaging", "desc": "100% biodegradable, plastic-free packaging that protects your plants and the planet."},
        {"icon": "&#128137;", "title": "30-Day Guarantee", "desc": "If your plant does not survive within 30 days, we replace it — no questions asked."},
    ]
    cols = st.columns(4)
    for col, v in zip(cols, values):
        with col:
            st.markdown(f"""
            <div class="about-value-card">
                <div class="about-value-icon">{v['icon']}</div>
                <div class="about-value-title">{v['title']}</div>
                <p style="font-size:13px;color:var(--neutral-600);line-height:1.6;">{v['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:var(--green-xlight);padding:60px;text-align:center;">
        <div class="section-label">Our Impact</div>
        <h2 class="section-title" style="margin-bottom:40px;">Numbers That Matter</h2>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    stats = [
        ("50,000+", "Happy Customers"),
        ("500+", "Plant Varieties"),
        ("25+", "Nursery Partners"),
        ("4.9 / 5", "Average Rating"),
    ]
    for col, (num, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:20px 0;">
                <div style="font-family:'Playfair Display',serif;font-size:40px;font-weight:700;color:var(--green-main);">{num}</div>
                <div style="font-size:14px;color:var(--neutral-600);text-transform:uppercase;letter-spacing:1px;margin-top:6px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONTACT PAGE
# ─────────────────────────────────────────────
def render_contact_page():
    st.markdown("""
    <div class="page-header">
        <h1 class="page-header-title">Get in Touch</h1>
        <div class="page-header-breadcrumb">Home / Contact Us</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

    info_cols = st.columns(3)
    contact_info = [
        {"icon": "&#128205;", "title": "Visit Us", "line1": "12, Green Valley Complex", "line2": "Ahmedabad, Gujarat 380015"},
        {"icon": "&#128222;", "title": "Call Us", "line1": "+91 98765 43210", "line2": "Mon – Sat, 9 AM – 6 PM"},
        {"icon": "&#9993;", "title": "Email Us", "line1": "care@verdantplants.in", "line2": "We reply within 24 hours"},
    ]
    for col, info in zip(info_cols, contact_info):
        with col:
            st.markdown(f"""
            <div class="contact-info-card">
                <div style="font-size:32px;color:var(--green-main);margin-bottom:12px;">{info['icon']}</div>
                <div style="font-weight:700;font-size:16px;margin-bottom:8px;">{info['title']}</div>
                <div style="font-size:14px;color:var(--neutral-600);">{info['line1']}</div>
                <div style="font-size:14px;color:var(--neutral-600);">{info['line2']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    form_col, faq_col = st.columns([1, 1])
    with form_col:
        st.markdown("""
        <div style="background:white;border-radius:var(--radius-md);padding:32px;border:1px solid var(--neutral-200);">
            <h3 style="font-family:'Playfair Display',serif;font-size:24px;margin-bottom:24px;">Send Us a Message</h3>
        </div>
        """, unsafe_allow_html=True)
        name = st.text_input("Your Name", placeholder="Priya Sharma")
        email = st.text_input("Email Address", placeholder="priya@example.com")
        subject = st.selectbox("Subject", ["Order Enquiry", "Plant Care Help", "Returns & Refunds", "Wholesale / Bulk Orders", "Other"])
        message = st.text_area("Message", placeholder="Tell us how we can help you...", height=140)
        if st.button("Send Message", type="primary", use_container_width=True):
            if name and email and message:
                st.success("Thank you! We have received your message and will respond within 24 hours.")
            else:
                st.warning("Please fill in all required fields.")

    with faq_col:
        st.markdown('<h3 style="font-family:\'Playfair Display\',serif;font-size:24px;margin-bottom:24px;">Frequently Asked Questions</h3>', unsafe_allow_html=True)
        faqs = [
            ("How long does delivery take?", "Most orders are delivered within 3–5 business days. Express delivery is available for select cities within 1–2 days."),
            ("Do you offer a plant health guarantee?", "Yes! If your plant does not survive within 30 days of delivery due to transit damage or quality issues, we will replace it for free."),
            ("How are plants packaged?", "Plants are secured in custom-fit boxes with coconut coir padding. All packaging is 100% biodegradable and plastic-free."),
            ("Can I return a plant?", "Due to the perishable nature of plants, we do not accept returns. However, our 30-day health guarantee covers all quality issues."),
            ("Do you deliver all over India?", "We deliver to 400+ cities across India. Enter your PIN code at checkout to verify availability."),
        ]
        for q, a in faqs:
            with st.expander(q):
                st.markdown(f'<p style="font-size:14px;color:var(--neutral-600);line-height:1.6;">{a}</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CART PAGE
# ─────────────────────────────────────────────
def render_cart_page():
    st.markdown("""
    <div class="page-header">
        <h1 class="page-header-title">Shopping Cart</h1>
        <div class="page-header-breadcrumb">Home / Cart</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.checkout_done:
        st.markdown("""
        <div style="text-align:center;padding:80px 60px;">
            <div style="font-size:64px;margin-bottom:20px;color:var(--green-main);">&#10003;</div>
            <h2 style="font-family:'Playfair Display',serif;font-size:36px;color:var(--green-dark);margin-bottom:12px;">Order Placed Successfully!</h2>
            <p style="font-size:16px;color:var(--neutral-600);margin-bottom:32px;">
                Thank you for shopping with Verdant. Your plants are being carefully prepared for dispatch.<br>
                Expected delivery: 3–5 business days. Order confirmation sent to your email.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue Shopping", type="primary", use_container_width=True):
                st.session_state.checkout_done = False
                st.session_state.cart = {}
                st.session_state.page = "Home"
                st.rerun()
        return

    st.markdown('<div style="padding:40px 60px;">', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.markdown("""
        <div style="text-align:center;padding:80px 0;">
            <div style="font-size:64px;margin-bottom:20px;color:var(--neutral-200);">&#128722;</div>
            <h3 style="font-family:'Playfair Display',serif;font-size:28px;color:var(--neutral-600);">Your cart is empty</h3>
            <p style="color:var(--neutral-600);margin-bottom:24px;">Discover our beautiful plant collection and bring nature home.</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Browse Plants", type="primary", use_container_width=True):
                st.session_state.page = "Plants"
                st.rerun()
    else:
        cart_col, summary_col = st.columns([3, 1])

        with cart_col:
            st.markdown(f'<h3 style="font-size:20px;font-weight:700;margin-bottom:20px;">{get_cart_count()} Items in your cart</h3>', unsafe_allow_html=True)
            for pid, qty in list(st.session_state.cart.items()):
                product = get_product_by_id(pid)
                if not product:
                    continue
                item_col1, item_col2, item_col3, item_col4 = st.columns([1, 3, 2, 1])
                with item_col1:
                    st.image(product["image"], width=80)
                with item_col2:
                    st.markdown(f"""
                    <div style="padding-top:8px;">
                        <div style="font-weight:600;font-size:15px;">{product['name']}</div>
                        <div style="font-size:12px;color:var(--neutral-600);">{product['category']}</div>
                        <div style="font-size:15px;font-weight:700;color:var(--green-main);margin-top:4px;">&#8377;{product['price']:,} per unit</div>
                    </div>
                    """, unsafe_allow_html=True)
                with item_col3:
                    col_minus, col_qty, col_plus = st.columns(3)
                    with col_minus:
                        if st.button("-", key=f"minus_{pid}"):
                            if st.session_state.cart[pid] > 1:
                                st.session_state.cart[pid] -= 1
                            else:
                                remove_from_cart(pid)
                            st.rerun()
                    with col_qty:
                        st.markdown(f'<div style="text-align:center;font-weight:700;font-size:16px;padding-top:8px;">{qty}</div>', unsafe_allow_html=True)
                    with col_plus:
                        if st.button("+", key=f"plus_{pid}"):
                            st.session_state.cart[pid] += 1
                            st.rerun()
                with item_col4:
                    st.markdown(f'<div style="font-weight:700;font-size:16px;text-align:right;padding-top:8px;">&#8377;{product["price"] * qty:,}</div>', unsafe_allow_html=True)
                    if st.button("Remove", key=f"remove_{pid}"):
                        remove_from_cart(pid)
                        st.rerun()
                st.divider()

            if st.button("Continue Shopping", key="continue_shopping"):
                st.session_state.page = "Plants"
                st.rerun()

        with summary_col:
            subtotal = get_cart_total()
            shipping = 0 if subtotal >= 999 else 99
            discount_amt = int(subtotal * 0.05)
            total = subtotal + shipping - discount_amt

            st.markdown(f"""
            <div class="order-summary">
                <h3 style="font-family:'Playfair Display',serif;font-size:20px;margin-bottom:20px;">Order Summary</h3>
                <div class="order-row">
                    <span>Subtotal ({get_cart_count()} items)</span>
                    <span>&#8377;{subtotal:,}</span>
                </div>
                <div class="order-row">
                    <span>Shipping</span>
                    <span style="color:var(--green-main);">{"Free" if shipping == 0 else f"&#8377;{shipping}"}</span>
                </div>
                <div class="order-row">
                    <span>Member Discount (5%)</span>
                    <span style="color:#E53935;">-&#8377;{discount_amt:,}</span>
                </div>
                <div class="order-total">
                    <span>Total</span>
                    <span>&#8377;{total:,}</span>
                </div>
                <p style="font-size:11px;color:var(--neutral-600);margin-top:12px;">Inclusive of all taxes. Free shipping on orders above &#8377;999.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            promo = st.text_input("Promo Code", placeholder="Enter promo code")
            if st.button("Apply Code", use_container_width=True):
                if promo.upper() == "VERDANT10":
                    st.success("Code applied! Additional 10% off.")
                else:
                    st.error("Invalid promo code.")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Proceed to Checkout", type="primary", use_container_width=True, key="checkout_btn"):
                st.session_state.checkout_done = True
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEARCH PAGE
# ─────────────────────────────────────────────
def render_search_page():
    query = st.session_state.search_query
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-header-title">Search Results</h1>
        <div class="page-header-breadcrumb">Showing results for: "{query}"</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

    results = [p for p in PRODUCTS if query.lower() in p["name"].lower() or
               query.lower() in p["category"].lower() or
               query.lower() in p["description"].lower()]

    st.markdown(f'<div class="search-result-info">Found {len(results)} result(s) for "{query}"</div>', unsafe_allow_html=True)

    if not results:
        st.info("No products found. Try a different search term.")
    else:
        for i in range(0, len(results), 4):
            cols = st.columns(4)
            for j, col in enumerate(cols):
                if i + j < len(results):
                    with col:
                        render_product_card(results[i + j], key_suffix=f"search_{i}_{j}")
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
def render_footer():
    st.markdown("""
    <div class="footer">
        <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:48px;max-width:1200px;">
            <div>
                <div class="footer-brand">Verdant.</div>
                <div class="footer-brand-desc">Bringing premium, ethically sourced plants to homes across India since 2019. Every purchase supports sustainable nurseries.</div>
                <div style="display:flex;gap:16px;margin-top:8px;">
                    <span style="font-size:20px;cursor:pointer;">&#128241;</span>
                    <span style="font-size:20px;cursor:pointer;">&#128247;</span>
                    <span style="font-size:20px;cursor:pointer;">&#128241;</span>
                    <span style="font-size:20px;cursor:pointer;">&#127916;</span>
                </div>
            </div>
            <div>
                <div class="footer-heading">Shop</div>
                <span class="footer-link">Indoor Plants</span>
                <span class="footer-link">Outdoor Plants</span>
                <span class="footer-link">Seeds</span>
                <span class="footer-link">Plant Care</span>
                <span class="footer-link">Offers</span>
            </div>
            <div>
                <div class="footer-heading">Support</div>
                <span class="footer-link">Track Order</span>
                <span class="footer-link">Returns Policy</span>
                <span class="footer-link">Plant Guarantee</span>
                <span class="footer-link">Care Guides</span>
                <span class="footer-link">FAQs</span>
            </div>
            <div>
                <div class="footer-heading">Company</div>
                <span class="footer-link">About Us</span>
                <span class="footer-link">Careers</span>
                <span class="footer-link">Press</span>
                <span class="footer-link">Privacy Policy</span>
                <span class="footer-link">Terms of Service</span>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&#169; 2025 Verdant Plant Boutique. All rights reserved.</span>
            <span>Crafted with care in India</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHATBOT — PLANTPULSE DOCTOR
# ─────────────────────────────────────────────
def render_chatbot():
    """Chatbot panel in the sidebar — opened via legacy sidebar toggle."""

    with st.sidebar:
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            display: block !important;
            width: 400px !important;
            right: 0 !important;
            left: auto !important;
            background: #ffffff !important;
            border-left: 1px solid #E8E8E0 !important;
            box-shadow: -4px 0 32px rgba(0,0,0,0.12) !important;
            padding: 0 !important;
        }
        section[data-testid="stSidebar"] > div {
            padding: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.session_state.chatbot_open:
            # ── Header ──
            st.markdown("""
            <div style="
                background:linear-gradient(135deg,#1B5E20,#2E7D32);
                padding:20px;color:white;
            ">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-family:'Playfair Display',serif;font-size:18px;font-weight:700;">PlantPulse Doctor</div>
                        <div style="font-size:11px;opacity:0.8;margin-top:2px;">AI Plant Care Assistant</div>
                    </div>
                    <div style="
                        width:10px;height:10px;border-radius:50%;
                        background:#69F0AE;box-shadow:0 0 6px #69F0AE;
                    "></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.chatbot_mode is None:
                # Mode selection
                st.markdown("""
                <div style="padding:20px;">
                    <p style="font-size:14px;color:#6B6B6B;margin-bottom:20px;line-height:1.6;">
                        Welcome! How can I help you today? Choose a service below.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Plant Diagnosis\nDoctor", key="bot_mode_diag", use_container_width=True):
                        st.session_state.chatbot_mode = "diagnosis"
                        st.session_state.chatbot_diagnosis_done = False
                        st.rerun()
                with col2:
                    if st.button("Plant Suggestions\nExpert", key="bot_mode_sug", use_container_width=True):
                        st.session_state.chatbot_mode = "suggestions"
                        st.session_state.chatbot_suggestions_done = False
                        st.session_state.suggestion_answers = {}
                        st.rerun()

                st.markdown("""
                <div style="padding:16px 20px 20px;">
                    <div style="background:#F1F8F1;border-radius:12px;padding:14px;border:1px solid #C8E6C9;">
                        <div style="font-size:12px;color:#2E7D32;font-weight:600;margin-bottom:4px;">Plant Diagnosis Doctor</div>
                        <div style="font-size:12px;color:#6B6B6B;">Upload a plant photo for AI-powered health assessment and treatment recommendations.</div>
                    </div>
                    <div style="background:#F1F8F1;border-radius:12px;padding:14px;border:1px solid #C8E6C9;margin-top:10px;">
                        <div style="font-size:12px;color:#2E7D32;font-weight:600;margin-bottom:4px;">Plant Suggestions Expert</div>
                        <div style="font-size:12px;color:#6B6B6B;">Answer a few questions to get personalized plant recommendations for your space.</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif st.session_state.chatbot_mode == "diagnosis":
                render_diagnosis_bot()

            elif st.session_state.chatbot_mode == "suggestions":
                render_suggestions_bot()

            # Close button
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("Close Assistant", key="close_chatbot", use_container_width=True):
                st.session_state.chatbot_open = False
                st.session_state.chatbot_mode = None
                st.rerun()

# ─────────────────────────────────────────────
# DIAGNOSIS BOT
# ─────────────────────────────────────────────
def render_diagnosis_bot():
    st.markdown("""
    <div style="padding:16px 16px 0;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
            <div style="font-size:14px;font-weight:700;color:#1B5E20;">Plant Diagnosis Doctor</div>
        </div>
        <p style="font-size:13px;color:#6B6B6B;line-height:1.6;">
            Upload a clear photo of your plant and I will analyze its health, identify issues, and recommend treatments.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Back to Menu", key="diag_back"):
        st.session_state.chatbot_mode = None
        st.session_state.chatbot_diagnosis_done = False
        st.rerun()

    uploaded = st.file_uploader("Upload plant photo", type=["jpg", "jpeg", "png", "webp"],
                                 label_visibility="collapsed",
                                 key="diagnosis_upload")

    if uploaded and not st.session_state.chatbot_diagnosis_done:
        st.image(uploaded, caption="Uploaded Plant", use_container_width=True)
        if st.button("Analyze Plant Health", key="run_diagnosis", type="primary", use_container_width=True):
            with st.spinner("Analyzing leaf patterns and health indicators..."):
                time.sleep(2)
            st.session_state.chatbot_diagnosis_done = True
            st.rerun()

    if st.session_state.chatbot_diagnosis_done:
        # Simulated diagnosis
        diagnoses = [
            {
                "condition": "Early Stage Yellowing",
                "severity": "Moderate",
                "cause": "Likely overwatering combined with poor drainage. The yellowing pattern starting from lower leaves is characteristic of root saturation.",
                "care": "Reduce watering frequency to once every 10–14 days. Ensure pot has drainage holes. Allow top 2 inches of soil to dry before next watering.",
                "treatment": "Remove yellow leaves at the base. Apply a balanced NPK fertilizer at half strength after the soil dries out.",
            },
            {
                "condition": "Nutrient Deficiency",
                "severity": "Mild",
                "cause": "Pale green to yellow coloration between leaf veins indicates iron or magnesium deficiency. Often caused by pH imbalance in soil.",
                "care": "Repot with fresh potting mix. Add slow-release fertilizer with micronutrients.",
                "treatment": "Apply chelated iron spray directly to leaves. Test and adjust soil pH to 6.0–6.5 range.",
            },
            {
                "condition": "Pest Infestation (Spider Mites)",
                "severity": "Early",
                "cause": "Fine webbing on leaf undersides and tiny moving dots indicate spider mite presence. Common in dry indoor environments.",
                "care": "Isolate the plant immediately. Increase humidity around the plant. Rinse leaves with water.",
                "treatment": "Apply neem oil spray every 5–7 days for 3 weeks. Keep humidity above 60%.",
            },
        ]
        diagnosis = random.choice(diagnoses)

        severity_color = {"Mild": "#F57F17", "Moderate": "#E65100", "Early": "#2E7D32"}
        color = severity_color.get(diagnosis["severity"], "#2E7D32")

        st.markdown(f"""
        <div style="background:#F1F8F1;border-radius:12px;padding:16px;border:1px solid #C8E6C9;margin:12px 0;">
            <div style="font-weight:700;font-size:15px;color:#1B5E20;margin-bottom:4px;">Diagnosis Result</div>
            <div style="font-size:16px;font-weight:700;color:#2A2A2A;">{diagnosis['condition']}</div>
            <span style="background:{color};color:white;font-size:11px;font-weight:600;padding:2px 8px;border-radius:4px;margin-top:4px;display:inline-block;">
                {diagnosis['severity']} Severity
            </span>
            <div style="margin-top:12px;font-size:13px;color:#6B6B6B;line-height:1.6;"><strong>Cause:</strong> {diagnosis['cause']}</div>
            <div style="margin-top:8px;font-size:13px;color:#6B6B6B;line-height:1.6;"><strong>Care:</strong> {diagnosis['care']}</div>
            <div style="margin-top:8px;font-size:13px;color:#6B6B6B;line-height:1.6;"><strong>Treatment:</strong> {diagnosis['treatment']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-weight:700;font-size:14px;color:#1B5E20;margin:16px 0 8px;">Recommended Products</div>
        """, unsafe_allow_html=True)

        recommended_ids = [27, 30, 24, 26]  # Neem Oil, Seaweed Tonic, Fertilizer, Potting Mix
        recommended_products = [get_product_by_id(pid) for pid in recommended_ids if get_product_by_id(pid)]

        for product in recommended_products[:3]:
            discount = int((1 - product["price"] / product["original_price"]) * 100)
            rec_col1, rec_col2 = st.columns([1, 2])
            with rec_col1:
                st.image(product["image"], use_container_width=True)
            with rec_col2:
                st.markdown(f"""
                <div>
                    <div style="font-weight:600;font-size:13px;color:#2A2A2A;">{product['name']}</div>
                    <div style="font-size:12px;color:#6B6B6B;margin:2px 0;">{product['description'][:60]}...</div>
                    <div style="font-weight:700;color:#2E7D32;font-size:14px;">&#8377;{product['price']:,}</div>
                    <div style="font-size:11px;color:#E53935;">-{discount}% off</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Add to Cart", key=f"diag_cart_{product['id']}", use_container_width=True, type="primary"):
                    add_to_cart(product["id"])
                    st.success("Added!")
                    st.rerun()

        if st.button("New Diagnosis", key="new_diagnosis", use_container_width=True):
            st.session_state.chatbot_diagnosis_done = False
            st.rerun()

# ─────────────────────────────────────────────
# SUGGESTIONS BOT
# ─────────────────────────────────────────────
def render_suggestions_bot():
    st.markdown("""
    <div style="padding:16px 16px 0;">
        <div style="font-size:14px;font-weight:700;color:#1B5E20;margin-bottom:8px;">Plant Suggestions Expert</div>
        <p style="font-size:13px;color:#6B6B6B;line-height:1.6;">Answer a few quick questions and I will find the perfect plants for your space.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Back to Menu", key="sug_back"):
        st.session_state.chatbot_mode = None
        st.session_state.chatbot_suggestions_done = False
        st.session_state.suggestion_answers = {}
        st.rerun()

    if not st.session_state.chatbot_suggestions_done:
        with st.form("suggestion_form"):
            placement = st.radio("Where will you keep the plant?", ["Indoors", "Outdoors", "Both"], horizontal=True)
            sunlight = st.radio("Available sunlight?", ["Low Light", "Indirect Light", "Bright Light", "Full Sun"], horizontal=True)
            maintenance = st.radio("Preferred maintenance level?", ["Minimal (Water weekly)", "Moderate", "Enjoy regular care"], horizontal=True)
            purpose = st.multiselect("What is the plant for?", ["Home Decor", "Air Purification", "Gifting", "Fragrance", "Edible/Herb"])
            submitted = st.form_submit_button("Find My Plants", use_container_width=True)

        if submitted:
            st.session_state.suggestion_answers = {
                "placement": placement,
                "sunlight": sunlight,
                "maintenance": maintenance,
                "purpose": purpose,
            }
            st.session_state.chatbot_suggestions_done = True
            st.rerun()

    else:
        answers = st.session_state.suggestion_answers
        placement = answers.get("placement", "Indoors")
        sunlight = answers.get("sunlight", "Indirect Light")
        maintenance = answers.get("maintenance", "Minimal")
        purpose = answers.get("purpose", [])

        # Logic-based filtering
        candidates = []
        if placement in ["Indoors", "Both"]:
            candidates += [p for p in PRODUCTS if p["category"] in ["Indoor Plants", "Succulents", "Flowering Plants", "Bonsai Plants", "Air Purifying Plants"]]
        if placement in ["Outdoors", "Both"]:
            candidates += [p for p in PRODUCTS if p["category"] in ["Outdoor Plants", "Flowering Plants"]]

        if "Minimal" in maintenance:
            candidates = [p for p in candidates if p.get("care_level") in ["Very Easy", "Easy"]]
        elif "Moderate" in maintenance:
            candidates = [p for p in candidates if p.get("care_level") in ["Easy", "Moderate"]]

        if "Air Purification" in purpose:
            candidates = [p for p in candidates if p.get("air_purifying")]
        if "Gifting" in purpose:
            candidates = [p for p in candidates if "gifting" in p.get("tags", [])]

        # Remove duplicates
        seen = set()
        unique = []
        for p in candidates:
            if p["id"] not in seen:
                seen.add(p["id"])
                unique.append(p)

        if not unique:
            unique = PRODUCTS[:4]

        recommendations = unique[:4]

        st.markdown(f"""
        <div style="background:#F1F8F1;border-radius:12px;padding:14px;border:1px solid #C8E6C9;margin:12px 0;">
            <div style="font-size:13px;color:#1B5E20;font-weight:600;">Based on your preferences</div>
            <div style="font-size:12px;color:#6B6B6B;margin-top:4px;">
                {placement} • {sunlight} • {maintenance}
                {" • " + ", ".join(purpose) if purpose else ""}
            </div>
        </div>
        <div style="font-weight:700;font-size:14px;color:#1B5E20;margin-bottom:10px;">Perfect Plants For You</div>
        """, unsafe_allow_html=True)

        for product in recommendations:
            discount = int((1 - product["price"] / product["original_price"]) * 100)
            rec_col1, rec_col2 = st.columns([1, 2])
            with rec_col1:
                st.image(product["image"], use_container_width=True)
            with rec_col2:
                st.markdown(f"""
                <div>
                    <div style="font-weight:600;font-size:13px;color:#2A2A2A;">{product['name']}</div>
                    <div style="font-size:11px;color:#2E7D32;background:#F1F8F1;border-radius:4px;padding:2px 6px;display:inline-block;margin:3px 0;">
                        Care: {product.get('care_level','N/A')}
                    </div>
                    <div style="font-size:12px;color:#6B6B6B;margin:3px 0;">{product['description'][:55]}...</div>
                    <div style="font-weight:700;color:#2E7D32;font-size:14px;">&#8377;{product['price']:,}
                        <span style="font-size:11px;color:#E53935;margin-left:4px;">-{discount}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Add to Cart", key=f"sug_cart_{product['id']}", use_container_width=True, type="primary"):
                    add_to_cart(product["id"])
                    st.success("Added!")
                    st.rerun()
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("Start Over", key="restart_suggestions", use_container_width=True):
            st.session_state.chatbot_suggestions_done = False
            st.session_state.suggestion_answers = {}
            st.rerun()

# ─────────────────────────────────────────────
# PLANTPAL AI CHATBOT PAGE  (v2 — clean flow)
# ─────────────────────────────────────────────

# ── Session keys used exclusively by PlantPal ──
_PP_KEYS = [
    "pp_step",          # current step name (string)
    "pp_flow",          # "suggestions" | "doctor"
    "pp_answers",       # dict of collected answers
    "pp_result",        # AI / logic result dict
    "pp_upload_key",    # int counter — forces file_uploader reset
    "pp_suggested",     # list of recommended product ids
]

def _pp_init():
    """Initialise PlantPal session keys if missing."""
    defaults = {
        "pp_step": "greeting",
        "pp_flow": None,
        "pp_answers": {},
        "pp_result": None,
        "pp_upload_key": 0,
        "pp_suggested": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _pp_reset():
    st.session_state.pp_step = "greeting"
    st.session_state.pp_flow = None
    st.session_state.pp_answers = {}
    st.session_state.pp_result = None
    st.session_state.pp_suggested = []
    st.session_state.pp_upload_key += 1
    st.rerun()


def _call_claude(system_prompt: str, user_content: list) -> str:
    """Call Claude API and return text response. Returns error string on failure."""
    import json, urllib.request, urllib.error
    payload = json.dumps({
        "model": "claude-opus-4-5",
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_content}],
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={"Content-Type": "application/json", "anthropic-version": "2023-06-01"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"__ERROR__:HTTP {e.code}"
    except Exception as e:
        return f"__ERROR__:{str(e)[:120]}"


def _bot_bubble(text: str):
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:10px;margin:12px 0 4px;">
        <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#1B5E20,#43A047);
                    display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">🌿</div>
        <div style="background:#F1F8F1;border:1px solid #C8E6C9;border-radius:0 16px 16px 16px;
                    padding:12px 16px;max-width:85%;font-size:14px;line-height:1.6;color:#1a1a1a;">
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)


def _user_bubble(text: str):
    st.markdown(f"""
    <div style="display:flex;justify-content:flex-end;margin:4px 0 12px;">
        <div style="background:#2E7D32;color:white;border-radius:16px 0 16px 16px;
                    padding:12px 16px;max-width:75%;font-size:14px;line-height:1.6;">
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)


def _choice_buttons(options: list, key_prefix: str):
    """Render pill-style choice buttons. Returns chosen label or None."""
    cols = st.columns(len(options))
    for i, (col, label) in enumerate(zip(cols, options)):
        with col:
            if st.button(label, key=f"{key_prefix}_{i}", use_container_width=True):
                return label
    return None


def _product_card(product):
    """Render a compact product card with Add to Cart."""
    discount = int((1 - product["price"] / product["original_price"]) * 100)
    st.markdown(f"""
    <div style="background:white;border-radius:12px;border:1px solid #D7EDD7;
                padding:12px;margin-bottom:10px;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
        <div style="display:flex;gap:12px;align-items:flex-start;">
            <img src="{product['image']}" style="width:72px;height:72px;border-radius:8px;
                 object-fit:cover;flex-shrink:0;" />
            <div style="flex:1;min-width:0;">
                <div style="font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:2px;">{product['name']}</div>
                <div style="font-size:12px;color:#6B6B6B;line-height:1.4;margin-bottom:6px;">{product['description'][:70]}…</div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <span style="font-size:14px;font-weight:700;color:#2E7D32;">₹{product['price']:,}</span>
                    <span style="font-size:11px;color:#E53935;background:#FFF0F0;
                          padding:1px 6px;border-radius:4px;font-weight:600;">−{discount}%</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"Add to Cart", key=f"pp_add_{product['id']}", use_container_width=True, type="primary"):
        add_to_cart(product["id"])
        st.success(f"'{product['name']}' added to cart!")
        st.rerun()


def render_plantpal_page():
    import base64

    _pp_init()

    # ── Page chrome ──
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 60%,#43A047 100%);
                padding:40px 60px 32px;color:white;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-80px;right:-80px;width:320px;height:320px;
                    border-radius:50%;background:rgba(255,255,255,0.04);"></div>
        <div style="position:relative;z-index:2;">
            <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.15);
                        border:1px solid rgba(255,255,255,0.25);border-radius:20px;
                        padding:4px 14px;font-size:11px;font-weight:600;letter-spacing:2px;
                        text-transform:uppercase;margin-bottom:14px;">
                <span>🌿</span><span>AI-Powered</span>
            </div>
            <h1 style="font-family:'Playfair Display',serif;font-size:38px;font-weight:700;
                       margin:0 0 8px;line-height:1.2;">PlantPal Chatbot</h1>
            <p style="font-size:15px;opacity:0.80;max-width:500px;line-height:1.6;margin:0;">
                Get personalised plant suggestions or diagnose your plant with AI.
            </p>
        </div>
    </div>
    <div style="height:24px;"></div>
    """, unsafe_allow_html=True)

    # ── Two-column layout ──
    chat_col, side_col = st.columns([3, 2], gap="large")

    with chat_col:
        # Header bar
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1B5E20,#2E7D32);border-radius:14px 14px 0 0;
                    padding:14px 20px;display:flex;align-items:center;gap:12px;">
            <div style="width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,0.18);
                        display:flex;align-items:center;justify-content:center;font-size:17px;">🌿</div>
            <div>
                <div style="font-family:'Playfair Display',serif;font-size:15px;font-weight:700;color:white;">PlantPal</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.70);">AI Plant Assistant · Online</div>
            </div>
            <div style="margin-left:auto;width:9px;height:9px;border-radius:50%;
                        background:#69F0AE;box-shadow:0 0 6px #69F0AE;"></div>
        </div>
        <div style="background:white;border:1px solid #D7EDD7;border-top:none;
                    border-radius:0 0 14px 14px;padding:20px 20px 16px;min-height:340px;">
        """, unsafe_allow_html=True)

        step = st.session_state.pp_step

        # ── STEP: greeting ──────────────────────────────────────────────────
        if step == "greeting":
            _bot_bubble("Hi! I'm <strong>PlantPal</strong> 🌱<br>How can I help you today?")
            chosen = _choice_buttons(
                ["🪴 Get Plant Suggestions", "🔬 PlantPal Doctor"],
                key_prefix="pp_greeting"
            )
            if chosen == "🪴 Get Plant Suggestions":
                st.session_state.pp_flow = "suggestions"
                st.session_state.pp_step = "ask_location"
                st.rerun()
            elif chosen == "🔬 PlantPal Doctor":
                st.session_state.pp_flow = "doctor"
                st.session_state.pp_step = "doctor_prompt"
                st.rerun()

        # ── FLOW: SUGGESTIONS ───────────────────────────────────────────────
        elif step == "ask_location":
            _user_bubble("🪴 Get Plant Suggestions")
            _bot_bubble("Great! Where will you keep the plant?")
            chosen = _choice_buttons(["Indoor", "Outdoor", "Gifting"], key_prefix="pp_loc")
            if chosen:
                st.session_state.pp_answers["location"] = chosen
                st.session_state.pp_step = "ask_sunlight"
                st.rerun()

        elif step == "ask_sunlight":
            loc = st.session_state.pp_answers.get("location", "Indoor")
            _user_bubble("🪴 Get Plant Suggestions")
            _bot_bubble(f"<strong>{loc}</strong> — good choice! How much sunlight is available?")
            chosen = _choice_buttons(["Low Light", "Medium Light", "Bright Light"], key_prefix="pp_sun")
            if chosen:
                st.session_state.pp_answers["sunlight"] = chosen
                st.session_state.pp_step = "ask_maintenance"
                st.rerun()

        elif step == "ask_maintenance":
            _user_bubble(st.session_state.pp_answers.get("sunlight", ""))
            _bot_bubble("How much time can you give to plant care?")
            chosen = _choice_buttons(["Low maintenance", "Medium", "Enjoy regular care"], key_prefix="pp_maint")
            if chosen:
                st.session_state.pp_answers["maintenance"] = chosen
                st.session_state.pp_step = "show_suggestions"
                st.rerun()

        elif step == "show_suggestions":
            ans = st.session_state.pp_answers
            loc      = ans.get("location", "Indoor")
            sunlight = ans.get("sunlight", "Medium Light")
            maint    = ans.get("maintenance", "Low maintenance")

            _user_bubble(maint)
            _bot_bubble(f"Here are some plants perfect for <strong>{loc.lower()}</strong> spaces with <strong>{sunlight.lower()}</strong> and <strong>{maint.lower()}</strong> care:")

            # Filter logic
            candidates = []
            if loc == "Indoor" or loc == "Gifting":
                cats = ["Indoor Plants", "Succulents", "Flowering Plants", "Bonsai Plants", "Air Purifying Plants"]
                candidates = [p for p in PRODUCTS if p["category"] in cats]
            else:
                candidates = [p for p in PRODUCTS if p["category"] in ["Outdoor Plants", "Flowering Plants"]]

            if "Low" in maint:
                candidates = [p for p in candidates if p.get("care_level") in ["Very Easy", "Easy"]]
            elif "Medium" in maint:
                candidates = [p for p in candidates if p.get("care_level") in ["Easy", "Moderate"]]

            if loc == "Gifting":
                gifting = [p for p in candidates if "gifting" in p.get("tags", [])]
                if gifting:
                    candidates = gifting

            seen, unique = set(), []
            for p in candidates:
                if p["id"] not in seen:
                    seen.add(p["id"])
                    unique.append(p)

            if not unique:
                unique = [p for p in PRODUCTS if p["category"] == "Indoor Plants"][:4]

            recs = unique[:4]
            st.session_state.pp_suggested = [p["id"] for p in recs]

            for product in recs:
                _product_card(product)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Start over", key="pp_restart_sug", use_container_width=False):
                _pp_reset()

        # ── FLOW: DOCTOR ────────────────────────────────────────────────────
        elif step == "doctor_prompt":
            _user_bubble("🔬 PlantPal Doctor")
            _bot_bubble("Please upload a clear image of your plant 🌿<br><small style='color:#6B6B6B;'>I'll analyse its condition and recommend treatments.</small>")

            uploaded = st.file_uploader(
                "Upload plant image",
                type=["jpg", "jpeg", "png", "webp"],
                key=f"pp_doctor_upload_{st.session_state.pp_upload_key}",
                label_visibility="collapsed",
            )

            if uploaded:
                st.image(uploaded, caption="Uploaded image", use_container_width=True)
                if st.button("Analyse my plant 🔍", key="pp_analyse_btn", type="primary", use_container_width=True):
                    # Build base64 payload
                    img_bytes = uploaded.read()
                    b64 = base64.b64encode(img_bytes).decode("utf-8")
                    ext = uploaded.name.rsplit(".", 1)[-1].lower()
                    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"

                    product_list = "\n".join([
                        f"- {p['name']} (₹{p['price']}) [{p['category']}]: {p['description'][:70]}"
                        for p in PRODUCTS
                        if p["category"] in ["Fertilizers", "Pest Control", "Plant Medicines",
                                             "Soil & Compost", "Pots & Planters", "Watering Accessories"]
                    ])

                    system_prompt = f"""You are PlantPal, an expert AI plant care assistant for Verdant Premium Plant Boutique (India).

Your task:
1. First, determine if the uploaded image contains a plant. If it does NOT contain a plant, reply with exactly: NOT_A_PLANT
2. If it IS a plant, analyse its health and respond in this exact JSON format (no markdown, no code blocks, just raw JSON):
{{
  "plant_name": "...",
  "condition": "...",
  "severity": "Mild|Moderate|Severe",
  "diagnosis": "...",
  "causes": "...",
  "treatment": "...",
  "care_tip": "...",
  "recommended_products": ["exact product name 1", "exact product name 2"],
  "schedule": "Mon & Thu: ... | Sat: ..."
}}

Only recommend products from this list:
{product_list}

Be concise. Keep each field under 2 sentences."""

                    content = [
                        {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}},
                        {"type": "text", "text": "Please analyse this plant image."}
                    ]

                    with st.spinner("Analysing your plant…"):
                        raw = _call_claude(system_prompt, content)

                    if raw.startswith("__ERROR__"):
                        st.session_state.pp_result = {"error": raw.replace("__ERROR__:", "")}
                    elif raw.strip() == "NOT_A_PLANT":
                        st.session_state.pp_result = {"not_plant": True}
                    else:
                        import json as _json
                        try:
                            # Strip any accidental markdown code fences
                            clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
                            data = _json.loads(clean)
                            st.session_state.pp_result = data
                            # Match recommended products to our DB
                            matched = []
                            for p in PRODUCTS:
                                for rec_name in data.get("recommended_products", []):
                                    if rec_name.lower() in p["name"].lower() or p["name"].lower() in rec_name.lower():
                                        matched.append(p["id"])
                            st.session_state.pp_suggested = matched[:3]
                        except Exception:
                            # If JSON parse fails, store raw text
                            st.session_state.pp_result = {"raw": raw}

                    st.session_state.pp_step = "doctor_result"
                    st.rerun()

        elif step == "doctor_result":
            result = st.session_state.pp_result or {}

            if result.get("not_plant"):
                _user_bubble("📷 [Image uploaded]")
                _bot_bubble("This doesn't seem to be a plant image. Please upload a clear photo of a plant 🌱")
                if st.button("Try again", key="pp_retry_notplant", use_container_width=False):
                    st.session_state.pp_step = "doctor_prompt"
                    st.session_state.pp_result = None
                    st.session_state.pp_upload_key += 1
                    st.rerun()

            elif result.get("error"):
                _user_bubble("📷 [Image uploaded]")
                _bot_bubble("I had trouble analysing the image. This could be a network issue. Please try again.")
                if st.button("Retry", key="pp_retry_err", use_container_width=False):
                    st.session_state.pp_step = "doctor_prompt"
                    st.session_state.pp_result = None
                    st.session_state.pp_upload_key += 1
                    st.rerun()

            elif result.get("raw"):
                # Fallback: show raw AI text cleanly
                _user_bubble("📷 [Image uploaded]")
                clean_text = result["raw"].replace("\n", "<br>")
                _bot_bubble(clean_text)
                if st.button("Start over", key="pp_restart_raw", use_container_width=False):
                    _pp_reset()

            else:
                # Clean structured result
                severity_colors = {"Mild": "#F57F17", "Moderate": "#E65100", "Severe": "#C62828"}
                sev = result.get("severity", "Moderate")
                sev_color = severity_colors.get(sev, "#E65100")

                _user_bubble("📷 [Image uploaded]")
                _bot_bubble(f"""
                    <strong>Diagnosis: {result.get('condition', 'Issue detected')}</strong><br>
                    <span style="background:{sev_color};color:white;font-size:11px;font-weight:600;
                          padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;">
                        {sev} Severity
                    </span>
                """)

                _bot_bubble(f"<strong>Plant:</strong> {result.get('plant_name', 'Unknown')}<br>"
                            f"<strong>Cause:</strong> {result.get('causes', '—')}")

                _bot_bubble(f"<strong>Treatment:</strong> {result.get('treatment', '—')}")

                if result.get("schedule"):
                    _bot_bubble(f"<strong>Care Schedule:</strong><br>{result['schedule'].replace('|','<br>')}")

                if result.get("care_tip"):
                    _bot_bubble(f"💡 <em>{result['care_tip']}</em>")

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

                if st.button("Diagnose another plant", key="pp_new_diag", use_container_width=False):
                    st.session_state.pp_step = "doctor_prompt"
                    st.session_state.pp_result = None
                    st.session_state.pp_upload_key += 1
                    st.rerun()

                col_l, col_r = st.columns(2)
                with col_l:
                    if st.button("Start over", key="pp_restart_doc", use_container_width=True):
                        _pp_reset()

        # Close the chat window div
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Right column: recommended products ──────────────────────────────────
    with side_col:
        suggested_ids = st.session_state.pp_suggested
        step = st.session_state.pp_step

        if suggested_ids:
            st.markdown("""
            <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;
                        color:#1B5E20;margin-bottom:4px;">Recommended Products</div>
            <p style="font-size:13px;color:#6B6B6B;margin-bottom:16px;">From PlantPal's suggestions</p>
            """, unsafe_allow_html=True)
            for pid in suggested_ids:
                p = get_product_by_id(pid)
                if p:
                    _product_card(p)
        else:
            # Default care products shown before any interaction
            st.markdown("""
            <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;
                        color:#1B5E20;margin-bottom:4px;">Popular Care Products</div>
            <p style="font-size:13px;color:#6B6B6B;margin-bottom:4px;">PlantPal recommends based on your plant's needs</p>
            <div style="background:#F1F8F1;border-radius:10px;padding:12px 14px;
                        border:1px dashed #A5D6A7;margin-bottom:16px;">
                <div style="font-size:12px;color:#2E7D32;font-weight:600;">💡 How it works</div>
                <div style="font-size:12px;color:#6B6B6B;margin-top:3px;line-height:1.5;">
                    Chat with PlantPal and personalised product picks will appear here automatically.
                </div>
            </div>
            """, unsafe_allow_html=True)
            for pid in [24, 27, 26, 30]:
                p = get_product_by_id(pid)
                if p:
                    _product_card(p)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    render_footer()


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────
def main():
    inject_css()
    render_navbar()

    page = st.session_state.page

    if page == "Home":
        render_home()
    elif page == "Plants":
        render_plants_page()
        render_footer()
    elif page == "Seeds":
        render_seeds_page()
        render_footer()
    elif page == "Plant Care":
        render_plant_care_page()
        render_footer()
    elif page == "Offers":
        render_offers_page()
        render_footer()
    elif page == "About Us":
        render_about_page()
        render_footer()
    elif page == "Contact":
        render_contact_page()
        render_footer()
    elif page == "Cart":
        render_cart_page()
        render_footer()
    elif page == "Search":
        render_search_page()
        render_footer()
    elif page == "PlantPal":
        render_plantpal_page()

    # Legacy chatbot still available in sidebar if opened
    render_chatbot()


if __name__ == "__main__":
    main()
