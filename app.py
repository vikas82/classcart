import streamlit as st

st.set_page_config(page_title="Class Cart", page_icon="📚", layout="wide")

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
    "hridhaan": {"password": "Ceo@456", "name": "Hridhaan Aggrawal", "role": "CEO", "summary": "Leads business planning, pricing, operations and company growth."},
    "sahil": {"password": "Cmo@321", "name": "Sahil Singh", "role": "CMO", "summary": "Leads promotion, customer communication and brand strategy."},
}


def get_theme_css():
    return """
    <style>
    .stApp { background: linear-gradient(135deg, #050505 0%, #0d0d0f 100%); }
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }
    .hero-card { background: linear-gradient(135deg, #121216 0%, #09090b 100%); border: 1px solid rgba(255,255,255,0.12); border-radius: 24px; padding: 2rem; margin-bottom: 1.2rem; box-shadow: 0 24px 64px rgba(0,0,0,0.35); }
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
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("view", "home")


def set_view(view_name: str):
    st.session_state["view"] = view_name


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

    st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;'><div style='font-size:1.15rem;font-weight:700;'>Class Cart</div><div class='muted'>student essentials • since 2026</div></div>", unsafe_allow_html=True)
    nav = st.columns([1, 1, 1, 1.4])
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
    with nav[3]:
        if st.button(f"Cart · {sum(st.session_state['cart'].values())}", use_container_width=True):
            set_view("cart")
            st.session_state["show_login"] = False


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
            st.session_state["cart"] = add_to_cart(st.session_state["cart"], 14)

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
                st.session_state["cart"] = add_to_cart(st.session_state["cart"], product["id"])
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


def render_login_and_dashboard():
    if st.session_state.get("show_login"):
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("### Team login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Continue"):
            account = ACCOUNTS.get(username.strip().lower())
            if account and account["password"] == password:
                st.session_state["user"] = account
                st.session_state["show_login"] = False
                st.success("Welcome back.")
            else:
                st.error("Incorrect username or password.")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("user"):
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Leadership dashboard")
        account = st.session_state["user"]
        st.markdown(f"**{account['name']}** · {account['role']}")
        st.write(account["summary"])
        cols = st.columns(3)
        cols[0].metric("Total products", "14")
        cols[1].metric("Starting price", "₹5")
        cols[2].metric("Featured combo", "₹110")
        if st.button("Log out"):
            st.session_state.pop("user", None)
        st.markdown("</div>", unsafe_allow_html=True)


def render_cart_sidebar():
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
                st.session_state["cart"] = update_cart_quantity(st.session_state["cart"], product["id"], -1)
        with qty_cols[1]:
            st.sidebar.write(f"{product['qty']}")
        with qty_cols[2]:
            if st.sidebar.button("+", key=f"inc_{product['id']}"):
                st.session_state["cart"] = update_cart_quantity(st.session_state["cart"], product["id"], 1)

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
    else:
        render_hero()
        render_catalog()
        render_features()
        render_team()
        render_login_and_dashboard()

    render_cart_sidebar()


if __name__ == "__main__":
    main()
