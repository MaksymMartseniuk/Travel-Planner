# Travel Planner API

A robust RESTful API built with **Django REST Framework (DRF)** to help travelers plan trips, manage projects, and collect desired places to visit. Integrated with the public **Art Institute of Chicago API** for real-time place validation.

## Tech Stack
- **Framework:** Python 3.14.5, Django 5.2+, Django REST Framework (DRF)
- **Database:** MySQL 8.0
- **Integrations:** `requests` for Art Institute API
- **Tooling:** Docker, Docker Compose, Swagger UI (`drf-spectacular`)

Swagger UI: [http://localhost:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/#/)

## Quick Setup (Docker - Recommended)
The easiest way to run this application is via Docker

**1. Clone the repository**
```bash
python manage.py runverver
