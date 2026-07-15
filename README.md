# goods_dash

A demo marketplace analytics platform: a **FastAPI** backend serving a fully
async REST API over PostgreSQL, paired with a **Streamlit** dashboard for
browsing users/orders/products and visualizing sales analytics with Plotly.

All data is synthetic, generated with [Faker](https://faker.readthedocs.io/)
— this is a portfolio/demo project, not a production system.

## Stack

- **Backend:** FastAPI, SQLAlchemy 2.0 (async), PostgreSQL (`asyncpg`), Alembic, Pydantic v2
- **Frontend:** Streamlit, Plotly, httpx, pandas
- **Tooling:** [uv](https://docs.astral.sh/uv/) for dependency management

## Repository structure

```
goods_dash/
├── backend/
│   ├── main.py                 # FastAPI app entrypoint (mounts API at /api/v1)
│   ├── pyproject.toml           # all deps for backend + frontend live here
│   ├── alembic/                 # DB migrations
│   ├── seed/                    # Faker-based seed data generators
│   └── src/
│       ├── core/                 # settings, constants
│       ├── db/                    # engine/session/init
│       ├── models/                 # SQLAlchemy models (User, Product, Order, OrderItem)
│       ├── schemes/                 # Pydantic request/response + filter schemas
│       ├── repositories/             # query layer
│       ├── services/                  # business logic layer
│       ├── routers/                    # FastAPI routers
│       └── dependencies/                # DI wiring
└── frontend/
    ├── app.py                   # Streamlit entrypoint (st.navigation shell)
    ├── components/                # header/footer/sidebar/KPI cards/pagination
    ├── pages/                       # Dashboard, Users, Orders, Products, Analytics
    └── utils/                         # API client, formatting, session-state helpers
```

The layered backend architecture is: **models → repositories → services → routers**.

## Features

### Users, Orders, Products
- Paginated, filterable, sortable tables
- Click a row to view full details (a user's order history, an order's
  nested items/products, a product's computed stats)

### Analytics
- Revenue and new-user trends by month
- Orders by status / country
- Top products, category sales, payment method split
- Weekday × hour revenue heatmap

## API

All routes are mounted under `/api/v1`. Interactive docs are available at
`/docs` once the server is running.

| Resource | Endpoint | Notes |
|---|---|---|
| Dashboard | `GET /dashboard/` | KPI summary |
| Users | `GET /users/` | `country`, `vip`, `created_after`, `created_before`, `search`, `sort`, `order`, `page`, `page_size` |
| Users | `GET /users/countries` | distinct countries, for filter dropdowns |
| Users | `GET /users/{user_id}` | user detail + recent orders |
| Orders | `GET /orders/` | `status`, `country`, `vip`, `payment`, `date_from`, `date_to`, `search`, `sort`, `order`, `page`, `page_size` |
| Orders | `GET /orders/{order_id}` | order → user → items → products |
| Products | `GET /products/` | `category`, `in_stock`, `min_price`, `max_price`, `search`, `sort`, `order`, `page`, `page_size` |
| Products | `GET /products/categories` | distinct categories, for filter dropdowns |
| Products | `GET /products/{product_id}` | product detail with computed stats |
| Analytics | `GET /analytics/revenue/monthly` | line chart |
| Analytics | `GET /analytics/orders/status` | pie chart |
| Analytics | `GET /analytics/orders/country` | horizontal bar chart |
| Analytics | `GET /analytics/users/monthly` | line chart |
| Analytics | `GET /analytics/top-products` | bar chart, `?limit=` |
| Analytics | `GET /analytics/category-sales` | pie chart |
| Analytics | `GET /analytics/payment-methods` | donut chart |
| Analytics | `GET /analytics/revenue/heatmap` | weekday × hour grid |

## Setup

### Prerequisites
- Python 3.14+
- PostgreSQL running locally (or reachable via connection string)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### 1. Clone and install

```bash
git clone https://github.com/Proxima5559/goods_dash.git
cd goods_dash/backend
uv sync
```

This installs both backend and frontend dependencies — they share one
`pyproject.toml`/environment.


### 2. Run migrations

```bash
cd backend
uv run alembic upgrade head
```

### 3. Seed demo data

```bash
uv run python -m seed.seed
```

Re-running this clears and regenerates all users/products/orders.

### 4. Start the backend

```bash
uv run python main.py
# or: uv run uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 5. Start the frontend

In a second terminal, from `backend/` (same environment):

```bash
uv run streamlit run ../frontend/app.py
```

By default the frontend points at `http://127.0.0.1:8000`. Override with:

```bash
BACKEND_URL=http://localhost:8000 uv run streamlit run ../frontend/app.py
```

Dashboard: http://localhost:8501

## Environment variables

| Variable | Used by | Description |
|---|---|---|
| `DATABASE_URL` | backend | SQLAlchemy async connection string (`postgresql+asyncpg://...`) |
| `ORIGIN_ALLOWED` | backend | Comma-separated list of allowed CORS origins |
| `PORT` | backend | Port for `main.py`'s built-in uvicorn runner |
| `BACKEND_URL` | frontend | Base URL of the FastAPI server (defaults to `http://127.0.0.1:8000`) |
