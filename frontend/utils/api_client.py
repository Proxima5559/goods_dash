import os

import httpx
from dotenv import load_dotenv
import streamlit as st
load_dotenv() 
BASE_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

BACKEND_URL = f"{BASE_URL}/api/v1"

_client = httpx.Client(base_url=BACKEND_URL, timeout=10.0)


def _get(path: str, params: dict | None = None) -> dict | list | None:
    clean_params = {k: v for k, v in (params or {}).items() if v is not None}
    try:
        response = _client.get(path, params=clean_params)
        response.raise_for_status()
        return response.json()
    except httpx.ConnectError:
        st.error(
            f"Can't reach the backend at `{BACKEND_URL}`. "
            "Is the FastAPI server running? (`uvicorn src.main:app --reload`)"
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            st.warning("Not found.")
        else:
            st.error(f"Backend error {e.response.status_code}: {e.response.text}")
    except httpx.HTTPError as e:
        st.error(f"Request failed: {e}")
    return None


# ---------------------------------------------------------------- Dashboard

@st.cache_data(ttl=30)
def get_dashboard() -> dict | None:
    return _get("/dashboard/")


# --------------------------------------------------------------------- Users

@st.cache_data(ttl=30)
def get_users(
    page: int = 1,
    page_size: int = 20,
    country: str | None = None,
    vip: bool | None = None,
    created_after: str | None = None,
    created_before: str | None = None,
    search: str | None = None,
    sort: str = "created_at",
    order: str = "desc",
) -> dict | None:
    return _get(
        "/users/",
        {
            "page": page,
            "page_size": page_size,
            "country": country,
            "vip": vip,
            "created_after": created_after,
            "created_before": created_before,
            "search": search,
            "sort": sort,
            "order": order,
        },
    )


@st.cache_data(ttl=30)
def get_user(user_id: str) -> dict | None:
    return _get(f"/users/{user_id}")


@st.cache_data(ttl=300)
def get_user_countries() -> list[str]:
    return _get("/users/countries") or []


# -------------------------------------------------------------------- Orders

@st.cache_data(ttl=30)
def get_orders(
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    country: str | None = None,
    vip: bool | None = None,
    payment: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    search: str | None = None,
    sort: str = "created_at",
    order: str = "desc",
) -> dict | None:
    return _get(
        "/orders/",
        {
            "page": page,
            "page_size": page_size,
            "status": status,
            "country": country,
            "vip": vip,
            "payment": payment,
            "date_from": date_from,
            "date_to": date_to,
            "search": search,
            "sort": sort,
            "order": order,
        },
    )


@st.cache_data(ttl=30)
def get_order(order_id: str) -> dict | None:
    return _get(f"/orders/{order_id}")


# ------------------------------------------------------------------ Products

@st.cache_data(ttl=30)
def get_products(
    page: int = 1,
    page_size: int = 20,
    category: str | None = None,
    in_stock: bool | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    sort: str = "name",
    order: str = "asc",
) -> dict | None:
    return _get(
        "/products/",
        {
            "page": page,
            "page_size": page_size,
            "category": category,
            "in_stock": in_stock,
            "min_price": min_price,
            "max_price": max_price,
            "search": search,
            "sort": sort,
            "order": order,
        },
    )


@st.cache_data(ttl=30)
def get_product(product_id: str) -> dict | None:
    return _get(f"/products/{product_id}")


@st.cache_data(ttl=300)
def get_product_categories() -> list[str]:
    return _get("/products/categories") or []


# ---------------------------------------------------------------- Analytics

@st.cache_data(ttl=60)
def get_monthly_revenue() -> list | None:
    return _get("/analytics/revenue/monthly")


@st.cache_data(ttl=60)
def get_orders_by_status() -> list | None:
    return _get("/analytics/orders/status")


@st.cache_data(ttl=60)
def get_orders_by_country() -> list | None:
    return _get("/analytics/orders/country")


@st.cache_data(ttl=60)
def get_monthly_registrations() -> list | None:
    return _get("/analytics/users/monthly")


@st.cache_data(ttl=60)
def get_top_products(limit: int = 10) -> list | None:
    return _get("/analytics/top-products", {"limit": limit})


@st.cache_data(ttl=60)
def get_category_sales() -> list | None:
    return _get("/analytics/category-sales")


@st.cache_data(ttl=60)
def get_payment_method_stats() -> list | None:
    return _get("/analytics/payment-methods")


@st.cache_data(ttl=60)
def get_revenue_heatmap() -> list | None:
    return _get("/analytics/revenue/heatmap")
