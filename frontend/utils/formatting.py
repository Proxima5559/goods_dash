from datetime import datetime


def fmt_money(value) -> str:
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return "$0.00"


def fmt_date(value: str | None, with_time: bool = False) -> str:
    if not value:
        return "—"
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return dt.strftime("%b %d, %Y %H:%M") if with_time else dt.strftime("%b %d, %Y")


def fmt_label(value: str) -> str:
    return value.replace("_", " ").title()


STATUS_COLORS = {
    "PENDING": "🟡",
    "PROCESSING": "🔵",
    "SHIPPED": "🟣",
    "DELIVERED": "🟢",
    "CANCELLED": "🔴",
}


def status_badge(status: str) -> str:
    icon = STATUS_COLORS.get(status, "⚪")
    return f"{icon} {fmt_label(status)}"


WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
