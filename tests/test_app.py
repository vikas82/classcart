import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app


def test_products_available():
    assert len(app.PRODUCTS) >= 4
    assert any(product["name"] == "Back-to-School Combo" for product in app.PRODUCTS)


def test_filter_products_search():
    results = app.filter_products("combo", "All")
    assert len(results) >= 1
    assert any(product["name"] == "Back-to-School Combo" for product in results)

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


def test_register_user_uses_defaults_for_missing_name_or_role():
    users = {}
    created = app.register_user("anotheruser", "pass123", "", "", users)
    assert created is not None
    assert users["anotheruser"]["name"] == "New User"
    assert users["anotheruser"]["role"] == "Member"


def test_authenticate_user_normalizes_username_and_returns_consistent_payload():
    users = {"demo": {"password": "secret", "name": "Demo User", "role": "Staff", "summary": "Demo summary"}}
    account = app.authenticate_user(" DEMO ", "secret", users)
    assert account is not None
    assert account["username"] == "demo"
    assert account["name"] == "Demo User"


def test_role_dashboard_config_contains_role_specific_sections():
    ceo_config = app.get_role_dashboard_config("CEO")
    inventory_config = app.get_role_dashboard_config("Head of Inventory")

    assert ceo_config["icon"] == "👑"
    assert "Attendance" in ceo_config["cards"]
    assert inventory_config["icon"] == "📦"
    assert "Inventory rating" in inventory_config["cards"]


def test_seed_default_users_refreshes_existing_credentials(tmp_path, monkeypatch):
    monkeypatch.setattr(app, "DB_PATH", tmp_path / "classcart.db")

    conn = sqlite3.connect(app.DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL, name TEXT NOT NULL, role TEXT NOT NULL, summary TEXT NOT NULL)"
    )
    conn.execute(
        "INSERT INTO users (username, password, name, role, summary) VALUES (?, ?, ?, ?, ?)",
        ("ridhaan", "123456", "Old User", "Old Role", "old summary"),
    )
    conn.commit()
    conn.close()

    app.seed_default_users()

    legacy = sqlite3.connect(app.DB_PATH).execute(
        "SELECT username FROM users WHERE username = ?",
        ("ridhaan",),
    ).fetchone()
    assert legacy is None

    ceo = sqlite3.connect(app.DB_PATH).execute(
        "SELECT password, name, role FROM users WHERE username = ?",
        ("hridhaan",),
    ).fetchone()
    assert ceo[0] == "ceo@cc4007"
    assert ceo[1] == "Hridhaan Aggrawal"
    assert ceo[2] == "CEO"


def test_database_authentication_uses_sqlite():
    account = app.authenticate_user("hridhaan", "ceo@cc4007")
    assert account is not None
    assert account["name"] == "Hridhaan Aggrawal"


def test_mark_attendance_records_daily_presence_once(tmp_path, monkeypatch):
    monkeypatch.setattr(app, "DB_PATH", tmp_path / "attendance.db")

    first_mark = app.mark_attendance("hridhaan")
    second_mark = app.mark_attendance("hridhaan")

    assert first_mark is True
    assert second_mark is False

    conn = sqlite3.connect(app.DB_PATH)
    rows = conn.execute("SELECT username, attendance_date FROM attendance_logs WHERE username = ?", ("hridhaan",)).fetchall()
    conn.close()

    assert len(rows) == 1


def test_get_todays_attendance_summary_lists_present_leadership(tmp_path, monkeypatch):
    monkeypatch.setattr(app, "DB_PATH", tmp_path / "attendance.db")

    app.mark_attendance("hridhaan")
    app.mark_attendance("vivaan")

    summary = app.get_todays_attendance_summary()

    assert "hridhaan" in summary
    assert "vivaan" in summary


def test_shared_theme_css_contains_consistent_ui_classes():
    css = app.get_theme_css()
    assert ".hero-card" in css
    assert ".section-card" in css
    assert ".product-card" in css
    assert ".team-card" in css
