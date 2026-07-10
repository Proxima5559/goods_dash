import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.footer import render_footer
from components.header import render_header
from utils.api_client import (
    get_category_sales,
    get_monthly_registrations,
    get_monthly_revenue,
    get_orders_by_country,
    get_orders_by_status,
    get_payment_method_stats,
    get_revenue_heatmap,
    get_top_products,
)
from utils.formatting import WEEKDAY_LABELS, fmt_label

render_header("Analytics", "Trends, breakdowns, and sales patterns across the marketplace")

# ---------------------------------------------------------- Revenue & users

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Revenue by month")
    data = get_monthly_revenue()
    if data:
        fig = px.line(data, x="month", y="revenue", markers=True)
        fig.update_layout(xaxis_title=None, yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No data.")

with col2:
    st.markdown("#### New users by month")
    data = get_monthly_registrations()
    if data:
        fig = px.line(data, x="month", y="users", markers=True, color_discrete_sequence=["#2ca02c"])
        fig.update_layout(xaxis_title=None, yaxis_title="New users")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No data.")

st.divider()

# --------------------------------------------------------------- Breakdowns

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("#### Orders by status")
    data = get_orders_by_status()
    if data:
        for row in data:
            row["label"] = fmt_label(row["status"])
        fig = px.pie(data, names="label", values="count", hole=0.35)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No data.")

with col4:
    st.markdown("#### Sales by category")
    data = get_category_sales()
    if data:
        fig = px.pie(data, names="category", values="revenue")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No data.")

with col5:
    st.markdown("#### Payment methods")
    data = get_payment_method_stats()
    if data:
        for row in data:
            row["label"] = fmt_label(row["payment_method"])
        fig = px.pie(data, names="label", values="count", hole=0.5)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No data.")

st.divider()

# ------------------------------------------------------------- Country/top

col6, col7 = st.columns(2)

with col6:
    st.markdown("#### Orders by country")
    data = get_orders_by_country()
    if data:
        df = pd.DataFrame(data).sort_values("orders")
        fig = px.bar(df, x="orders", y="country", orientation="h")
        fig.update_layout(yaxis_title=None, xaxis_title="Orders")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No data.")

with col7:
    st.markdown("#### Top products by revenue")
    limit = st.slider("Number of products", min_value=5, max_value=50, value=10, step=5)
    data = get_top_products(limit=limit)
    if data:
        df = pd.DataFrame(data).sort_values("revenue")
        fig = px.bar(df, x="revenue", y="name", orientation="h", hover_data=["category", "units_sold"])
        fig.update_layout(yaxis_title=None, xaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No data.")

st.divider()

# ------------------------------------------------------------------ Heatmap

st.markdown("#### Revenue heatmap — day of week × hour")
data = get_revenue_heatmap()
if data:
    df = pd.DataFrame(data)
    pivot = df.pivot(index="weekday", columns="hour", values="revenue").reindex(index=range(7), columns=range(24), fill_value=0)
    counts_pivot = df.pivot(index="weekday", columns="hour", values="orders_count").reindex(index=range(7), columns=range(24), fill_value=0)

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=[f"{h:02d}:00" for h in pivot.columns],
            y=[WEEKDAY_LABELS[i] for i in pivot.index],
            colorscale="YlOrRd",
            customdata=counts_pivot.values,
            hovertemplate="%{y} %{x}<br>Revenue: $%{z:,.2f}<br>Orders: %{customdata}<extra></extra>",
        )
    )
    fig.update_layout(xaxis_title="Hour of day", yaxis_title=None, height=400)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.caption("No data.")

render_footer()
