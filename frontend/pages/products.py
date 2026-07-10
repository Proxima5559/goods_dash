import pandas as pd
import streamlit as st

from components.footer import render_footer
from components.header import render_header
from components.pagination import render_pagination
from utils.api_client import get_product, get_product_categories, get_products
from utils.formatting import fmt_money
from utils.state import clear_selection, get_page, get_selected, select_row, sync_filters_and_maybe_reset_page

NAMESPACE = "products"

render_header("Products", "Browse and filter the product catalog")

selected_id = get_selected(NAMESPACE)

# ------------------------------------------------------------------- Detail

if selected_id:
    if st.button("← Back to list"):
        clear_selection(NAMESPACE)
        st.rerun()

    product = get_product(selected_id)
    if product is None:
        st.stop()

    st.subheader(product["name"])
    st.caption(product["category"])

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Price", fmt_money(product["price"]))
    c2.metric("Rating", f"{float(product['rating']):.1f} ⭐")
    c3.metric("Remaining Stock", product["remaining_stock"])
    c4.metric("Orders", product["orders_count"])
    c5.metric("Revenue Generated", fmt_money(product["revenue_generated"]))

    if product["remaining_stock"] < 10:
        st.warning("⚠️ Low stock — fewer than 10 units remaining.")

    render_footer()
    st.stop()

# -------------------------------------------------------------------- List

categories = get_product_categories()

with st.expander("Filters", expanded=True):
    f1, f2, f3 = st.columns(3)
    with f1:
        search = st.text_input("Search by name", key=f"{NAMESPACE}_search")
    with f2:
        category_choice = st.selectbox("Category", ["Any"] + categories, key=f"{NAMESPACE}_category")
        category = None if category_choice == "Any" else category_choice
    with f3:
        stock_choice = st.selectbox("Stock", ["Any", "In stock", "Out of stock"], key=f"{NAMESPACE}_stock")
        in_stock = {"Any": None, "In stock": True, "Out of stock": False}[stock_choice]

    f4, f5, f6, f7 = st.columns(4)
    with f4:
        min_price = st.number_input("Min price", min_value=0.0, value=0.0, step=1.0, key=f"{NAMESPACE}_min_price")
    with f5:
        max_price = st.number_input("Max price", min_value=0.0, value=0.0, step=1.0, key=f"{NAMESPACE}_max_price")
    with f6:
        sort = st.selectbox("Sort by", ["name", "category", "price", "rating", "stock"], key=f"{NAMESPACE}_sort")
    with f7:
        order = st.selectbox("Order", ["asc", "desc"], key=f"{NAMESPACE}_order")

sync_filters_and_maybe_reset_page(
    NAMESPACE,
    (search, category, in_stock, min_price, max_price, sort, order),
)

page = get_page(NAMESPACE)

result = get_products(
    page=page,
    page_size=20,
    category=category,
    in_stock=in_stock,
    min_price=min_price if min_price > 0 else None,
    max_price=max_price if max_price > 0 else None,
    search=search or None,
    sort=sort,
    order=order,
)

if result is None:
    st.stop()

items = result["items"]

if not items:
    st.info("No products match these filters.")
    render_footer()
    st.stop()

df = pd.DataFrame(items)
df["price"] = df["price"].apply(fmt_money)
df["stock_flag"] = df["stock"].apply(lambda s: "⚠️ Low" if s < 10 else "")

display_cols = ["name", "category", "price", "rating", "stock", "stock_flag"]

event = st.dataframe(
    df[display_cols],
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "name": "Name",
        "category": "Category",
        "price": "Price",
        "rating": st.column_config.NumberColumn("Rating", format="%.1f ⭐"),
        "stock": "Stock",
        "stock_flag": "",
    },
)

st.caption("Click a row to view product details.")

if event.selection.rows:
    row_index = event.selection.rows[0]
    select_row(NAMESPACE, items[row_index]["id"])
    st.rerun()

render_pagination(NAMESPACE, result["meta"])
render_footer()
