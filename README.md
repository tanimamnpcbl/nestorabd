# Nestora

Nestora is a Django-powered online bookstore for browsing books, managing a session-based cart, placing orders, and tracking order history.

## Features

- Browse active products and categories, with search by name, author, brand, or SKU.
- Filter products by category and view related products.
- Maintain a session-based cart with stock checks.
- Register, log in, log out, and view authenticated order history.
- Place orders with Bangladesh-focused delivery fields and Cash on Delivery, bKash, Nagad, Rocket, or Upay payment options.
- Store payment metadata and optional payment screenshots.
- Manage store data through Django admin.

## Technology

- Python 3.8+
- Django 4.2
- SQLite for local development
- Pillow for image uploads
- Bootstrap-based templates with custom CSS in `static/css/`

## Project layout

```text
manage.py             Django management entry point
nestora/              Project settings and URL configuration
store/                Store models, views, forms, admin, and migrations
templates/            HTML templates
static/               Static assets
media/                Local user-uploaded images
db.sqlite3            Local development database
```

## Local setup

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install "Django>=4.2,<5" Pillow
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. Create an administrator with `python manage.py createsuperuser` to manage products, categories, and orders at `/admin/`.

## Configuration

The checked-in settings target local development: `DEBUG` is enabled, SQLite is used, and media files are served by Django in debug mode. Before deployment, move the secret key and database settings to environment variables, set `DEBUG=False`, configure `ALLOWED_HOSTS`, and run `python manage.py collectstatic`.

## Testing

```powershell
python manage.py test
```
# nestorabd
