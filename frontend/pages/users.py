import pandas as pd
import streamlit as st

from components.footer import render_footer
from components.header import render_header
from components.pagination import render_pagination
from utils.api_client import get_user, get_user_countries, get_users
from utils.formatting import fmt_date, fmt_money, status_badge
from utils.state import clear_selection, get_page, get_selected, select_row, sync_filters_and_maybe_reset_page

NAMESPACE = "users"

render_header("Users", "Browse and filter marketplace customers")

selected_id = get_selected(NAMESPACE)

# ------------------------------------------------------------------- Detail

if selected_id:
    if st.button("← Back to list"):
        clear_selection(NAMESPACE)
        st.rerun()

    user = get_user(selected_id)
    if user is None:
        st.stop()

    st.subheader(user["name"])
    st.caption(user["email"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Orders", user["orders_count"])
    c2.metric("Total Spent", fmt_money(user["total_spent"]))
    c3.metric("Avg Order", fmt_money(user["average_order"]))
    c4.metric("VIP", "Yes" if user["vip"] else "No")

    st.markdown(
        f"**Location:** {user['city']}, {user['country']}  \n"
        f"**Customer since:** {fmt_date(user['created_at'])}"
    )

    st.markdown("#### Recent orders")
    orders = user.get("orders") or []
    if orders:
        df = pd.DataFrame(orders)
        df["status"] = df["status"].apply(status_badge)
        df["total"] = df["total"].apply(fmt_money)
        df["created_at"] = df["created_at"].apply(fmt_date)
        st.dataframe(
            df[["created_at", "status", "payment_method", "total"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "created_at": "Date",
                "status": "Status",
                "payment_method": "Payment",
                "total": "Total",
            },
        )
    else:
        st.caption("No orders yet.")

    render_footer()
    st.stop()

# -------------------------------------------------------------------- List

countries = get_user_countries()

with st.expander("Filters", expanded=True):
    f1, f2, f3 = st.columns(3)
    with f1:
        search = st.text_input("Search (name or email)", key=f"{NAMESPACE}_search")
    with f2:
        country = st.selectbox("Country", ["Any"] + countries, key=f"{NAMESPACE}_country")
        country = None if country == "Any" else country
    with f3:
        vip_choice = st.selectbox("VIP status", ["Any", "VIP only", "Regular only"], key=f"{NAMESPACE}_vip")
        vip = {"Any": None, "VIP only": True, "Regular only": False}[vip_choice]

    f4, f5, f6, f7 = st.columns(4)
    with f4:
        created_after = st.date_input("Created after", value=None, key=f"{NAMESPACE}_after")
    with f5:
        created_before = st.date_input("Created before", value=None, key=f"{NAMESPACE}_before")
    with f6:
        sort = st.selectbox(
            "Sort by",
            ["created_at", "name", "email", "country", "orders_count", "total_spent"],
            key=f"{NAMESPACE}_sort",
        )
    with f7:
        order = st.selectbox("Order", ["desc", "asc"], key=f"{NAMESPACE}_order")

sync_filters_and_maybe_reset_page(
    NAMESPACE,
    (search, country, vip, str(created_after), str(created_before), sort, order),
)

page = get_page(NAMESPACE)

result = get_users(
    page=page,
    page_size=20,
    country=country,
    vip=vip,
    created_after=created_after.isoformat() if created_after else None,
    created_before=created_before.isoformat() if created_before else None,
    search=search or None,
    sort=sort,
    order=order,
)

if result is None:
    st.stop()

items = result["items"]

if not items:
    st.info("No users match these filters.")
    render_footer()
    st.stop()

df = pd.DataFrame(items)
df["total_spent"] = df["total_spent"].apply(fmt_money)
df["created_at"] = df["created_at"].apply(fmt_date)
df["vip"] = df["vip"].apply(lambda v: "⭐ VIP" if v else "")

display_cols = ["name", "email", "country", "vip", "orders_count", "total_spent", "created_at"]

event = st.dataframe(
    df[display_cols],
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "name": "Name",
        "email": "Email",
        "country": "Country",
        "vip": "",
        "orders_count": "Orders",
        "total_spent": "Total Spent",
        "created_at": "Joined",
    },
)

st.caption("Click a row to view customer details.")

if event.selection.rows:
    row_index = event.selection.rows[0]
    select_row(NAMESPACE, items[row_index]["id"])
    st.rerun()

render_pagination(NAMESPACE, result["meta"])
render_footer()
