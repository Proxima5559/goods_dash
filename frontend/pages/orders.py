import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
    
import pandas as pd
import streamlit as st

from components.footer import render_footer
from components.header import render_header
from components.pagination import render_pagination
from utils.api_client import get_order, get_orders, get_user_countries
from utils.formatting import fmt_date, fmt_label, fmt_money, status_badge
from utils.state import clear_selection, get_page, get_selected, select_row, sync_filters_and_maybe_reset_page
from backend.src.models.order import OrderStatus, PaymentMethod


    
NAMESPACE = "orders"

ORDER_STATUSES = [status.value for status in OrderStatus]
PAYMENT_METHODS = [method.value for method in PaymentMethod]

render_header("Orders", "Browse and filter marketplace orders")

selected_id = get_selected(NAMESPACE)

# ------------------------------------------------------------------- Detail

if selected_id:
    if st.button("← Back to list"):
        clear_selection(NAMESPACE)
        st.rerun()

    order = get_order(selected_id)
    if order is None:
        st.stop()

    user = order["user"]

    st.subheader(f"Order #{order['id'][:8]}")
    st.markdown(status_badge(order["status"]))

    c1, c2, c3 = st.columns(3)
    c1.metric("Total", fmt_money(order["total"]))
    c2.metric("Payment", fmt_label(order["payment_method"]))
    c3.metric("Placed on", fmt_date(order["created_at"]))

    st.markdown("#### Customer")
    st.markdown(
        f"**{user['name']}** ({'⭐ VIP' if user['vip'] else 'Regular'})  \n"
        f"{user['email']}  \n"
        f"{user['country']}"
    )

    st.markdown("#### Timeline")
    t1, t2, t3 = st.columns(3)
    t1.markdown(f"**Created**  \n{fmt_date(order['created_at'], with_time=True)}")
    t2.markdown(f"**Shipped**  \n{fmt_date(order.get('shipped_at'), with_time=True)}")
    t3.markdown(f"**Delivered**  \n{fmt_date(order.get('delivered_at'), with_time=True)}")

    st.markdown("#### Items")
    items = order.get("items") or []
    if items:
        rows = [
            {
                "Product": item["product"]["name"],
                "Category": item["product"]["category"],
                "Quantity": item["quantity"],
                "Unit Price": fmt_money(item["price"]),
                "Subtotal": fmt_money(float(item["price"]) * item["quantity"]),
            }
            for item in items
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.caption("No items on this order.")

    render_footer()
    st.stop()

# -------------------------------------------------------------------- List

countries = get_user_countries()

with st.expander("Filters", expanded=True):
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        search = st.text_input("Search (customer name or email)", key=f"{NAMESPACE}_search")
    with f2:
        status_choice = st.selectbox("Status", ["Any"] + ORDER_STATUSES, key=f"{NAMESPACE}_status")
        status = None if status_choice == "Any" else status_choice
    with f3:
        country_choice = st.selectbox("Country", ["Any"] + countries, key=f"{NAMESPACE}_country")
        country = None if country_choice == "Any" else country_choice
    with f4:
        payment_choice = st.selectbox("Payment method", ["Any"] + PAYMENT_METHODS, key=f"{NAMESPACE}_payment")
        payment = None if payment_choice == "Any" else payment_choice

    f5, f6, f7, f8, f9 = st.columns(5)
    with f5:
        vip_choice = st.selectbox("Customer type", ["Any", "VIP only", "Regular only"], key=f"{NAMESPACE}_vip")
        vip = {"Any": None, "VIP only": True, "Regular only": False}[vip_choice]
    with f6:
        date_from = st.date_input("From date", value=None, key=f"{NAMESPACE}_from")
    with f7:
        date_to = st.date_input("To date", value=None, key=f"{NAMESPACE}_to")
    with f8:
        sort = st.selectbox(
            "Sort by", ["created_at", "total", "status", "shipped_at", "delivered_at"], key=f"{NAMESPACE}_sort"
        )
    with f9:
        order = st.selectbox("Order", ["desc", "asc"], key=f"{NAMESPACE}_order")

sync_filters_and_maybe_reset_page(
    NAMESPACE,
    (search, status, country, payment, vip, str(date_from), str(date_to), sort, order),
)

page = get_page(NAMESPACE)

result = get_orders(
    page=page,
    page_size=20,
    status=status,
    country=country,
    vip=vip,
    payment=payment,
    date_from=date_from.isoformat() if date_from else None,
    date_to=date_to.isoformat() if date_to else None,
    search=search or None,
    sort=sort,
    order=order,
)

if result is None:
    st.stop()

items = result["items"]

if not items:
    st.info("No orders match these filters.")
    render_footer()
    st.stop()

rows = []
for order_row in items:
    rows.append(
        {
            "id": order_row["id"],
            "customer": order_row["user"]["name"],
            "country": order_row["user"]["country"],
            "vip": "⭐" if order_row["user"]["vip"] else "",
            "status": status_badge(order_row["status"]),
            "payment_method": fmt_label(order_row["payment_method"]),
            "total": fmt_money(order_row["total"]),
            "created_at": fmt_date(order_row["created_at"]),
        }
    )

df = pd.DataFrame(rows)
display_cols = ["customer", "country", "vip", "status", "payment_method", "total", "created_at"]

event = st.dataframe(
    df[display_cols],
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "customer": "Customer",
        "country": "Country",
        "vip": "",
        "status": "Status",
        "payment_method": "Payment",
        "total": "Total",
        "created_at": "Date",
    },
)

st.caption("Click a row to view order details.")

if event.selection.rows:
    row_index = event.selection.rows[0]
    select_row(NAMESPACE, items[row_index]["id"])
    st.rerun()

render_pagination(NAMESPACE, result["meta"])
render_footer()
