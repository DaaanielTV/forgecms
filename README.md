## Warranty & Liability
This software is provided "as is", without warranty of any kind. See the LICENSE file for the full GPL-3.0 disclaimer of warranty and limitation of liability.

I'm not responsible if this breaks your setup. Test it before using it in production.

# ForgeCMS

ForgeCMS is a Flask-based blogging and CMS application backed by MariaDB. It includes authentication, an admin workflow for draft/scheduled/published content, Markdown authoring, and media upload support.

## Overview

### What ForgeCMS provides
- User registration and login
- Admin content management experience
- Post workflow states (`draft`, `scheduled`, `published`, `archived`)
- Preview support for unpublished posts
- SEO-friendly slugs and Bootstrap-based responsive UI
- Image upload support for post media

### Repository layout
- `app/` – Flask application package (blueprints, models, app factory)
- `templates/` – Jinja2 HTML templates
- `static/` – CSS and uploaded/static assets
- `migrations/` – Database migration artifacts (including `migrations/manual/` SQL files)
- `wsgi.py` – WSGI entrypoint
- `Dockerfile` – Production image definition
- `docker-compose.yml` – Default single-server deployment
- `docker-compose.enterprise.yml` – Enterprise multi-instance deployment
- `docker/` – Container helper scripts and NGINX configuration

### Tech stack
- Python 3.8+
- Flask
- SQLAlchemy + Flask-Migrate
- MariaDB 10.5+
- Bootstrap 5
- Docker / Docker Compose

## Quick start with Docker (recommended)

### Prerequisites
- Docker Engine 24+
- Docker Compose v2+

### 1) Configure environment
```bash
cp .env.example .env
```

Update at least:
- `SECRET_KEY`
- `DB_PASSWORD`
- `DB_ROOT_PASSWORD`

### 2) Default mode: single Linux server
Runs one ForgeCMS container plus one MariaDB container on one host.

```bash
docker compose up -d --build
```

- ForgeCMS: `http://localhost:8000`
- Persistent data:
  - `mariadb_data` volume for DB
  - `uploads_data` volume for media uploads

Stop:
```bash
docker compose down
```

### 3) Enterprise mode: multi-instance application tier
Runs two ForgeCMS app instances behind NGINX plus one MariaDB server.

```bash
docker compose -f docker-compose.enterprise.yml up -d --build
```

- Entry point: `http://localhost` (port 80)
- Backend app containers: `forgecms-a`, `forgecms-b`
- Shared uploads volume mounted by both app containers and NGINX

Stop:
```bash
docker compose -f docker-compose.enterprise.yml down
```

## Docker behavior notes
- Container startup waits for MariaDB before launching the app.
- Database migrations run automatically at startup.
  - In enterprise mode, only `forgecms-a` runs migrations.
- `UPLOAD_FOLDER` defaults to `static/uploads` and is persisted in Docker volumes.

## Local non-Docker setup

### 1) Clone the repository
```bash
git clone <repository-url>
cd forgecms
```

### 2) Create and activate a virtual environment
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Create MariaDB database and user
```sql
CREATE DATABASE forgecms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'forgecms'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON forgecms.* TO 'forgecms'@'localhost';
FLUSH PRIVILEGES;
```

### 5) Configure environment variables
```bash
cp .env.example .env
```

### 6) Apply database migrations
```bash
flask db upgrade
```

### 7) Run the development server
```bash
flask run
```

By default, Flask serves on `http://127.0.0.1:5000`.

## Create an admin user (Flask shell)
```bash
flask shell
```

```python
from app import db
from app.models import User

admin = User(username='admin', email='admin@example.com', is_admin=True)
admin.set_password('your-secure-password')
db.session.add(admin)
db.session.commit()
```

## Community and governance

- [Contributing guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [License (GNU GPLv3)](LICENSE)
