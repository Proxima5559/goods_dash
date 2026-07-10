import streamlit as st

from components.header import render_header
from components.footer import render_footer
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Marketplace Analytics",
    page_icon="📊",
    layout="wide",
)

render_sidebar()

pages = [
    st.Page("pages/dashboard.py", title="Dashboard", icon="🏠", default=True),
    st.Page("pages/users.py", title="Users", icon="👥"),
    st.Page("pages/orders.py", title="Orders", icon="📦"),
    st.Page("pages/products.py", title="Products", icon="🛒"),
    st.Page("pages/analytics.py", title="Analytics", icon="📈"),
]

nav = st.navigation(pages)
nav.run()
