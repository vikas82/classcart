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
