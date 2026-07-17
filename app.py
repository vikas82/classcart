import os
import sqlite3
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Class Cart", page_icon="📚", layout="wide")

DB_PATH = Path(__file__).resolve().parent / "classcart.db"

PRODUCTS = [
    {"id": 1, "name": "Pen", "price": 10, "category": "stationery", "icon": "🖊️", "desc": "Smooth everyday writing pen."},
    {"id": 2, "name": "Pencil", "price": 10, "category": "stationery", "icon": "✏️", "desc": "Useful for classwork and drawing."},
    {"id": 3, "name": "Eraser", "price": 5, "category": "stationery", "icon": "⬜", "desc": "Clean and easy erasing."},
    {"id": 4, "name": "Sharpener", "price": 5, "category": "stationery", "icon": "🔺", "desc": "Compact school sharpener."},
    {"id": 5, "name": "Ruler", "price": 20, "category": "stationery", "icon": "📏", "desc": "Clear markings for neat work."},
    {"id": 6, "name": "Highlighter", "price": 45, "category": "stationery", "icon": "🖍️", "desc": "Highlight important notes."},
    {"id": 7, "name": "Bookmark", "price": 10, "category": "stationery", "icon": "🔖", "desc": "Mark your reading place."},
    {"id": 8, "name": "Simple Keychain", "price": 25, "category": "keychains", "icon": "🔑", "desc": "Simple and useful design."},
    {"id": 9, "name": "Cartoon Keychain", "price": 40, "category": "keychains", "icon": "🌟", "desc": "Fun cartoon bag accessory."},
    {"id": 10, "name": "Anime Keychain", "price": 120, "category": "keychains", "icon": "🎨", "desc": "Premium anime-themed keychain."},
    {"id": 11, "name": "Customised Keychain", "price": 125, "category": "keychains", "icon": "✨", "desc": "Personalised name or design."},
    {"id": 12, "name": "Friendship Bracelet", "price": 20, "category": "bracelets", "icon": "🧵", "desc": "A small gift for friends."},
    {"id": 13, "name": "Name Bracelet", "price": 45, "category": "bracelets", "icon": "🔤", "desc": "Bracelet personalised with a name."},
    {"id": 14, "name": "Gift Combo", "price": 110, "category": "combos", "icon": "🎁", "desc": "Popular items in one useful combo."},
    {"id": 15, "name": "Lumen Planner", "price": 24, "category": "stationery", "icon": "🗓️", "desc": "Premium weekly planner for students."},
    {"id": 16, "name": "Halo Notes", "price": 16, "category": "stationery", "icon": "📝", "desc": "Soft-touch notes for focused study."},
]

FILTERS = ["all", "stationery", "keychains", "bracelets", "combos"]

ACCOUNTS = {
    "ridhaan": {"password": "123456", "name": "ridhaan Aggrawal", "role": "CEO", "summary": "Leads business planning, pricing, operations and company growth."},
    "sahil": {"password": "123456", "name": "Sahil Singh", "role": "CMO", "summary": "Leads promotion, customer communication and brand strategy."},
}


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL, name TEXT NOT NULL, role TEXT NOT NULL, summary TEXT NOT NULL)")
    return conn


def seed_default_users():
    conn = get_db_connection()
    try:
        for username, account in ACCOUNTS.items():
            conn.execute(
                "INSERT OR IGNORE INTO users (username, password, name, role, summary) VALUES (?, ?, ?, ?, ?)",
                (username, account["password"], account["name"], account["role"], account["summary"]),
            )
        conn.commit()
    finally:
        conn.close()


seed_default_users()


def authenticate_user(username: str, password: str, accounts=None):
    if accounts is None:
        conn = get_db_connection()
        try:
            row = conn.execute("SELECT username, password, name, role, summary FROM users WHERE username = ?", (username.strip().lower(),)).fetchone()
            if row and row["password"] == password:
                return {
                    "username": row["username"],
                    "password": row["password"],
                    "name": row["name"],
                    "role": row["role"],
                    "summary": row["summary"],
                }
            return None
        finally:
            conn.close()
    accounts = ACCOUNTS if accounts is None else accounts
    account = accounts.get(username.strip().lower())
    if account and account.get("password") == password:
        return account
    return None


def register_user(username: str, password: str, name: str, role: str, accounts=None):
    if accounts is None:
        normalized_username = username.strip().lower()
        if not normalized_username:
            return None
        conn = get_db_connection()
        try:
            existing = conn.execute("SELECT 1 FROM users WHERE username = ?", (normalized_username,)).fetchone()
            if existing:
                return None
            conn.execute(
                "INSERT INTO users (username, password, name, role, summary) VALUES (?, ?, ?, ?, ?)",
                (normalized_username, password, name or "New User", role or "Member", "New team member onboarded to Class Cart."),
            )
            conn.commit()
            return {
                "username": normalized_username,
                "password": password,
                "name": name or "New User",
                "role": role or "Member",
                "summary": "New team member onboarded to Class Cart.",
            }
        finally:
            conn.close()
    accounts = ACCOUNTS if accounts is None else accounts
    normalized_username = username.strip().lower()
    if not normalized_username or normalized_username in accounts:
        return None
    accounts[normalized_username] = {
        "password": password,
        "name": name,
        "role": role,
        "summary": "New team member onboarded to Class Cart.",
    }
    return accounts[normalized_username]


def get_theme_css():
    return """
    <style>
    .stApp { background: linear-gradient(135deg, #050505 0%, #0d0d0f 100%); }
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }
    .hero-card { background: linear-gradient(135deg, #121216 0%, #09090b 100%); border: 1px solid rgba(255,255,255,0.12); border-radius: 24px; padding: 2rem; margin-bottom: 1.2rem; box-shadow: 0 24px 64px rgba(0,0,0,0.35); }
    .top-strip { background: linear-gradient(90deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03)); border: 1px solid rgba(255,255,255,0.1); border-radius: 999px; padding: 0.7rem 1rem; margin-bottom: 1rem; display:flex; justify-content:space-between; align-items:center; }
    .brand-badge { display:flex; align-items:center; gap:0.7rem; font-weight:700; }
    .brand-badge img { width:38px; height:38px; border-radius:12px; }
    .section-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 1.1rem; margin-bottom: 1rem; box-shadow: 0 12px 32px rgba(0,0,0,0.2); }
    .product-card { background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%); border: 1px solid rgba(255,255,255,0.12); border-radius: 20px; padding: 1rem; height: 100%; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .team-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 22px; padding: 1.3rem; text-align: center; }
    .muted { color: #b8b8c0; }
    .tiny { color: #9a9aa2; font-size: 0.8rem; }
    .pill { background: white; color: black; border-radius: 999px; padding: 0.4rem 0.7rem; font-weight: 700; }
    .stButton > button { border-radius: 999px; border: 1px solid rgba(255,255,255,0.16); background: rgba(255,255,255,0.04); color: white; }
    .stButton > button:hover { border-color: rgba(255,255,255,0.26); }
    [data-testid="stSidebar"] { background: #050505; border-left: 1px solid rgba(255,255,255,0.08); }
    </style>
    """


def initialize_session():
    st.session_state.setdefault("cart", {})
    st.session_state.setdefault("search_term", "")
    st.session_state.setdefault("active_category", "all")
    st.session_state.setdefault("show_login", False)
    st.session_state.setdefault("show_signup", False)
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("view", "home")
    st.session_state.setdefault("dashboard_open", False)
    st.session_state.setdefault("auth_page", "login")


def set_view(view_name: str):
    st.session_state["view"] = view_name


def open_auth_page(page_name: str):
    st.session_state["auth_page"] = page_name
    st.session_state["show_login"] = False
    st.session_state["show_signup"] = False
    set_view(page_name)


def add_to_cart(cart, product_id, quantity=1):
    new_cart = dict(cart)
    new_cart[product_id] = new_cart.get(product_id, 0) + quantity
    return new_cart


def update_cart_quantity(cart, product_id, delta):
    new_cart = dict(cart)
    new_cart[product_id] = new_cart.get(product_id, 0) + delta
    if new_cart.get(product_id, 0) <= 0:
        new_cart.pop(product_id, None)
    return new_cart


def filter_products(search_term: str, category: str):
    search_term = search_term.lower().strip()
    normalized_category = (category or "all").lower()
    filtered = PRODUCTS
    if normalized_category != "all":
        filtered = [product for product in filtered if product["category"] == normalized_category]
    if search_term:
        filtered = [
            product
            for product in filtered
            if search_term in product["name"].lower() or search_term in product["desc"].lower()
        ]
    return filtered


def calculate_cart_total(cart):
    total = 0
    for product_id, quantity in cart.items():
        product = next((item for item in PRODUCTS if item["id"] == product_id), None)
        if product:
            total += product["price"] * quantity
    return total


def get_cart_items(cart):
    items = []
    for product_id, quantity in cart.items():
        product = next((item for item in PRODUCTS if item["id"] == product_id), None)
        if product and quantity > 0:
            items.append({**product, "qty": quantity})
    return items


def render_header():
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    st.markdown("<div class='top-strip'><div class='brand-badge'><img src='data:image/svg+xml;base64,{}' alt='Class Cart logo' /><div><div>Class Cart</div><div class='muted' style='font-size:0.78rem;font-weight:500;'>student essentials • since 2026</div></div></div><div class='muted'>smart school essentials</div></div>".format(__import__('base64').b64encode(Path(__file__).resolve().parent.joinpath('logo.svg').read_bytes()).decode()), unsafe_allow_html=True)
    nav = st.columns([1, 1, 1, 1, 1, 1, 1, 1.2])
    with nav[0]:
        if st.button("Shop", use_container_width=True):
            set_view("shop")
            st.session_state["active_category"] = "all"
    with nav[1]:
        if st.button("Categories", use_container_width=True):
            set_view("shop")
            st.session_state["active_category"] = "stationery"
    with nav[2]:
        if st.button("Team", use_container_width=True):
            set_view("team")
            st.session_state["show_login"] = True
            st.session_state["dashboard_open"] = False
    with nav[3]:
        if st.button("Team Login", use_container_width=True):
            set_view("team_login")
            st.session_state["dashboard_open"] = False
    with nav[4]:
        if st.button("Dashboard", use_container_width=True):
            set_view("dashboard")
            st.session_state["show_login"] = False
    with nav[5]:
        if st.button("Login", use_container_width=True):
            open_auth_page("login")
    with nav[6]:
        if st.button("Sign up", use_container_width=True):
            open_auth_page("signup")
    with nav[7]:
        if st.button(f"Cart · {sum(st.session_state['cart'].values())}", use_container_width=True):
            set_view("cart")
            st.session_state["show_login"] = False
            st.session_state["dashboard_open"] = False


def handle_cart_update(product_id, quantity=1):
    current_cart = st.session_state.get("cart", {})
    st.session_state["cart"] = add_to_cart(current_cart, product_id, quantity)
    st.rerun()


def render_hero():
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    left, right = st.columns([1.2, 0.8], gap="large")

    with left:
        st.caption("STUDENT ESSENTIALS • SINCE 2026")
        st.markdown("<h1 style='font-size:3rem;line-height:1.05;margin:0.2rem 0 0.8rem;'>Everything you need.<br><span style='color:#777780;'>Nothing you don't.</span></h1>", unsafe_allow_html=True)
        st.markdown("<p class='muted' style='font-size:1rem;max-width:650px;'>Premium stationery, customised accessories and useful school essentials—simple, smart and student-friendly.</p>", unsafe_allow_html=True)
        action_cols = st.columns(2)
        with action_cols[0]:
            if st.button("Explore products", use_container_width=True):
                set_view("shop")
                st.session_state["active_category"] = "all"
        with action_cols[1]:
            if st.button("Meet the team", use_container_width=True):
                set_view("team")
                st.session_state["show_login"] = True

        stats = st.columns(3)
        stats[0].metric("14", "products")
        stats[1].metric("₹5", "starting price")
        stats[2].metric("2026", "founded")

    with right:
        st.markdown(
            """
            <div class='section-card'>
                <div style='font-size:4rem;text-align:center;'>🎁</div>
                <h3 style='margin:0.4rem 0 0.2rem;'>Student Gift Combo</h3>
                <p class='muted'>A useful mix of popular Class Cart products.</p>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-top:1rem;'><strong>₹110</strong><span class='pill'>Add</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Add combo", key="combo_add", use_container_width=True):
            handle_cart_update(14)

    st.markdown("</div>", unsafe_allow_html=True)


def render_catalog():
    st.markdown("<a id='shop'></a>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:0.3rem;'>Shop Class Cart</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted'>Search, filter and add your favourite products to the cart.</p>", unsafe_allow_html=True)

    search_col, filter_col = st.columns([2, 1])
    with search_col:
        st.session_state["search_term"] = st.text_input("Search products", value=st.session_state["search_term"], placeholder="Search products...")
    with filter_col:
        st.session_state["active_category"] = st.selectbox("Category", FILTERS, index=FILTERS.index(st.session_state["active_category"]))

    filtered_products = filter_products(st.session_state["search_term"], st.session_state["active_category"])

    if not filtered_products:
        st.info("No products found.")
        return

    cols = st.columns(4)
    for index, product in enumerate(filtered_products):
        column = cols[index % 4]
        with column:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:3rem;text-align:center;'>{product['icon']}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0.4rem 0 0.2rem;'>{product['name']}</h4>", unsafe_allow_html=True)
            st.caption(product["category"].upper())
            st.write(product["desc"])
            st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;margin-top:1rem;'><strong>₹{product['price']}</strong><span class='tiny'>Add to cart</span></div>", unsafe_allow_html=True)
            if st.button("Add", key=f"add_{product['id']}", use_container_width=True):
                handle_cart_update(product["id"])
            st.markdown("</div>", unsafe_allow_html=True)


def render_features():
    st.markdown("<a id='categories'></a>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-top:2rem;'>Designed for everyday school life.</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted'>Simple prices, useful products and personalised options—all in one student-run store.</p>", unsafe_allow_html=True)
    feature_cols = st.columns(3)
    for col, (title, desc) in zip(feature_cols, [("Student-friendly prices", "Affordable products starting from just ₹5."), ("Customised options", "Name bracelets and keychains made personally for you."), ("Simple ordering", "Add items to your cart and prepare your order quickly.")]):
        with col:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0.2rem 0;'>{title}</h4>", unsafe_allow_html=True)
            st.write(desc)
            st.markdown("</div>", unsafe_allow_html=True)


def render_team():
    st.markdown("<a id='team'></a>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-top:2.5rem;'>The team behind Class Cart</h2>", unsafe_allow_html=True)
    team = [
        ("HA", "CHIEF EXECUTIVE OFFICER", "Hridhaan Aggrawal", "Leads business planning, pricing, operations and company growth."),
        ("SS", "CHIEF MARKETING OFFICER", "Sahil Singh", "Leads promotion, customer communication and brand strategy."),
        ("VC", "HEAD OF INVENTORY", "Vivaan Chawla", "Manages inventory and stock."),
        ("IA", "INVENTORY ASSISTANT", "To Be Assigned", "Supports inventory operations."),
    ]
    cols = st.columns(2)
    for col, (avatar, role, name, bio) in zip(cols, team):
        with col:
            st.markdown("<div class='team-card'>", unsafe_allow_html=True)
            st.markdown(f"<div style='width:72px;height:72px;border-radius:50%;background:white;color:black;display:grid;place-items:center;margin:auto;font-size:1.3rem;font-weight:700;'>{avatar}</div>", unsafe_allow_html=True)
            st.markdown(f"<p class='tiny' style='margin:0.4rem 0 0.1rem;'>{role}</p>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0.2rem 0;'>{name}</h4>", unsafe_allow_html=True)
            st.write(bio)
            st.markdown("</div>", unsafe_allow_html=True)


def render_auth_page(page_name: str):
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    if page_name == "signup":
        st.markdown("### Create your account")
        st.write("Create a new account to access the team dashboard.")
        signup_username = st.text_input("Choose a username", key="auth_signup_username")
        signup_password = st.text_input("Choose a password", type="password", key="auth_signup_password")
        signup_name = st.text_input("Your name", key="auth_signup_name")
        signup_role = st.text_input("Role", key="auth_signup_role")
        if st.button("Create account"):
            account = register_user(signup_username, signup_password, signup_name or "New User", signup_role or "Member")
            if account:
                st.session_state["user"] = account
                st.session_state["show_signup"] = False
                st.session_state["dashboard_open"] = True
                set_view("dashboard")
                st.success("Account created successfully.")
            else:
                st.error("That username is already taken.")
        if st.button("Go to login"):
            open_auth_page("login")
    else:
        st.markdown("### Login to Class Cart")
        st.write("Sign in to continue to your dashboard.")
        username = st.text_input("Username", key="auth_login_username")
        password = st.text_input("Password", type="password", key="auth_login_password")
        if st.button("Log in"):
            account = authenticate_user(username, password)
            if account:
                st.session_state["user"] = account
                st.session_state["show_login"] = False
                st.session_state["dashboard_open"] = True
                set_view("dashboard")
                st.success(f"Welcome back, {account['name']}!")
            else:
                st.error("Incorrect username or password.")
        if st.button("Create an account"):
            open_auth_page("signup")
    st.markdown("</div>", unsafe_allow_html=True)


def render_team_login_page():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### Team login")
    st.write("Access the leadership dashboard from this dedicated page.")
    username = st.text_input("Username", key="team_login_username")
    password = st.text_input("Password", type="password", key="team_login_password")
    if st.button("Continue"):
        account = authenticate_user(username, password)
        if account:
            st.session_state["user"] = account
            st.session_state["show_login"] = False
            st.session_state["dashboard_open"] = True
            set_view("dashboard")
            st.success("Welcome back.")
        else:
            st.error("Incorrect username or password.")
    st.markdown("</div>", unsafe_allow_html=True)


def render_leadership_dashboard_page():
    if not st.session_state.get("user"):
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("### Leadership dashboard")
        st.write("Please sign in from the Team Login page to access the leadership dashboard.")
        if st.button("Go to Team Login"):
            set_view("team_login")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### Leadership dashboard")
    account = st.session_state["user"]
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;'><div><strong>{account['name']}</strong><div class='muted'>{account['role']}</div></div><span class='pill'>Active</span></div>", unsafe_allow_html=True)
    st.write(account["summary"])

    summary_cols = st.columns(4)
    summary_cols[0].metric("Products", "16")
    summary_cols[1].metric("Starting price", "₹5")
    summary_cols[2].metric("Best combo", "₹110")
    summary_cols[3].metric("Orders ready", "3")

    action_cols = st.columns(2)
    with action_cols[0]:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Store overview")
        st.write("Monitor the product range, pricing and featured bundles in one place.")
        st.markdown("</div>", unsafe_allow_html=True)
    with action_cols[1]:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Team operations")
        st.write("Keep the team login, onboarding and dashboard access organised for the store.")
        st.markdown("</div>", unsafe_allow_html=True)

    button_cols = st.columns(2)
    with button_cols[0]:
        if st.button("Back to shop"):
            st.session_state["dashboard_open"] = False
            set_view("home")
    with button_cols[1]:
        if st.button("Log out"):
            st.session_state.pop("user", None)
            st.session_state["dashboard_open"] = False
            set_view("team_login")
    st.markdown("</div>", unsafe_allow_html=True)


def render_login_and_dashboard():
    if st.session_state["view"] == "dashboard":
        render_leadership_dashboard_page()
    else:
        render_team_login_page()


def render_cart_sidebar():
    st.sidebar.markdown("<div style='display:flex;align-items:center;gap:0.7rem;padding:0.3rem 0 0.8rem 0;'><img src='data:image/svg+xml;base64,{}' style='width:36px;height:36px;border-radius:10px;' /><div><div style='font-weight:700;'>Class Cart</div><div style='font-size:0.78rem;color:#9a9aa2;'>school essentials</div></div></div>".format(__import__('base64').b64encode(Path(__file__).resolve().parent.joinpath('logo.svg').read_bytes()).decode()), unsafe_allow_html=True)
    st.sidebar.header("Your cart")
    cart = st.session_state.setdefault("cart", {})
    if not cart:
        st.sidebar.write("Your cart is empty. Add a few essentials to build your setup.")
        return

    items = get_cart_items(cart)
    for product in items:
        st.sidebar.markdown(f"**{product['name']}**")
        st.sidebar.write(f"₹{product['price']} each")
        qty_cols = st.sidebar.columns([1, 1, 1])
        with qty_cols[0]:
            if st.sidebar.button("−", key=f"dec_{product['id']}"):
                st.session_state["cart"] = update_cart_quantity(st.session_state.get("cart", {}), product["id"], -1)
                st.rerun()
        with qty_cols[1]:
            st.sidebar.write(f"{product['qty']}")
        with qty_cols[2]:
            if st.sidebar.button("+", key=f"inc_{product['id']}"):
                st.session_state["cart"] = update_cart_quantity(st.session_state.get("cart", {}), product["id"], 1)
                st.rerun()

    total = calculate_cart_total(cart)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### Total: ₹{total}")
    if st.sidebar.button("Prepare order"):
        st.sidebar.success("Order prepared. Connect WhatsApp or a secure backend for real orders.")


def render_cart_view():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.header("Your cart")
    cart = st.session_state.get("cart", {})
    if not cart:
        st.info("Your cart is empty. Add a few essentials to build your setup.")
        return

    items = get_cart_items(cart)
    for product in items:
        cols = st.columns([2, 1, 1])
        with cols[0]:
            st.write(f"**{product['name']}**")
        with cols[1]:
            st.write(f"₹{product['price']} each")
        with cols[2]:
            st.write(f"Qty: {product['qty']}")

    total = calculate_cart_total(cart)
    st.markdown("---")
    st.subheader(f"Total: ₹{total}")
    st.markdown("</div>", unsafe_allow_html=True)


def main():
    initialize_session()
    render_header()

    if st.session_state["view"] == "cart":
        render_cart_view()
    elif st.session_state["view"] == "dashboard":
        render_login_and_dashboard()
    elif st.session_state["view"] == "team_login":
        render_login_and_dashboard()
    elif st.session_state["view"] in {"login", "signup"}:
        render_auth_page(st.session_state["view"])
    else:
        render_hero()
        render_catalog()
        render_features()
        render_team()
        render_login_and_dashboard()

    render_cart_sidebar()


if __name__ == "__main__":
    main()
