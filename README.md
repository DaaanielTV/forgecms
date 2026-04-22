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

### Tech stack
- Python 3.8+
- Flask
- SQLAlchemy + Flask-Migrate
- MariaDB 10.5+
- Bootstrap 5

## Installation

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
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1
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
Copy `.env.example` to `.env` and update values as needed:

```bash
cp .env.example .env
```

Example values:
```dotenv
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=change-this-to-a-secure-secret-key
DB_HOST=localhost
DB_USER=forgecms
DB_PASSWORD=your_password
DB_NAME=forgecms
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### 6) Apply database migrations
```bash
flask db upgrade
```

## Usage

### Run the development server
```bash
flask run
```

By default, Flask serves on `http://127.0.0.1:5000`.

### Create an admin user (Flask shell)
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

### Useful maintenance commands
```bash
# Create a new migration after model changes
flask db migrate -m "describe change"

# Apply pending migrations
flask db upgrade

# Backup database
mysqldump -u your_user -p forgecms > backup.sql
```

## Production notes

For production, run with a WSGI server (for example Gunicorn) behind NGINX, use HTTPS, and set a strong `SECRET_KEY`.


## Community and governance

- [Contributing guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [License (GNU GPLv3)](LICENSE)
