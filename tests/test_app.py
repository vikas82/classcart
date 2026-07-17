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

    study_results = app.filter_products("", "Study")
    assert len(study_results) >= 2
