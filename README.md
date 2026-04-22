# BlogForge

A modern blog/CMS system built with Flask and MariaDB.

## Features

- User authentication and registration
- Admin dashboard for content management
- Markdown support for blog posts
- Image upload support
- Responsive design using Bootstrap
- SEO-friendly URLs
- Post workflow states (draft, scheduled, published, archived)
- Admin preview route for unpublished content

## Incremental CMS Roadmap

The project is intentionally evolving in small, low-risk increments:

1. **Workflow + Preview (implemented):** status model, scheduling timestamp, admin preview.
2. **Taxonomy:** categories, tags, filtering UI.
3. **Revisions:** immutable post revision snapshots + rollback.
4. **Media library:** media table, metadata, and picker improvements.
5. **RBAC:** role + permission models (keep `is_admin` compatibility).
6. **SEO fields:** per-post meta title/description/canonical/og image.
7. **Search:** keyword + status/category/tag filters for admin/public lists.
8. **Dashboard analytics:** top posts, draft/scheduled counts, and activity snapshots.
9. **Headless API:** authenticated JSON endpoints with minimal schema.

Each phase should ship with migration scripts and remain backward compatible.

## Prerequisites

- Python 3.8+
- MariaDB 10.5+
- NGINX (for production)
- Python virtual environment

## Local Development Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure MariaDB:
   ```sql
   CREATE DATABASE blogforge CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'blogforge'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON blogforge.* TO 'blogforge'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Set up environment variables by copying `.env.example` to `.env` and updating the values:
   ```
   FLASK_APP=app
   FLASK_ENV=development
   SECRET_KEY=your-super-secret-key
   DB_HOST=localhost
   DB_USER=blogforge
   DB_PASSWORD=your_password
   DB_NAME=blogforge
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

6. Run the development server:
   ```bash
   flask run
   ```

## Production Deployment with NGINX

1. Install required system packages:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx mariadb-server
   ```

2. Set up MariaDB:
   ```bash
   sudo mysql_secure_installation
   ```
   Then create the database and user as shown in the local setup.

3. Clone the repository and set up the application:
   ```bash
   git clone <repository-url>
   cd blogforge
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. Create NGINX configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /path/to/blogforge/static;
           expires 30d;
       }

       location /uploads {
           alias /path/to/blogforge/static/uploads;
           expires 30d;
       }
   }
   ```

5. Create a systemd service file `/etc/systemd/system/blogforge.service`:
   ```ini
   [Unit]
   Description=BlogForge Gunicorn Service
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/blogforge
   Environment="PATH=/path/to/blogforge/venv/bin"
   EnvironmentFile=/path/to/blogforge/.env
   ExecStart=/path/to/blogforge/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app()"

   [Install]
   WantedBy=multi-user.target
   ```

6. Set up permissions and start services:
   ```bash
   sudo chown -R www-data:www-data /path/to/blogforge
   sudo systemctl enable blogforge
   sudo systemctl start blogforge
   sudo systemctl enable nginx
   sudo systemctl start nginx
   ```

7. Configure SSL with Let's Encrypt:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## Creating an Admin User

After deployment, create an admin user using the Flask shell:

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

## Security Considerations

1. Always use strong passwords
2. Keep your secret key secure and unique
3. Regularly update dependencies
4. Enable HTTPS in production
5. Configure proper file upload limits
6. Set secure file permissions

## Maintenance

### Database Backup
```bash
mysqldump -u your_user -p blogforge > backup.sql
```

### Updating the Application
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
sudo systemctl restart blogforge
```
