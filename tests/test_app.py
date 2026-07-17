import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app


def test_products_available():
    assert len(app.PRODUCTS) >= 4
    assert any(product["name"] == "Lumen Planner" for product in app.PRODUCTS)


def test_filter_products_search():
    results = app.filter_products("planner", "All")
    assert len(results) >= 1
    assert any(product["name"] == "Lumen Planner" for product in results)

    study_results = app.filter_products("", "stationery")
    assert len(study_results) >= 2


def test_cart_total_calculation():
    cart = {1: 2, 2: 1}
    assert app.calculate_cart_total(cart) == 30


def test_add_to_cart_increments_quantity():
    cart = {1: 2}
    updated_cart = app.add_to_cart(cart, 1, 1)
    assert updated_cart[1] == 3


def test_authenticate_user_with_known_account():
    users = {"demo": {"password": "secret", "name": "Demo User", "role": "Staff"}}
    assert app.authenticate_user("demo", "secret", users) is not None
    assert app.authenticate_user("demo", "wrong", users) is None


def test_register_user_creates_account():
    users = {}
    created = app.register_user("newuser", "pass123", "New User", "Staff", users)
    assert created is not None
    assert users["newuser"]["password"] == "pass123"
    assert users["newuser"]["name"] == "New User"


def test_shared_theme_css_contains_consistent_ui_classes():
    css = app.get_theme_css()
    assert ".hero-card" in css
    assert ".section-card" in css
    assert ".product-card" in css
    assert ".team-card" in css
