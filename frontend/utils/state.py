import streamlit as st


def get_selected(namespace: str) -> str | None:
    return st.session_state.get(f"{namespace}_selected_id")


def select_row(namespace: str, row_id: str) -> None:
    st.session_state[f"{namespace}_selected_id"] = row_id


def clear_selection(namespace: str) -> None:
    st.session_state[f"{namespace}_selected_id"] = None


def get_page(namespace: str) -> int:
    return st.session_state.get(f"{namespace}_page", 1)


def set_page(namespace: str, page: int) -> None:
    st.session_state[f"{namespace}_page"] = page


def sync_filters_and_maybe_reset_page(namespace: str, filters: tuple) -> None:
    key = f"{namespace}_filters_signature"
    if st.session_state.get(key) != filters:
        st.session_state[key] = filters
        set_page(namespace, 1)
