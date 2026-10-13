# Nestora

Nestora is a Django-powered online bookstore for browsing books, managing a session-based cart, placing orders, and tracking order history.

## Local setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DEBUG = "True"
$env:SECRET_KEY = "local-development-key-change-me"
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. Create an administrator with `python manage.py createsuperuser`.

## Appliku deployment

This repository is prepared for Appliku's Python build image:

1. Push this project to GitHub and connect the `main` branch in Appliku.
2. Select a supported Python build image (Python 3.12 or newer) and configure the app to use this repository root.
3. Add processes: `web` → `bash run.sh`; `release` → `bash release.sh`.
4. Create a PostgreSQL database in Appliku and make its connection URL available as `DATABASE_URL`.
5. Set environment variables in Appliku before deploying:
   - `SECRET_KEY`: generate locally with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: the actual Appliku hostname, comma-separated with any custom domains
   - `DATABASE_URL`: the PostgreSQL URL supplied by Appliku
6. Deploy and check build and release logs. Appliku's Python build image runs `collectstatic` when it detects `manage.py`; WhiteNoise serves the collected static files.
7. Configure a persistent volume mounted at `/app/media` (or set `MEDIA_ROOT` to the chosen mount path) for uploaded product and payment images. Existing local SQLite data and uploaded files are not transferred automatically.

Do not commit `.env`, production secrets, database credentials, or database backups. `.env.example` contains only local-development guidance. The Appliku dashboard controls server, domain, HTTPS, database, persistent volume, and deployment configuration; those account-specific steps cannot be completed from this repository.
