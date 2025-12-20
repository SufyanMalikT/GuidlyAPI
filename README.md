# GuidlyAPI

GuidlyAPI is a Django REST API for managing students, consultants, universities, programs, applications, and payments. It uses Django REST Framework and Simple JWT for authentication. The project is structured as a Django project with two primary apps:

- `accounts` — custom user model and authentication-related views/serializers.
- `api` — main application logic (models, serializers, viewsets, routes).

This README gives an overview of the code, setup and run instructions, environment configuration, and usage examples.

---

## Repo structure (high level)

- GuidlyAPI/ — Django project settings, ASGI/WSGI, URLs
  - settings.py — project settings (JWT, REST framework, CORS, database config via env)
  - urls.py — registers `admin/`, `accounts/` and `api` routes
- api/ — main app
  - models.py — Student, Consultant, University, Program, Application, Payment
  - serializers.py — Model serializers (notable: ApplicationSerializer auto-assigns a consultant)
  - views.py — ModelViewSets with role-based querysets and permissions
  - urls.py — Router exposing API endpoints (`/api/...`)
  - migrations/ — auto-generated migrations
- accounts/ — auth app
  - models.py — `CustomUser` (extends `AbstractUser` with `role` field)
  - views.py — user viewset and custom token view
- manage.py
- requirements.txt
- .gitignore

---

## What the API provides

- CRUD for Students, Consultants, Programs and Applications via DRF viewsets.
- Application lifecycle:
  - `Application` has statuses (`Pending`, `Submitted`, `Approved`, `Rejected`).
  - `ApplicationSerializer` sets read-only fields for student, consultant, status and auto-assigns a consultant on creation (simple assignment logic).
  - Unique constraint: a student cannot apply to the same program more than once.
- `Payment` model with statuses (`Pending`, `Completed`, `Failed`) and relation to `Application`.
- Role-based permissions:
  - `CustomUser.role` supports `'student'`, `'consultant'`, and `'admin'`.
  - `ApplicationViewSet` enforces:
    - Create: students only
    - Update: consultants only
    - Destroy: admins only
  - `PaymentViewSet` restricted to admins.
- Authentication: JWT via `rest_framework_simplejwt`.

---

## Key endpoints

Registered router in `api/urls.py` exposes these endpoints under `/api/`:

- GET/POST/PUT/PATCH/DELETE /api/applications/
- GET/POST/PUT/PATCH/DELETE /api/students/
- GET/POST/PUT/PATCH/DELETE /api/consultants/
- GET/POST/PUT/PATCH/DELETE /api/programs/

Also:
- /admin/ — Django admin
- /accounts/ — account-related routes (user management and token views depending on configuration)

(Exact auth/token endpoints depend on how `accounts.urls` are configured in the repo — check `accounts/urls.py` for token route paths if present.)

---

## Environment / Configuration

GuidlyAPI loads several settings from environment variables (via python-dotenv). The important ones found in `GuidlyAPI/settings.py`:

- API_SECRET_KEY — Django SECRET_KEY
- API_DEBUG — "True" or "False" (defaults to False)
- API_ALLOWED_HOSTS — comma-separated hostnames (defaults to `localhost`)
- DB_NAME — database name (defaults to `GuidlyDB`)
- DB_HOST — database host (defaults to `DESKTOP-5SQEJQ7`)
- DB_TRUSTED — trusted connection option for MS SQL driver (defaults to `yes`)

The project is configured to use Microsoft SQL Server via `mssql` engine and ODBC Driver 17 for SQL Server. If you are using SQL Server with SQL authentication, you may also need to provide DB user and password using environment variables (for example `DB_USER`, `DB_PASSWORD`) — adjust settings or the env accordingly.

CORS allowed origins include:
- http://localhost:5173
- http://localhost:3000

JWT settings:
- Access token lifetime: 30 minutes
- Refresh token lifetime: 1 day
- Auth header type: `Bearer`

REST framework default authentication is JWT and default permission is `IsAuthenticated`.

---

## Quickstart (development)

1. Clone the repository
   - git clone https://github.com/SufyanMalikT/GuidlyAPI.git
   - cd GuidlyAPI

2. Create and activate a virtual environment
   - python -m venv venv
   - On Windows: venv\Scripts\activate
   - On macOS/Linux: source venv/bin/activate

3. Install dependencies
   - pip install -r requirements.txt

4. Create a `.env` file in project root with required variables (example below).

5. Apply database migrations
   - python manage.py migrate

6. (Optional) Create a superuser
   - python manage.py createsuperuser

7. Run the development server
   - python manage.py runserver

8. Open:
   - Admin site: http://127.0.0.1:8000/admin/
   - API root: http://127.0.0.1:8000/api/

---

## Example .env template

Create a `.env` file in project root. Adjust values as needed:

API_SECRET_KEY=replace_this_with_a_secret_key
API_DEBUG=True
API_ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=GuidlyDB
DB_HOST=localhost
DB_TRUSTED=yes
### If using SQL auth:
DB_USER=sa
DB_PASSWORD=yourStrong(!)Password

