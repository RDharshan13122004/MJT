# MJT Project Documentation

This document describes the MJT Django project: structure, apps, key files, routes, authentication/session flow, setup, and troubleshooting tips.

## Table of Contents
- Project overview
- Requirements
- Project structure
- Apps and responsibilities
- Key files and templates
- URLs / Routes
- Authentication & session flow
- Running the project
- Development tips
- Troubleshooting

## Project overview

MJT is a Django application that provides an internal tracking dashboard and user management. The main apps are:
- `tracking`: Core business functionality and dashboards.
- `users`: User registration, login, and session management.

The project uses Django's templating system for HTML pages and sessions to persist logged-in user information across pages.

## Requirements

- Python 3.11+ (project currently shows Python 3.13 used in other parts) 
- Django 5.x
- Install dependencies with `pip install -r requirements.txt` if present.

## Project structure (important files)

Root:
- `manage.py` — Django CLI entrypoint.
- `db.sqlite3` — default SQLite database (development).
- `DOCUMENTATION.md` — this file.

Project package `MJT/`:
- `settings.py` — Django settings, database, static/media settings, installed apps.
- `urls.py` — root URL configuration.
- `wsgi.py` / `asgi.py` — deployment entrypoints.

App: `tracking/`
- `models.py` — core models used by the application (inward entries, invoices, program details, etc.).
- `views.py` — views that render `dashboard.html`, `Add_invoices.html`, and other templates.
- `forms.py` — Django forms used in tracking views.
- `urls.py` — app-level routes.
- `templates/` — HTML templates used by the tracking app (dashboard, add forms).

App: `users/`
- `models.py` — `UserProfile` model and related fields.
- `forms.py` — `UserLoginForm`, signup forms, etc.
- `views.py` — `user_login`, `signup`, session handling.
- `decorators.py` — helper decorators for protecting views.
- `templates/` — `login.html`, `signup.html`.

## URLs / Routes

Important app routes (see `users/urls.py` and `tracking/urls.py` for details):
- `/users/login/` — Login page handled by `users.views.user_login`.
- `/users/signup/` — Signup page handled by `users.views.signup`.
- `/` or `/dashboard/` — Main dashboard (provided by `tracking.views`).
- Additional views for adding invoices, inward entries and program details are under tracking app routes.

## Authentication & session flow

This project uses a simple session-based flow (custom, not Django's auth):

1. `user_login` view (in `users/views.py`) validates submitted credentials using `UserLoginForm`.
2. On successful login, `user_login` stores minimal user info in session:
   - `request.session['user_id']`
   - `request.session['user_name']`
   - `request.session['role']`
3. Other views should check for presence of `request.session['user_id']` to allow access. Example:

```python
def some_protected_view(request):
    if 'user_id' not in request.session:
        return redirect('users:login')
    user_id = request.session.get('user_id')
    # fetch user or continue
```

4. To log out, clear the session keys:

```python
def user_logout(request):
    request.session.flush()  # removes all session data
    return redirect('users:login')
```

Security notes:
- Do not store sensitive data (passwords) in the session.
- For production use, prefer Django's built-in `django.contrib.auth` with proper password hashing and authentication middleware.

## Running the project

1. Create and activate a virtual environment.

Windows PowerShell:
```powershell
python -m venv dj_frame
.\dj_frame\Scripts\Activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations and start server:
```bash
python manage.py migrate
python manage.py runserver
```

4. Open browser: `http://127.0.0.1:8000/`

## Development tips

- Use `print()` or logging to debug session contents: `print(request.session.items())`.
- Use `django-debug-toolbar` in development to inspect SQL queries and sessions.
- When including templates that reference `request` (e.g., `request.GET`), ensure `request` is available in the context (Django provides it by default when using RequestContext or render shortcut). If an included template still can't access `request`, pass it explicitly in the view context.

## Troubleshooting

- ValueError: view didn't return an HttpResponse -> Ensure all code paths return `HttpResponse` or `redirect` in views (fix `user_login` GET/POST branches).
- Session values not present in template -> pass `request` in template context or use a context processor.
- Authentication mismatch -> If you want Django auth, switch to `django.contrib.auth` and use `login()`/`logout()` helpers.
- Database errors -> run `python manage.py makemigrations` and `python manage.py migrate`.

## Questions / Next steps

- Migrate to Django auth (recommended) for production.
- Add logout view and `@login_required`-like decorator that checks session keys.
- Add unit tests for login/signup flows and protected views.

---
Generated on: 2025-11-20
Copy Right: Dharshan Srinivas R
