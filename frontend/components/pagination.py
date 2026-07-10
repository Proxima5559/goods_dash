import streamlit as st

from utils.state import get_page, set_page


def render_pagination(namespace: str, meta: dict) -> None:
    """meta is the `meta` block off a PaginatedResponse:
    {page, page_size, total_items, total_pages}"""
    page = meta["page"]
    total_pages = max(meta["total_pages"], 1)
    total_items = meta["total_items"]

    left, mid, right = st.columns([1, 2, 1])

    with left:
        if st.button("← Previous", disabled=page <= 1, use_container_width=True, key=f"{namespace}_prev"):
            set_page(namespace, page - 1)
            st.rerun()

    with mid:
        st.markdown(
            f"<div style='text-align:center; padding-top:0.4rem;'>"
            f"Page {page} of {total_pages} · {total_items} total</div>",
            unsafe_allow_html=True,
        )

    with right:
        if st.button("Next →", disabled=page >= total_pages, use_container_width=True, key=f"{namespace}_next"):
            set_page(namespace, page + 1)
            st.rerun()
