# 📚 Bookstore API — Django + PostgreSQL CRUD Project

A complete learning project covering Python, Django, PostgreSQL, REST APIs, Git, and local debugging.

---

## 🗂️ Project Structure

```
django_crud_project/
├── config/                  ← Django project settings
│   ├── __init__.py
│   ├── settings.py          ← Database, installed apps, DRF config
│   ├── urls.py              ← Root URL routing
│   └── wsgi.py
├── bookstore/               ← Our main app
│   ├── migrations/          ← Database migration files
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py             ← Django Admin configuration
│   ├── apps.py
│   ├── models.py            ← Author & Book database models
│   ├── serializers.py       ← JSON ↔ Python conversion
│   ├── views.py             ← API logic (CRUD handlers)
│   └── urls.py              ← App-level URL routing
├── manage.py                ← Django management CLI
├── requirements.txt         ← Python dependencies
├── .env.example             ← Environment variable template
└── README.md                ← This file
```

---

## ⚙️ 1. Prerequisites — Install These First

### Python 3.10+
```bash
# Check if installed
python --version   # or python3 --version

# Download from: https://www.python.org/downloads/
```

### PostgreSQL 15+
```
Download from: https://www.postgresql.org/download/
- During install, set a password for the 'postgres' user (remember it!)
- Default port: 5432
- pgAdmin is installed alongside PostgreSQL — use it to visually manage your DB
```

### Postman
```
Download from: https://www.postman.com/downloads/
Used to test our API endpoints visually (like a browser for APIs)
```

### Git
```
Download from: https://git-scm.com/downloads
```

---

## 🐘 2. PostgreSQL Setup

### Create the database
Open **pgAdmin** or **psql** terminal and run:

```sql
-- In pgAdmin: right-click "Databases" → Create → Database
-- Or in psql terminal:
CREATE DATABASE bookstore_db;

-- Verify it exists
\l
```

### Using psql (command line)
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE bookstore_db;

# Exit
\q
```

---

## 🐍 3. Python Virtual Environment Setup

```bash
# Navigate to project folder
cd django_crud_project

# Create virtual environment (isolates dependencies)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Your prompt will change to: (venv) $

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

---

## 🔐 4. Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your PostgreSQL credentials:
DB_NAME=bookstore_db
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD   ← change this!
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=my-super-secret-key-12345
DEBUG=True
```

> ⚠️ Never commit `.env` to Git. It's already in `.gitignore`.

---

## 🚀 5. Run the Application

```bash
# Make sure your virtual environment is active: (venv) $

# Step 1: Apply database migrations (creates tables in PostgreSQL)
python manage.py migrate

# Step 2: Create an admin user (for /admin panel)
python manage.py createsuperuser
# Enter: username, email, password

# Step 3: Start the development server
python manage.py runserver

# You'll see:
# Starting development server at http://127.0.0.1:8000/
```

Visit in browser:
- **API Root**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 📡 6. API Endpoints & Postman Testing

### Authors

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/authors/` | List all authors |
| POST | `/api/authors/` | Create an author |
| GET | `/api/authors/{id}/` | Get one author |
| PUT | `/api/authors/{id}/` | Update (full) |
| PATCH | `/api/authors/{id}/` | Update (partial) |
| DELETE | `/api/authors/{id}/` | Delete author |
| GET | `/api/authors/{id}/books/` | All books by author |

### Books

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/books/` | List all books |
| POST | `/api/books/` | Create a book |
| GET | `/api/books/{id}/` | Get one book |
| PUT | `/api/books/{id}/` | Update (full) |
| PATCH | `/api/books/{id}/` | Update (partial) |
| DELETE | `/api/books/{id}/` | Delete book |
| GET | `/api/books/available/` | Only available books |
| PATCH | `/api/books/{id}/toggle_availability/` | Flip availability |

### Search & Filter
```
GET /api/books/?search=python        ← search by title/author
GET /api/books/?ordering=price       ← sort ascending by price
GET /api/books/?ordering=-price      ← sort descending by price
GET /api/authors/?search=tolkien     ← search authors
```

---

## 🧪 7. Postman — Step by Step

### Setup
1. Open Postman → New Collection → "Bookstore API"
2. Set base URL variable: `{{base_url}}` = `http://127.0.0.1:8000`

### Create an Author (POST)
```
Method: POST
URL: {{base_url}}/api/authors/
Headers: Content-Type: application/json
Body (raw JSON):
{
    "name": "George Orwell",
    "bio": "English novelist known for 1984 and Animal Farm",
    "birth_date": "1903-06-25"
}
```

### Create a Book (POST)
```
Method: POST
URL: {{base_url}}/api/books/
Headers: Content-Type: application/json
Body (raw JSON):
{
    "title": "1984",
    "author": 1,
    "price": "12.99",
    "genre": "fiction",
    "published_year": 1949,
    "isbn": "9780451524935",
    "is_available": true
}
```

### List All Books (GET)
```
Method: GET
URL: {{base_url}}/api/books/
No body needed
```

### Update a Book (PATCH)
```
Method: PATCH
URL: {{base_url}}/api/books/1/
Body:
{
    "price": "9.99"
}
```

### Delete a Book (DELETE)
```
Method: DELETE
URL: {{base_url}}/api/books/1/
No body needed → Returns 204 No Content
```

---

## 🔍 8. Debugging Tips

### Check database connection
```bash
python manage.py dbshell
# Opens psql connected to your DB
\dt          # list tables
SELECT * FROM books LIMIT 5;
\q           # quit
```

### Django shell — test your models interactively
```bash
python manage.py shell

# Inside the shell:
from bookstore.models import Author, Book

# Create
author = Author.objects.create(name="J.K. Rowling")

# Read
Author.objects.all()
Author.objects.filter(name__icontains="rowl")
Author.objects.get(id=1)

# Update
author.name = "Joanne Rowling"
author.save()

# Delete
author.delete()

exit()
```

### Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `OperationalError: connection refused` | PostgreSQL not running | Start PostgreSQL service |
| `password authentication failed` | Wrong DB password in .env | Check `.env` DB_PASSWORD |
| `relation does not exist` | Migrations not run | Run `python manage.py migrate` |
| `ModuleNotFoundError: decouple` | venv not activated | Run `source venv/bin/activate` |
| `Port 8000 already in use` | Another server running | `python manage.py runserver 8001` |

---

## 🌿 9. Git Workflow

```bash
# Initialize repository
git init

# Create .gitignore FIRST
echo "venv/
.env
__pycache__/
*.pyc
db.sqlite3
.DS_Store" > .gitignore

# Initial commit
git add .
git commit -m "Initial Django + PostgreSQL bookstore project"

# Create a feature branch
git checkout -b feature/add-book-reviews

# After changes, commit them
git add bookstore/models.py
git commit -m "Add Review model linked to Book"

# Merge back to main
git checkout main
git merge feature/add-book-reviews
```

---

## 📚 10. Learning Concepts Checklist

- [ ] Python basics: functions, classes, decorators, f-strings
- [ ] Django structure: apps, settings, URLs, views
- [ ] PostgreSQL: connect, create DB, run SQL queries
- [ ] Models: fields, ForeignKey, Meta class
- [ ] Migrations: makemigrations, migrate, sqlmigrate
- [ ] CRUD: Create / Read / Update / Delete via API
- [ ] DRF: Serializers, ViewSets, Routers
- [ ] Postman: test all 5 HTTP methods
- [ ] Git: init, add, commit, branch, merge
- [ ] Debug: shell, dbshell, error messages

---

## 🧩 Key Concepts Explained

### What is a Migration?
Django can't read your Python model and magically create a table. You must:
1. `python manage.py makemigrations` → generates a migration file describing the change
2. `python manage.py migrate` → executes that SQL against PostgreSQL

### What is a Serializer?
```
API Request (JSON) → Serializer → Python Object → Database
Database → Python Object → Serializer → API Response (JSON)
```

### What is a ViewSet?
A ViewSet is a class that groups all CRUD operations for a model:
- `list()` → GET all
- `create()` → POST new
- `retrieve()` → GET one
- `update()` → PUT replace
- `partial_update()` → PATCH modify
- `destroy()` → DELETE
