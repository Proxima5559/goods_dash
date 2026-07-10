import plotly.express as px
import streamlit as st

from components.footer import render_footer
from components.header import render_header
from components.kpi_card import render_kpi_row
from utils.api_client import get_dashboard, get_monthly_revenue, get_orders_by_status
from utils.formatting import fmt_label, fmt_money

render_header(
    "Marketplace Analytics",
    "Interactive dashboard built with FastAPI + Streamlit",
)

dashboard = get_dashboard()

if dashboard is None:
    st.stop()

render_kpi_row(
    [
        ("Total Users", f"{dashboard['total_users']:,}", None),
        ("VIP Users", f"{dashboard['vip_users']:,}", "Users flagged as VIP"),
        ("Total Orders", f"{dashboard['total_orders']:,}", None),
        ("Total Revenue", fmt_money(dashboard["total_revenue"]), None),
    ]
)

render_kpi_row(
    [
        ("Avg Order Value", fmt_money(dashboard["average_order_value"]), None),
        ("Total Products", f"{dashboard['total_products']:,}", None),
        (
            "Low Stock Products",
            f"{dashboard['low_stock_products']:,}",
            "Products with fewer than 10 units left",
        ),
        (
            "VIP Share",
            f"{(dashboard['vip_users'] / dashboard['total_users'] * 100):.1f}%"
            if dashboard["total_users"]
            else "0%",
            None,
        ),
    ]
)

st.markdown("")
st.subheader("Quick stats")

col1, col2 = st.columns(2)

with col1:
    revenue_points = get_monthly_revenue()
    if revenue_points:
        fig = px.line(
            revenue_points,
            x="month",
            y="revenue",
            markers=True,
            title="Revenue by month",
        )
        fig.update_layout(yaxis_title="Revenue ($)", xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    status_points = get_orders_by_status()
    if status_points:
        for row in status_points:
            row["status_label"] = fmt_label(row["status"])
        fig = px.pie(
            status_points,
            names="status_label",
            values="count",
            title="Orders by status",
            hole=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
Welcome! This app demonstrates a marketplace analytics system backed by a
FastAPI service, with all data synthetically generated via Faker.

Use the navigation on the left to explore:

- 👥 **Users** — browse, filter, and drill into individual customers
- 📦 **Orders** — filter by status, country, payment method, or date range
- 🛒 **Products** — browse the catalog with stock and pricing filters
- 📈 **Analytics** — revenue trends, category breakdowns, and a sales heatmap
"""
)

render_footer()
