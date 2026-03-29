# OnlineStore

A backend project built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

## Project Summary

- Backend API with a layered structure: API routes, use cases, repositories, and database models.
- User flow: registration, login, JWT-based authentication, and a profile endpoint (`/me`).
- Item flow: create, list, retrieve, update, and delete items for authenticated users.

## Architecture

The project is built using a **layered architecture** with elements of **DDD (Domain-Driven Design)**.

### What DDD means in this project

DDD is an approach to software design where the application is built around the **domain** and **business rules**, rather than around routes and SQL queries.

In this project, DDD ideas are reflected in the separation of responsibilities between layers:

- Domain logic is not mixed directly into route handlers.
- Use cases describe the actions the system performs.
- Repositories isolate database access.
- The API acts as a thin delivery layer.
- Models / entities describe the core objects of the system.

## Stack

- **Backend:** FastAPI, Pydantic, SQLAlchemy (`async`), Dependency Injector, PyJWT (`JWT`)
- **Database:** PostgreSQL (`Docker-ready Compose configuration`)
- **Testing:** Pytest (`pytest_asyncio`, `httpx`, `asgi_lifespan`)

## Main API Endpoints

### Auth / Users
- `POST /api/v1/users/auth/register`
- `POST /api/v1/users/auth/login`
- `GET /api/v1/users/auth/me`
- `GET /api/v1/users/auth/refresh`

### Items
- `POST /api/v1/users/items`
- `GET /api/v1/users/items`
- `GET /api/v1/users/items/{item_id}`
- `PUT /api/v1/users/items/{item_id}`
- `DELETE /api/v1/users/items/{item_id}`


## How to Run (quick)
1. Start PostgreSQL via:
```bash
build/docker-compose.yaml
```
2. Install Python dependencies from requirements:
```bash 
build/requirements.txt
```
3. Run app:
```bash
$ uvicorn src.main:main --host 0.0.0.0 --port 8080 --reload
```
4. Open:
```bash 
http://localhost:8080
```
5. (Optional) Run the tests: 
```bash
$ PYTHONPATH=. pytest
```
