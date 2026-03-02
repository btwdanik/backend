# Backend

A small backend-stack demo project built with **FastAPI**, **PostgreSQL**, and a **SQLAlchemy**.

## Project Summary
- Backend API with layered structure: API routes, use cases, repositories, and database models.
- User flow: registration, login, JWT token auth, and profile endpoint (`/me`).
- Item flow: create, list, read, update, and delete items for authenticated users.

## Stack
- **Backend:** FastAPI, Pydantic, SQLAlchemy (async), Dependency Injector.
- **Database:** PostgreSQL (Docker-ready compose config).

## Main API Endpoints
- `POST /api/v1/users/auth/register`
- `POST /api/v1/users/auth/login`
- `GET /api/v1/users/auth/me`
- `GET /api/v1/users/auth/refresh`
- `POST /api/v1/users/items`
- `GET /api/v1/users/items`
- `GET /api/v1/users/items/{item_id}`
- `PUT /api/v1/users/items/{item_id}`
- `DELETE /api/v1/users/items/{item_id}`

## How to Run (quick)
1. Start PostgreSQL via `build/docker-compose.yaml`.
2. Install Python dependencies from `build/requirements.txt`.
3. Run app: `uvicorn main:main --host 0.0.0.0 --port 8080 --reload`.
4. Open `http://localhost:8080`.
