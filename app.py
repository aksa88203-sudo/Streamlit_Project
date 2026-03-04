import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
import os
import requests

# Page config
st.set_page_config(
    page_title="Inventory Prediction System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=DM+Mono:wght@400;500&display=swap');
    :root {
        --bg-1: #0b0f16;
        --bg-2: #0f172a;
        --card: rgba(255, 255, 255, 0.06);
        --card-strong: rgba(255, 255, 255, 0.09);
        --stroke: rgba(255, 255, 255, 0.08);
        --text: #e5e7eb;
        --muted: #9aa4b2;
        --accent: #22d3ee;
        --good: #10b981;
        --warn: #f59e0b;
        --bad: #ef4444;
    }
    html, body, [class*="css"] {
        font-family: "Space Grotesk", system-ui, -apple-system, sans-serif;
        color: var(--text);
    }
    .stApp {
        background: radial-gradient(1200px 700px at 10% -10%, #1f2937 0%, var(--bg-1) 55%, var(--bg-2) 100%);
    }
    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 1.5rem;
        max-width: 1250px;
    }
    h1, h2, h3 {
        letter-spacing: -0.02em;
        margin: 0.4rem 0 0.6rem 0;
    }
    p {
        margin: 0.25rem 0;
        color: var(--muted);
    }
    hr {
        margin: 0.6rem 0;
        border-color: var(--stroke);
    }
    /* Hide Streamlit sidebar */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        display: none;
    }
    /* Header */
    .header-shell {
        background: var(--card);
        border: 1px solid var(--stroke);
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }
    .brand {
        font-size: 22px;
        font-weight: 700;
    }
    .subtle {
        color: var(--muted);
        font-size: 12px;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    /* Buttons */
    .stButton>button {
        background: var(--card-strong);
        border: 1px solid var(--stroke);
        color: var(--text);
        height: 40px;
        border-radius: 12px;
        padding: 0 16px;
    }
    .stButton>button:hover {
        border-color: rgba(255,255,255,0.18);
        background: rgba(255,255,255,0.12);
    }
    /* Tabs */
    div[data-testid="stTabs"] {
        background: var(--card);
        border: 1px solid var(--stroke);
        border-radius: 14px;
        padding: 6px 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    button[data-baseweb="tab"] {
        background: transparent;
        color: var(--muted);
        font-weight: 600;
        border-radius: 10px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: rgba(34, 211, 238, 0.12);
        color: #c7f9ff;
    }
    /* Cards */
    .card {
        background: var(--card);
        border: 1px solid var(--stroke);
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .product-card {
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .product-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 30px rgba(0,0,0,0.35);
        border-color: rgba(34, 211, 238, 0.4);
    }
    .login-card {
        background: transparent;
        border: none;
        box-shadow: none;
        padding: 0;
    }
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }
    .stat-label {
        color: var(--muted);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        color: #0b0f16;
        background: #e5e7eb;
    }
    .pill.good { background: #d1fae5; color: #065f46; }
    .pill.warn { background: #fef3c7; color: #92400e; }
    .pill.bad { background: #fee2e2; color: #991b1b; }
    .alert-card {
        background: #fee2e2;
        border: 1px solid #fecaca;
        color: #111827;
        border-radius: 12px;
        padding: 12px 14px;
        margin: 8px 0;
    }
    .overstock-card {
        background: #fef3c7;
        border: 1px solid #fde68a;
        color: #111827;
        border-radius: 12px;
        padding: 12px 14px;
        margin: 8px 0;
    }
    .success-card {
        background: #d1fae5;
        border: 1px solid #a7f3d0;
        color: #064e3b;
        border-radius: 12px;
        padding: 12px 14px;
        margin: 8px 0;
    }
    .auth-shell {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid var(--stroke);
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 14px 32px rgba(0, 0, 0, 0.28);
    }
    .hero-shell {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 0;
        min-height: auto;
    }
    .hero-kpi {
        font-size: 22px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

API_BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8001/api/v1").rstrip("/")


def api_request(method, path, payload=None, params=None, show_errors=True):
    url = f"{API_BASE_URL}{path}"
    try:
        response = requests.request(method=method, url=url, json=payload, params=params, timeout=12)
    except requests.RequestException as exc:
        if show_errors:
            st.error(f"Backend connection failed: {exc}")
        return None

    if response.status_code >= 400:
        if show_errors:
            detail = response.text
            try:
                detail = response.json().get("detail", detail)
            except ValueError:
                pass
            st.error(f"API error ({response.status_code}): {detail}")
        return None

    if response.status_code == 204 or not response.text.strip():
        return {}
    return response.json()


def normalize_sales(sales):
    normalized = []
    for sale in sales:
        normalized.append(
            {
                "id": sale.get("id"),
                "date": str(sale.get("sale_date") or sale.get("date")),
                "product": sale.get("product_name") or sale.get("product") or "Unknown",
                "quantity": int(sale.get("quantity", 0)),
                "total": float(sale.get("total", 0)),
            }
        )
    return normalized


def refresh_backend_data(show_errors=True):
    products = api_request("GET", "/products/", show_errors=show_errors)
    sales = api_request("GET", "/sales/", show_errors=show_errors)

    if products is None or sales is None:
        return False

    st.session_state.products = products
    st.session_state.sales = normalize_sales(sales)
    st.session_state.backend_connected = True
    return True


# Initialize session state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = "admin"
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = "Login"
    if 'products' not in st.session_state:
        st.session_state.products = []
    if 'sales' not in st.session_state:
        st.session_state.sales = []
    if 'backend_connected' not in st.session_state:
        st.session_state.backend_connected = False
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = True
        refresh_backend_data(show_errors=False)
    elif not st.session_state.backend_connected:
        refresh_backend_data(show_errors=False)

def get_sample_products():
    return [
        {"id": 1, "name": "Laptop", "sku": "LAP001", "quantity": 45, "reorder_level": 20, "max_stock": 50, "price": 999.99, "category": "Electronics"},
        {"id": 2, "name": "Wireless Mouse", "sku": "MOU001", "quantity": 150, "reorder_level": 30, "max_stock": 100, "price": 29.99, "category": "Electronics"},
        {"id": 3, "name": "USB-C Cable", "sku": "CAB001", "quantity": 8, "reorder_level": 50, "max_stock": 200, "price": 12.99, "category": "Accessories"},
        {"id": 4, "name": "Monitor 27\"", "sku": "MON001", "quantity": 25, "reorder_level": 10, "max_stock": 40, "price": 349.99, "category": "Electronics"},
        {"id": 5, "name": "Keyboard", "sku": "KEY001", "quantity": 180, "reorder_level": 25, "max_stock": 80, "price": 79.99, "category": "Electronics"},
        {"id": 6, "name": "Webcam HD", "sku": "WEB001", "quantity": 12, "reorder_level": 15, "max_stock": 50, "price": 89.99, "category": "Electronics"},
        {"id": 7, "name": "Desk Lamp", "sku": "LAM001", "quantity": 65, "reorder_level": 20, "max_stock": 60, "price": 34.99, "category": "Office"},
        {"id": 8, "name": "Notebook Pack", "sku": "NOT001", "quantity": 200, "reorder_level": 50, "max_stock": 150, "price": 9.99, "category": "Office"},
    ]

def get_sample_sales():
    sales = []
    products = {
        "Laptop": 999.99,
        "Wireless Mouse": 29.99,
        "USB-C Cable": 12.99,
        "Monitor 27\"": 349.99,
        "Keyboard": 79.99,
        "Webcam HD": 89.99,
        "Desk Lamp": 34.99,
        "Notebook Pack": 9.99,
    }
    random.seed(42)
    start_year = 2020
    current_year = datetime.now().year
    sale_id = 1

    # Ensure every year from 2020 to current year has data in all 12 months.
    for year in range(start_year, current_year + 1):
        for month in range(1, 13):
            for _ in range(4):
                product = random.choice(list(products.keys()))
                quantity = random.randint(1, 12)
                day = random.randint(1, 28)
                date = datetime(year, month, day)
                sales.append({
                    "id": sale_id,
                    "date": date.strftime("%Y-%m-%d"),
                    "product": product,
                    "quantity": quantity,
                    "total": round(quantity * products[product], 2),
                })
                sale_id += 1

    # Ensure current day has sales so dashboard "today" stats are always meaningful.
    today = datetime.now()
    for _ in range(3):
        product = random.choice(list(products.keys()))
        quantity = random.randint(1, 6)
        sales.append({
            "id": sale_id,
            "date": today.strftime("%Y-%m-%d"),
            "product": product,
            "quantity": quantity,
            "total": round(quantity * products[product], 2),
        })
        sale_id += 1

    return sorted(sales, key=lambda x: x["date"], reverse=True)

# Authentication
def login_page():
    st.markdown("<h1 style='text-align: center;'>Inventory Prediction System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Professional inventory operations for modern teams.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("<div class='hero-shell'>", unsafe_allow_html=True)
        hero_image_url = "https://tse3.mm.bing.net/th/id/OIP.IiNMpWq2sC2--3lQZYQypQHaDt?rs=1&pid=ImgDetMain&o=7&rm=3"
        st.image(hero_image_url, use_container_width=True)
        st.markdown("### Unified Inventory Control")
        st.markdown("Track stock, monitor sales, and spot risk alerts from one professional workspace.")
        m1, m2, m3 = st.columns(3)
        m1.markdown("<div class='hero-kpi'>99.9%</div><p>Data Visibility</p>", unsafe_allow_html=True)
        m2.markdown("<div class='hero-kpi'>24/7</div><p>Monitoring</p>", unsafe_allow_html=True)
        m3.markdown("<div class='hero-kpi'>5 Tabs</div><p>Operational Views</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='auth-shell'>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Login", use_container_width=True, type="primary" if st.session_state.auth_mode == "Login" else "secondary"):
                st.session_state.auth_mode = "Login"
        with b2:
            if st.button("Register", use_container_width=True, type="primary" if st.session_state.auth_mode == "Register" else "secondary"):
                st.session_state.auth_mode = "Register"

        if st.session_state.auth_mode == "Login":
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="Enter email")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                submit = st.form_submit_button("Login", use_container_width=True)

                if submit:
                    if not (email and password):
                        st.error("Please enter email and password")
                    else:
                        result = api_request(
                            "POST",
                            "/auth/login",
                            payload={"email": email, "password": password},
                            show_errors=True,
                        )
                        if result is not None:
                            st.session_state.authenticated = True
                            st.session_state.username = result.get("user", {}).get("email", email)
                            refresh_backend_data(show_errors=False)
                            st.rerun()
            st.caption("Default account: admin / admin")
        else:
            with st.form("register_form"):
                new_email = st.text_input("Email", placeholder="name@company.com")
                new_password = st.text_input("Password", type="password", placeholder="At least 6 characters")
                confirm_password = st.text_input("Confirm Password", type="password")
                create_account = st.form_submit_button("Create Account", use_container_width=True)

                if create_account:
                    if not (new_email and new_password and confirm_password):
                        st.error("Please fill all fields")
                    elif "@" not in new_email:
                        st.error("Please enter a valid email")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        result = api_request(
                            "POST",
                            "/auth/register",
                            payload={"email": new_email, "password": new_password},
                            show_errors=True,
                        )
                        if result is not None:
                            st.success("Account created successfully. Please login.")
                            st.session_state.auth_mode = "Login"
        st.markdown("</div>", unsafe_allow_html=True)

def header_bar():
    with st.container():
        st.markdown("<div class='header-shell'>", unsafe_allow_html=True)
        col1, col2 = st.columns([7, 3])
        with col1:
            st.markdown("<div class='brand'>📦 Inventory System</div>", unsafe_allow_html=True)
            st.markdown("<div class='subtle'>Inventory intelligence for daily ops</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='subtle'>Signed in</div>", unsafe_allow_html=True)
            st.markdown(f"**{st.session_state.username}**")
            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.username = ""
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Dashboard
def dashboard_page():
    st.markdown("## 📊 Dashboard")
    st.caption("Live snapshot of stock health and sales momentum.")

    products = st.session_state.products
    sales = st.session_state.sales

    # Calculate metrics
    total_products = len(products)
    low_stock = len([p for p in products if p['quantity'] <= p['reorder_level']])
    overstocked = len([p for p in products if p['quantity'] > p['max_stock']])

    today = datetime.now().strftime("%Y-%m-%d")
    today_sales = sum(s['total'] for s in sales if s['date'] == today)
    today_sales_count = len([s for s in sales if s['date'] == today])

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='card'><div class='stat-label'>Total Products</div><div class='stat-value'>{total_products}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='card'><div class='stat-label'>Low Stock</div><div class='stat-value'>{low_stock}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='card'><div class='stat-label'>Overstocked</div><div class='stat-value'>{overstocked}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(
            f"<div class='card'><div class='stat-label'>Today's Sales</div>"
            f"<div class='stat-value'>${today_sales:,.2f}</div>"
            f"<p style='margin-top:6px;'>Count: <strong>{today_sales_count}</strong></p></div>",
            unsafe_allow_html=True,
        )

    # Charts row
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Sales Trend (Last 7 Days)")
        sales_df = pd.DataFrame(sales)
        if not sales_df.empty and 'date' in sales_df.columns and 'total' in sales_df.columns:
            sales_df['date'] = pd.to_datetime(sales_df['date'], errors='coerce')
            sales_df = sales_df.dropna(subset=['date'])
            last_7_days = datetime.now() - timedelta(days=7)
            recent_sales = sales_df[sales_df['date'] >= last_7_days]
            if recent_sales.empty:
                st.info("No sales in the last 7 days.")
            else:
                daily_sales = recent_sales.groupby(recent_sales['date'].dt.date)['total'].sum().reset_index()
                daily_sales.columns = ['Date', 'Total Sales']
                fig = px.line(daily_sales, x='Date', y='Total Sales', markers=True)
                fig.update_layout(height=300, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True, key="dashboard_sales_trend")
        else:
            st.info("Sales data not available yet.")

    with col2:
        st.markdown("### 📊 Stock Levels by Category")
        products_df = pd.DataFrame(products)
        if products_df.empty or 'category' not in products_df.columns or 'quantity' not in products_df.columns:
            st.info("Product data not available yet.")
        else:
            category_stock = products_df.groupby('category')['quantity'].sum().reset_index()
            fig = px.bar(category_stock, x='category', y='quantity', color='category')
            fig.update_layout(height=300, showlegend=False, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True, key="dashboard_category_stock")

    # Second row of charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Top Selling Products")
        sales_df = pd.DataFrame(sales)
        if sales_df.empty or 'product' not in sales_df.columns or 'quantity' not in sales_df.columns:
            st.info("No sales data available.")
        else:
            top_products = sales_df.groupby('product')['quantity'].sum().sort_values(ascending=False).head(5).reset_index()
            fig = px.pie(top_products, values='quantity', names='product', hole=0.4)
            fig.update_layout(height=300, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True, key="dashboard_top_products")

    with col2:
        st.markdown("### 📦 Stock Status Overview")
        status_counts = {
            'Normal': len([p for p in products if p['reorder_level'] < p['quantity'] <= p['max_stock']]),
            'Low Stock': len([p for p in products if p['quantity'] <= p['reorder_level']]),
            'Overstocked': len([p for p in products if p['quantity'] > p['max_stock']])
        }

        fig = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            color=list(status_counts.keys()),
            color_discrete_map={'Normal': '#10b981', 'Low Stock': '#ef4444', 'Overstocked': '#f59e0b'}
        )
        fig.update_layout(height=300, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True, key="dashboard_stock_status")

# Products page
def products_page():
    st.markdown("## 📦 Product Management")
    st.caption("Add, update, and monitor stock levels in one place.")

    # Add product form
    with st.expander("➕ Add New Product", expanded=False):
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Product Name")
                sku = st.text_input("SKU")
                category = st.selectbox("Category", ["Electronics", "Accessories", "Office", "Other"])
                price = st.number_input("Price ($)", min_value=0.01, step=0.01)
            with col2:
                quantity = st.number_input("Current Quantity", min_value=0, step=1)
                reorder_level = st.number_input("Reorder Level", min_value=0, step=1)
                max_stock = st.number_input("Max Stock Level", min_value=1, step=1)

            submit = st.form_submit_button("Add Product", use_container_width=True)

            if submit and name and sku:
                result = api_request(
                    "POST",
                    "/products/",
                    payload={
                        "name": name,
                        "sku": sku,
                        "quantity": int(quantity),
                        "reorder_level": int(reorder_level),
                        "max_stock": int(max_stock),
                        "price": float(price),
                        "category": category,
                    },
                    show_errors=True,
                )
                if result is not None:
                    refresh_backend_data(show_errors=False)
                    st.success(f"Product '{name}' added successfully!")
                    st.rerun()

    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search products", placeholder="Search by name or SKU...")
    with col2:
        filter_status = st.selectbox("Filter by status", ["All", "Low Stock", "Normal", "Overstocked"])

    # Products table
    products = st.session_state.products

    # Apply filters
    if search:
        products = [p for p in products if search.lower() in p['name'].lower() or search.lower() in p['sku'].lower()]

    if filter_status == "Low Stock":
        products = [p for p in products if p['quantity'] <= p['reorder_level']]
    elif filter_status == "Overstocked":
        products = [p for p in products if p['quantity'] > p['max_stock']]
    elif filter_status == "Normal":
        products = [p for p in products if p['reorder_level'] < p['quantity'] <= p['max_stock']]

    # Display products in a grid
    if not products:
        st.info("No products found.")
        return

    cols_per_row = 3
    rows = [products[i:i + cols_per_row] for i in range(0, len(products), cols_per_row)]

    for row in rows:
        cols = st.columns(len(row))
        for idx, product in enumerate(row):

            if product['quantity'] <= product['reorder_level']:
                status = "Low Stock"
                status_class = "bad"
            elif product['quantity'] > product['max_stock']:
                status = "Overstocked"
                status_class = "warn"
            else:
                status = "Normal"
                status_class = "good"

            with cols[idx]:
                st.markdown("<div class='card product-card'>", unsafe_allow_html=True)
                st.markdown(f"**{product['name']}**")
                st.caption(f"SKU: {product['sku']} • {product['category']}")
                st.markdown(f"<span class='pill {status_class}'>{status}</span>", unsafe_allow_html=True)
                st.markdown(f"**Qty:** {product['quantity']}")
                st.markdown(f"**Price:** ${product['price']:.2f}")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Edit", key=f"edit_{product['id']}", use_container_width=True):
                        st.session_state[f"editing_{product['id']}"] = True
                with b2:
                    if st.button("Delete", key=f"delete_{product['id']}", use_container_width=True):
                        result = api_request("DELETE", f"/products/{product['id']}", show_errors=True)
                        if result is not None:
                            refresh_backend_data(show_errors=False)
                            st.rerun()

                if st.session_state.get(f"editing_{product['id']}", False):
                    with st.form(f"edit_form_{product['id']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_name = st.text_input("Name", value=product['name'])
                            new_quantity = st.number_input("Quantity", value=product['quantity'], min_value=0)
                            new_price = st.number_input("Price", value=product['price'], min_value=0.01, step=0.01)
                        with col2:
                            new_reorder = st.number_input("Reorder Level", value=product['reorder_level'], min_value=0)
                            new_max = st.number_input("Max Stock", value=product['max_stock'], min_value=1)

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Save Changes", use_container_width=True):
                                result = api_request(
                                    "PUT",
                                    f"/products/{product['id']}",
                                    payload={
                                        "name": new_name,
                                        "quantity": int(new_quantity),
                                        "price": float(new_price),
                                        "reorder_level": int(new_reorder),
                                        "max_stock": int(new_max),
                                        "category": product['category'],
                                    },
                                    show_errors=True,
                                )
                                if result is not None:
                                    refresh_backend_data(show_errors=False)
                                    st.session_state[f"editing_{product['id']}"] = False
                                    st.rerun()
                        with col2:
                            if st.form_submit_button("Cancel", use_container_width=True):
                                st.session_state[f"editing_{product['id']}"] = False
                                st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

# Sales page
def sales_page():
    st.markdown("## 💰 Sales Tracking")
    st.caption("Record transactions and update inventory instantly.")

    # Record new sale
    with st.expander("➕ Record New Sale", expanded=False):
        if not st.session_state.products:
            st.info("Add products first, then record sales.")
            return
        with st.form("new_sale_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                product_names = [p['name'] for p in st.session_state.products]
                selected_product = st.selectbox("Product", product_names)
            with col2:
                sale_quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
            with col3:
                sale_date = st.date_input("Date", value=datetime.now())

            submit = st.form_submit_button("Record Sale", use_container_width=True)

            if submit and selected_product:
                # Get product price
                product = next((p for p in st.session_state.products if p['name'] == selected_product), None)
                if product:
                    result = api_request(
                        "POST",
                        "/sales/",
                        payload={
                            "product_id": product["id"],
                            "quantity": int(sale_quantity),
                            "sale_date": sale_date.strftime("%Y-%m-%d"),
                        },
                        show_errors=True,
                    )
                    if result is not None:
                        refresh_backend_data(show_errors=False)
                        st.success(f"Sale recorded: {sale_quantity}x {selected_product}")
                        st.rerun()

def reports_page():
    st.markdown("## 📑 Monthly Sales Reports")
    st.caption("Filter by year and month to analyze performance.")

    sales = st.session_state.sales
    sales_df = pd.DataFrame(sales)

    if sales_df.empty:
        st.info("No sales data available")
        return

    # Safe date conversion
    if 'date' not in sales_df.columns:
        st.error("Date column missing in sales data")
        return

    sales_df['date'] = pd.to_datetime(sales_df['date'], errors='coerce')
    sales_df = sales_df.dropna(subset=['date'])

    if sales_df.empty:
        st.warning("No valid date records found")
        return

    sales_df['Year'] = sales_df['date'].dt.year
    sales_df['Month'] = sales_df['date'].dt.month_name()

    # Year & Month Selection
    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox(
            "Select Year",
            sorted(sales_df['Year'].unique(), reverse=True)
        )

    with col2:
        months_order = ["January","February","March","April","May","June",
                        "July","August","September","October","November","December"]

        available_months = sales_df[sales_df['Year'] == selected_year]['Month'].unique()
        ordered_months = [m for m in months_order if m in available_months]

        if not ordered_months:
            st.warning("No sales found for selected year")
            return

        selected_month = st.selectbox("Select Month", ordered_months)

    # Filter Data
    filtered_df = sales_df[
        (sales_df['Year'] == selected_year) &
        (sales_df['Month'] == selected_month)
    ]

    if filtered_df.empty:
        st.warning("No sales found for selected month.")
        return

    # Metrics
    col1, col2, col3 = st.columns(3)

    total_revenue = filtered_df['total'].sum()
    total_items = filtered_df['quantity'].sum()
    avg_sale = total_revenue / len(filtered_df) if len(filtered_df) > 0 else 0

    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Items Sold", total_items)
    col3.metric("Avg. Sale Value", f"${avg_sale:,.2f}")

    # Sales Over Time Chart
    st.markdown("### 📈 Sales Over Time")

    daily = filtered_df.groupby(filtered_df['date'].dt.date)['total'].sum().reset_index()
    daily.columns = ['Date', 'Revenue']

    fig = px.area(daily, x='Date', y='Revenue')
    fig.update_layout(height=300, template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True, key="reports_sales_over_time")

    # Top Products Chart
    st.markdown("### 🏆 Top Selling Products")

    top_products = filtered_df.groupby('product')['quantity'].sum().sort_values(ascending=False).reset_index()

    fig2 = px.pie(top_products, values='quantity', names='product', hole=0.4)
    fig2.update_layout(height=300, template="plotly_dark")

    st.plotly_chart(fig2, use_container_width=True, key="reports_top_selling_products")

    # Sales Table
    st.markdown("### 📋 Sales Details")

    display_df = filtered_df[['date', 'product', 'quantity', 'total']]
    display_df.columns = ['Date', 'Product', 'Quantity', 'Total ($)']

    st.dataframe(
        display_df.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# Alerts page
def alerts_page():
    st.markdown("## ⚠️ Inventory Alerts")
    st.caption("Priority actions based on current stock and sales velocity.")

    products = st.session_state.products

    # Low stock alerts
    st.markdown("### 🔴 Low Stock Alerts")
    low_stock = [p for p in products if p['quantity'] <= p['reorder_level']]

    if low_stock:
        for product in low_stock:
            st.markdown(f"""
            <div class="alert-card">
                <strong>{product['name']}</strong> (SKU: {product['sku']})<br>
                Current: <strong>{product['quantity']}</strong> | Reorder Level: {product['reorder_level']}<br>
                <em>⚠️ Restock needed - {product['reorder_level'] - product['quantity']} units below threshold</em>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-card">✅ No low stock items</div>', unsafe_allow_html=True)

    # Overstock alerts
    st.markdown("### 🟡 Overstock Alerts")
    overstocked = [p for p in products if p['quantity'] > p['max_stock']]

    if overstocked:
        for product in overstocked:
            excess = product['quantity'] - product['max_stock']
            st.markdown(f"""
            <div class="overstock-card">
                <strong>{product['name']}</strong> (SKU: {product['sku']})<br>
                Current: <strong>{product['quantity']}</strong> | Max Level: {product['max_stock']}<br>
                <em>📦 Overstocked by {excess} units - Consider promotions or redistribution</em>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-card">✅ No overstocked items</div>', unsafe_allow_html=True)

    # Inventory prediction / recommendations
    st.markdown("### 🔮 Inventory Predictions")

    sales = st.session_state.sales
    sales_df = pd.DataFrame(sales)

    # Calculate average daily sales per product
    if sales_df.empty or 'date' not in sales_df.columns:
        st.info("Add sales data to generate predictions.")
        return
    sales_df['date'] = pd.to_datetime(sales_df['date'], errors='coerce')
    sales_df = sales_df.dropna(subset=['date'])
    if sales_df.empty:
        st.info("Add valid sales dates to generate predictions.")
        return
    days_range = (sales_df['date'].max() - sales_df['date'].min()).days + 1

    product_sales = sales_df.groupby('product')['quantity'].sum()

    for product in products:
        avg_daily = product_sales.get(product['name'], 0) / max(days_range, 1)
        if avg_daily > 0:
            days_until_reorder = (product['quantity'] - product['reorder_level']) / avg_daily

            if days_until_reorder < 7 and days_until_reorder > 0:
                st.warning(f"**{product['name']}**: At current sales rate, will need reorder in ~{int(days_until_reorder)} days")
            elif days_until_reorder < 0:
                st.error(f"**{product['name']}**: Already below reorder level!")

# Main app
def main():
    init_session_state()

    if not st.session_state.authenticated:
        login_page()
    else:
        header_bar()
        tab_labels = ["📊 Dashboard", "📦 Products", "💰 Sales", "📑 Reports", "⚠️ Alerts"]
        tabs = st.tabs(tab_labels)
        with tabs[0]:
            dashboard_page()
        with tabs[1]:
            products_page()
        with tabs[2]:
            sales_page()
        with tabs[3]:
            reports_page()
        with tabs[4]:
            alerts_page()
    st.markdown(
        '<p class="copyright" style="text-align:center; margin-top: 18px; color: #9aa4b2;">'
        '&copy;Small Inventory Prediction Website | All Rights Reserved | Creted By CodeGenZ BY AK 2026'
        '</p>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()

