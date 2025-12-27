Kasparro Backend API

A production-ready FastAPI + PostgreSQL + Docker backend with pagination, filtering, aggregation, ETL readiness, and clean API documentation.

 Features

.FastAPI REST API

.PostgreSQL database (Dockerized)

.Health check endpoint

.Paginated data retrieval

.Price filtering (min / max)

.Aggregation stats endpoint

.Swagger (OpenAPI) documentation

.Environment-based configuration

.Docker & Docker Compose setup

.Ready for ETL ingestion & testing

🏗️ Tech Stack

Backend: FastAPI (Python)

Database: PostgreSQL 15

ORM/Driver: psycopg2

Containerization: Docker, Docker Compose

Docs: Swagger UI (OpenAPI)

📁 Project Structure
kasparro-backend/
│
├── main.py                 # FastAPI application
├── etl.py                  # ETL ingestion script (CSV → DB)
├── requirements.txt        # Python dependencies
├── Dockerfile              # App container
├── docker-compose.yml      # App + Postgres
├── .env                    # Environment variables
├── README.md               # Project documentation
└── tests/                  # Pytest test cases (optional)

⚙️ Environment Variables (.env)
POSTGRES_DB=kasparro
POSTGRES_USER=kasparro_user
POSTGRES_PASSWORD=kasparro_pass
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

🐳 Run with Docker
Start services
docker compose up --build

Stop services
docker compose down

🌐 API Documentation (Swagger)

Once running, open:

http://localhost:8000/docs

🔌 API Endpoints
✅ Health Check
GET /health


Response

{
  "db": "connected",
  "etl_last_run": "success"
}

📦 Get Items (Pagination + Filtering)
GET /data


Query Params

Param	Type	Description
limit	int	Max rows (1–100)
offset	int	Pagination offset
min_price	float	Filter minimum price
max_price	float	Filter maximum price

Example

/data?limit=10&offset=0&min_price=2000&max_price=50000

--Stats Endpoint
GET /stats


Response

{
  "total_items": 3,
  "average_price": 35666.67,
  "min_price": 2000,
  "max_price": 75000
}

--Testing (Optional)

Install dependencies locally:

pip install pytest httpx


Run tests:

pytest

--ETL Ingestion

ETL script can ingest CSV or external data into PostgreSQL.

Run inside container:

docker exec -it kasparro-app python etl.py

--Best Practices Used

Read-only SELECT queries

Environment-based secrets

Parameterized SQL (safe)

Response validation with Pydantic

Docker-first workflow

--Future Enhancements

Background ETL jobs

CSV upload API

Authentication (JWT)

Alembic migrations

CI/CD pipeline

Caching (Redis)

