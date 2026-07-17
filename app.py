import streamlit as st

st.set_page_config(page_title="Class Cart", page_icon="📚", layout="wide")

PRODUCTS = [
    {
        "id": 1,
        "name": "Lumen Planner",
        "category": "Study",
        "description": "A premium weekly planner for keeping deadlines and routines in one place.",
        "price": 24,
        "emoji": "🗓️",
    },
    {
        "id": 2,
        "name": "Halo Notes",
        "category": "Study",
        "description": "Soft-touch notebooks with thick paper for deep-focus writing sessions.",
        "price": 16,
        "emoji": "📝",
    },
    {
        "id": 3,
        "name": "Orbit Pen Set",
        "category": "Stationery",
        "description": "Minimal pens that feel smooth in hand and look great on every desk.",
        "price": 18,
        "emoji": "✒️",
    },
    {
        "id": 4,
        "name": "Nova Desk Mat",
        "category": "Desk",
        "description": "A matte desk protector that keeps your workspace calm and tidy.",
        "price": 29,
        "emoji": "🖥️",
    },
    {
        "id": 5,
        "name": "Pulse Tote",
        "category": "Travel",
        "description": "A slim tote with cable pockets and room for your daily essentials.",
        "price": 35,
        "emoji": "🎒",
    },
    {
        "id": 6,
        "name": "Focus Bundle",
        "category": "Bundles",
        "description": "Planner, notes, and pen set combined into one refined starter pack.",
        "price": 54,
        "emoji": "📦",
    },
]

CATEGORIES = ["All", "Study", "Stationery", "Desk", "Travel", "Bundles"]


def filter_products(search_term: str, category: str):
    search_term = search_term.lower().strip()
    filtered = PRODUCTS

    if category != "All":
        filtered = [product for product in filtered if product["category"] == category]

    if search_term:
        filtered = [
            product
            for product in filtered
            if search_term in product["name"].lower()
            or search_term in product["description"].lower()
            or search_term in product["category"].lower()
        ]

    return filtered


def render_header():
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1rem; }
        .hero-card {
            background: linear-gradient(135deg, #121216 0%, #09090b 100%);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 24px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        }
        .section-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }
        .product-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 20px;
            padding: 1rem;
            height: 100%;
        }
        .tiny { color: #9a9aa2; font-size: 0.8rem; }
        .muted { color: #bcbcc6; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    top = st.columns([3, 1, 1, 1])
    with top[0]:
        st.markdown("<div style='font-size:1.15rem;font-weight:700;'>Class Cart</div>", unsafe_allow_html=True)
    with top[1]:
        st.markdown("[Shop](#shop)", unsafe_allow_html=True)
    with top[2]:
        st.markdown("[Features](#features)", unsafe_allow_html=True)
    with top[3]:
        st.markdown("[Team](#team)", unsafe_allow_html=True)


def render_hero():
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 0.8], gap="large")

    with col1:
        st.caption("PREMIUM DARK STATIONERY")
        st.markdown("<h1 style='font-size:3rem;line-height:1.05;margin:0.2rem 0 0.8rem;'>The calmest way to organize your study life.</h1>", unsafe_allow_html=True)
        st.markdown("<p class='muted' style='font-size:1.02rem;max-width:650px;'>Class Cart brings together planners, notebooks, and desk accessories in one refined shop built for students who value focus.</p>", unsafe_allow_html=True)
        buttons = st.columns([0.25, 0.25])
        with buttons[0]:
            st.button("Start shopping", use_container_width=True)
        with buttons[1]:
            st.button("Explore essentials", use_container_width=True)

        stats = st.columns(3)
        stats[0].metric("4.9/5", "student rated")
        stats[1].metric("24h", "dispatch")
        stats[2].metric("100%", "curated")

    with col2:
        st.markdown(
            """
            <div class='section-card'>
                <div style='font-size:4rem;text-align:center;'>📚</div>
                <h3 style='margin:0.4rem 0 0.2rem;'>Focus Edition</h3>
                <p class='muted'>An elevated starter set with planner, notes, and matte accessories.</p>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-top:1rem;'><strong>$54</strong><span style='background:white;color:black;border-radius:999px;padding:0.4rem 0.7rem;font-weight:700;'>Add</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_catalog():
    st.markdown("<a id='shop'></a>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:0.3rem;'>Shop essentials</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted'>Search by product or browse the categories below.</p>", unsafe_allow_html=True)

    search_col, filter_col = st.columns([2, 1])
    with search_col:
        search_term = st.text_input("Search", placeholder="Try planner, desk, or tote")
    with filter_col:
        category = st.selectbox("Category", CATEGORIES)

    filtered_products = filter_products(search_term, category)

    cols = st.columns(3)
    for index, product in enumerate(filtered_products):
        column = cols[index % 3]
        with column:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:3rem;text-align:center;'>{product['emoji']}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0.4rem 0 0.2rem;'>{product['name']}</h4>", unsafe_allow_html=True)
            st.caption(product["category"])
            st.write(product["description"])
            st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;margin-top:1rem;'><strong>${product['price']}</strong><span class='tiny'>Curated pick</span></div>", unsafe_allow_html=True)
            if st.button("Add to cart", key=f"add_{product['id']}", use_container_width=True):
                cart = st.session_state.setdefault("cart", {})
                cart[product["id"]] = cart.get(product["id"], 0) + 1
                st.session_state["cart"] = cart
            st.markdown("</div>", unsafe_allow_html=True)


def render_features():
    st.markdown("<a id='features'></a>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-top:2rem;'>Why students choose Class Cart</h2>", unsafe_allow_html=True)

    feature_cols = st.columns(3)
    feature_cards = [
        ("🧠", "Focus-first design", "Every product is selected to keep your desk calm, useful, and distraction-free."),
        ("⚡", "Fast delivery", "Orders are prepared quickly so you can get back to your routine without delay."),
        ("🌙", "Minimal styling", "Dark materials and soft details make your workspace feel polished and intentional."),
    ]

    for col, (emoji, title, description) in zip(feature_cols, feature_cards):
        with col:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:2rem;'>{emoji}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0.2rem 0;'>{title}</h4>", unsafe_allow_html=True)
            st.write(description)
            st.markdown("</div>", unsafe_allow_html=True)


def render_team():
    st.markdown("<a id='team'></a>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-top:2rem;'>Meet the team</h2>", unsafe_allow_html=True)

    team = [
        ("A", "Founder", "Ari builds the collection around calm routines and useful design."),
        ("M", "Product Lead", "Mina translates student needs into polished desk and study essentials."),
    ]

    cols = st.columns(2)
    for col, (avatar, role, bio) in zip(cols, team):
        with col:
            st.markdown("<div class='section-card' style='text-align:center;'>", unsafe_allow_html=True)
            st.markdown(f"<div style='width:72px;height:72px;border-radius:50%;background:white;color:black;display:grid;place-items:center;margin:auto;font-size:1.3rem;font-weight:700;'>{avatar}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0.4rem 0 0.2rem;'>{role}</h4>", unsafe_allow_html=True)
            st.write(bio)
            st.markdown("</div>", unsafe_allow_html=True)


def render_cart_sidebar():
    st.sidebar.header("Your cart")
    cart = st.session_state.setdefault("cart", {})

    if not cart:
        st.sidebar.write("Your cart is empty. Add a few essentials to build your setup.")
        return

    total = 0
    for product_id, quantity in list(cart.items()):
        product = next(item for item in PRODUCTS if item["id"] == product_id)
        line_total = product["price"] * quantity
        total += line_total
        st.sidebar.markdown(f"**{product['name']}** x{quantity}")
        st.sidebar.write(f"${line_total}")

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### Total: ${total}")
    if st.sidebar.button("Checkout", use_container_width=True):
        st.sidebar.success("Checkout is ready for the next step.")


def main():
    render_header()
    render_hero()
    render_catalog()
    render_features()
    render_team()
    render_cart_sidebar()


if __name__ == "__main__":
    main()
