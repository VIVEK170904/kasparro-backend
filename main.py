from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import os
import time
import uvicorn

app = FastAPI(title="Kasparro Backend API")

# ------------------
# DB Connection
# ------------------

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )

# ------------------
# Response Schemas
# ------------------

class HealthResponse(BaseModel):
    db: str
    etl_last_run: str

class Item(BaseModel):
    id: int
    name: str
    price: float

class DataResponse(BaseModel):
    data: List[Item]
    request_id: str
    api_latency_ms: int
    limit: int
    offset: int
    total: int

class StatsResponse(BaseModel):
    total_items: int
    average_price: Optional[float]
    min_price: Optional[float]
    max_price: Optional[float]

# ------------------
# Routes
# ------------------

@app.get("/health", response_model=HealthResponse)
def health():
    return {
        "db": "connected",
        "etl_last_run": "success"
    }

# ------------------
# Data Endpoint (Pagination)
# ------------------

@app.get("/data", response_model=DataResponse)
def get_data(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    start = time.time()

    conn = get_db_connection()
    cur = conn.cursor()

    # Total count (READ ONLY)
    cur.execute("SELECT COUNT(*) FROM items;")
    total = cur.fetchone()[0]

    # Paginated query (READ ONLY)
    cur.execute(
        """
        SELECT id, name, price
        FROM items
        ORDER BY id
        LIMIT %s OFFSET %s;
        """,
        (limit, offset)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    items = [
        Item(
            id=row[0],
            name=row[1],
            price=float(row[2])
        )
        for row in rows
    ]

    latency = int((time.time() - start) * 1000)

    return {
        "data": items,
        "request_id": "local",
        "api_latency_ms": latency,
        "limit": limit,
        "offset": offset,
        "total": total
    }

# ------------------
# Stats Endpoint (Aggregation + Filtering)
# ------------------

@app.get("/stats", response_model=StatsResponse)
def get_stats(
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0)
):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT
            COUNT(*) AS total_items,
            AVG(price) AS average_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price
        FROM items
        WHERE 1=1
    """

    params = []

    if min_price is not None:
        query += " AND price >= %s"
        params.append(min_price)

    if max_price is not None:
        query += " AND price <= %s"
        params.append(max_price)

    cur.execute(query, params)
    total, avg_price, min_p, max_p = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_items": total,
        "average_price": float(avg_price) if avg_price is not None else None,
        "min_price": float(min_p) if min_p is not None else None,
        "max_price": float(max_p) if max_p is not None else None,
    }

# ------------------
# App Runner
# ------------------

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000
    )
