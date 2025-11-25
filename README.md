# MJT — Internal Tracking Dashboard

This project (MJT) is a Django-based internal tracking and dashboard application. It contains two main Django apps:
- `tracking`: Business functionality (invoices, inward entries, program details, dashboards)
- `users`: User sign-up/login and session handling

This README gives you a quick start guide, development notes, and where to find key code paths.

## Quick Overview
- Language: Python 3.11+ (project uses Python 3.13 in other contexts)
- Framework: Django 5.x
- Database: MySQL (default in `MJT/settings.py`) — can also use SQLite in local dev

## Project Layout (Important Files)
- `manage.py` — Django management tool
- `MJT/` — configuration and global settings
  - `MJT/settings.py` — Django settings (DB, installed apps)
  - `MJT/urls.py` — root URL routes
- `tracking/` — tracking app (models, views, forms, templates)
- `users/` — user app (registration/login + session handling)
- `templates/` — reusable templates under each app's templates folder
- `requirements.txt` — dependencies (use pip to install)

## Setup (Windows PowerShell)
1. Create virtual environment:
```powershell
python -m venv dj_frame
.\dj_frame\Scripts\Activate
```
2. Install dependencies:
```powershell
pip install -r requirements.txt
```
3. If using MySQL, update `MJT/settings.py` with DB credentials (NAME/USER/PASSWORD/HOST/PORT).
   - On Windows, if `mysqlclient` fails to install, you can use `pymysql` and add to `MJT/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```
4. Apply migrations & create a superuser:
```powershell
python manage.py migrate
python manage.py createsuperuser
```
5. Run the development server:
```powershell
python manage.py runserver
```
6. Open in a browser: `http://127.0.0.1:8000/`.

## Important URLs & Views
- Login: `/users/login/` (handled by `users.views.user_login`)
- Signup: `/users/signup/` (handled by `users.views.signup`)
- Dashboard: Root or `/dashboard/` handled by `tracking.views` (check `tracking/urls.py`)
- Admin: `/admin/`

## Session Usage & Auth Flow
- This project currently uses a custom, session-based login (not Django's built-in auth):
  - After successful login, the view stores values in `request.session`: `user_id`, `user_name`, and `role`.
  - Other views should check `request.session.get('user_id')` to determine if the user is logged in.
  - Example: `if 'user_id' not in request.session: return redirect('users:login')`
- Recommended next steps: migrate to `django.contrib.auth` for production features like password hashing, permissions, and middleware integration.

## Database Notes
- Default config in `MJT/settings.py` shows a MySQL setup. If you want to run without MySQL, swap to SQLite by updating `DATABASES`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Templates & Static Files
- App-level template root folders are used (e.g. `tracking/templates/` and `users/templates/`).
- Place static files under each app's `static/` or a global `static/` directory.

## Running Tests
```powershell
python manage.py test
```

## Common Issues & Troubleshooting
- `ValueError: The view... returned None` — make sure all code paths in views return a `HttpResponse` or `redirect`.
- `mysqlclient` fails to install on Windows — use `pymysql` or install the MySQL developer toolchain.
- Session data not available on included templates — explicitly pass `request` to context or use context processors (`django.template.context_processors.request`).

## Development Tips
- Prefer PRG (POST-Redirect-GET) after successful POST to avoid resubmission.
- Use `django-debug-toolbar` during development (`pip install django-debug-toolbar`) and add to `INSTALLED_APPS`.
- Keep `DEBUG=False` when deploying.

## Recommended Enhancements
- Migrate to built-in Django authentication for robust user management and password reset flows.
- Add a `logout` view to flush the session: `request.session.flush()`.
- Add unit tests for login, session checks, and protected views.

## Contributing
1. Create a branch.
2. Run tests and linters.
3. Submit a PR with a clear description and migration files (if any).

---
If you'd like, I can also:
- Add a `user_logout` view and URL.
- Implement a small `@session_required` decorator to protect tracking views.
- Convert the session-based auth to use `django.contrib.auth`.

Feel free to request any of the above improvements or to tailor this README to match a deployment environment.
