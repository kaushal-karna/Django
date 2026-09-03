# Detailed Django Project Progress

This document explains the development journey and the work completed so far in the MMAMC Django project. The main working application is `myproject/`. The `portfolio/` directory is a separate Django project and should be run independently.

## 1. Installing Python

Django is a Python web framework, so Python is the first requirement. Install Python 3.8 or a newer version from the official Python website. On Windows, enable the option to add Python to `PATH` during installation.

Verify the installation in PowerShell:

```powershell
python --version
python -m pip --version
```

Using `python -m pip` is helpful because it makes sure that `pip` belongs to the Python interpreter being used by the current command.

## 2. Creating an Isolated Environment

A virtual environment keeps this project's packages separate from other Python projects. The repository already contains a `venv` directory, but a new environment can be created when setting up the project on another computer.

Run these commands from the `Django/` repository directory:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

After activation, PowerShell normally shows `(venv)` at the beginning of the prompt. To leave the environment later, run:

```powershell
deactivate
```

If PowerShell blocks activation because of its execution policy, use a terminal approved by your system administrator or activate the environment from Command Prompt with `venv\Scripts\activate.bat`.

## 3. Installing Django and Project Packages

The dependency list is stored in `requirements.txt`. Install it while the virtual environment is active:

```powershell
pip install -r requirements.txt
```

The project uses Django 6.1 and includes supporting packages such as `asgiref`, `asttokens`, `colorama`, and `comm`. WhiteNoise is also used by the settings for serving collected static files, so the installed environment should contain every package listed in the requirements file.

Check the Django installation with:

```powershell
python -m django --version
```

## 4. Creating the Django Project

A Django project is the configuration and deployment container for a website. It contains settings, the root URL configuration, and ASGI/WSGI entry points. A Django app is a focused feature area inside that project.

The active project follows this structure:

```text
myproject/
├── manage.py
├── db.sqlite3
├── myproject/
├── accounts/
├── home/
├── students/
├── teachers/
├── courses/
├── Templates/
├── static/
└── media/
```

The `manage.py` file is the command-line entry point. It loads the `myproject.settings` module and lets the developer run migrations, checks, tests, the development server, and other Django commands.

A new project would normally begin with commands similar to these:

```powershell
django-admin startproject myproject
cd myproject
python manage.py startapp home
```

The current repository has already progressed beyond this initial scaffold.

## 5. Registering Apps and Configuring Settings

The active settings file is `myproject/myproject/settings.py`. It registers these local apps in `INSTALLED_APPS`:

- `home` for the home page, dashboard, and profile model.
- `accounts` for registration and authentication views.
- `students` for student records and management pages.
- `teachers` for teacher records and management pages.
- `courses` for courses and course relationships.

The settings also configure the built-in Django apps for administration, authentication, sessions, messages, and static files.

The project uses SQLite during development:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

SQLite is convenient for learning because it does not require a separate database server. The database is stored in `myproject/db.sqlite3`.

## 6. Connecting URLs to Apps

The root URL file includes each app's URL configuration:

```python
path("", include("home.urls"))
path("accounts/", include("accounts.urls"))
path("students/", include("students.urls"))
path("teachers/", include("teachers.urls"))
path("courses/", include("courses.urls"))
```

This keeps routing organized. Each app owns its own paths and view names, while the project-level file provides the top-level prefixes.

The current route groups are:

- Home: `/`, `/dashboard/`, and `/profile/`.
- Accounts: `/accounts/login/`, `/accounts/register/`, and `/accounts/logout/`.
- Students: index, add, list, details, edit, and delete paths under `/students/`.
- Teachers: index, add, list, details, edit, and delete paths under `/teachers/`.
- Courses: display, index, add, list, details, edit, and delete paths under `/courses/`.
- Administration: `/admin/`.

Named URL patterns such as `students:student_lists` and `accounts:login` make redirects independent of hard-coded URL strings.

## 7. Templates and Shared Layout

Django templates separate page markup from Python view logic. The project has a shared `Templates/base.html` file and app-specific template directories such as `home/Templates/home/` and `students/Templates/students/`.

The settings enable both project-level template directories and app template discovery through `APP_DIRS`. Pages can extend the shared base template and override blocks for their own content. This avoids repeating the navigation and common page structure on every screen.

Views pass context dictionaries to templates. For example, a student list view queries the database and passes `students`; the template then loops over those records and displays them.

## 8. Building the Data Models

The application demonstrates several important Django model features.

### Student Model

`students.Student` stores:

- A unique student ID and email address.
- First name, last name, phone, address, and personal information.
- Date of birth, department, program, semester, and enrollment year.
- A status choice such as active, inactive, graduated, or suspended.
- Automatically managed `created_at` and `updated_at` timestamps.

The model orders records by last name and first name and provides a readable string representation.

### Teacher Model

`teachers.Teacher` stores personal and professional information, including department, position, qualification, experience, joining date, status, and biography.

Each teacher has a foreign-key relationship to a `Course`. The relationship gives courses access to their related teachers through the `teachers` related name.

### Course Model

`courses.Course` stores a unique course code, name, department, credits, duration, semester, capacity, status, and description.

It demonstrates two relationship types:

- A nullable foreign key to `teachers.Teacher` for the course instructor.
- A many-to-many relationship to `students.Student` through `enrolled_students`.

The many-to-many field allows a course to have multiple enrolled students and a student to enroll in multiple courses.

### Profile Model

`home.Profile` extends Django's built-in `User` without replacing it. A one-to-one field means each user has at most one profile. The profile includes biography, location, birth date, phone number, and an optional profile picture uploaded to `media/profiles/`.

## 9. Creating and Applying Migrations

Migrations translate model changes into database schema changes. After changing a model, use:

```powershell
cd myproject
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` creates migration files in an app's `migrations/` directory. `migrate` applies those files to SQLite and also creates the tables required by Django's built-in applications.

The repository contains migration history for the student, course, and home models. Migration files should be kept with the project because they describe how the schema evolved.

Useful checks are:

```powershell
python manage.py showmigrations
python manage.py sqlmigrate students 0001
```

The second command displays the SQL Django would use for a particular migration.

## 10. Writing Views and CRUD Workflows

Views receive an HTTP request, perform application logic, and return an HTTP response. The project uses function-based views.

The student, teacher, and course apps provide the common CRUD sequence:

1. Display an index or summary page.
2. Create a record from submitted form data.
3. Display a list of records.
4. Display details for one record.
5. Edit an existing record.
6. Delete a record and redirect back to the list.

The views use `get_object_or_404` for detail and edit operations, so an invalid record ID produces a normal 404 response. Django messages are used in some workflows to show a success message after a record is created, updated, or deleted.

The management views are protected with `@login_required`, so anonymous visitors are redirected to the configured login URL.

## 11. Forms and User Input

The `accounts` app uses Django's built-in form classes:

- `LoginForm` extends `AuthenticationForm` and customizes the username and password widgets.
- `RegisterForm` extends `UserCreationForm`, requires an email address, and validates the password confirmation.

The profile page uses `ProfileForm` to accept profile information and uploaded files. On a POST request, the view validates the form before saving. On a GET request, it displays the existing profile values in the form.

Django forms provide validation and help prevent invalid data from being saved directly. The current CRUD pages also demonstrate direct request data handling, which is useful for learning but can later be refactored into dedicated ModelForms for stronger validation and consistency.

## 12. Authentication and Authorization

Registration creates a Django `User`, creates the related empty `Profile`, and logs the new user in. Login checks the submitted credentials and starts a session. Logout ends the session and redirects to the login page.

The settings define these redirect behaviors:

- `LOGIN_URL` points to the login page.
- `LOGIN_REDIRECT_URL` sends a successful login to `/`.
- `LOGOUT_REDIRECT_URL` sends a logged-out user to the login page.

The `login_required` decorator protects the student, teacher, course, and profile workflows. The Django admin is separately protected by staff-user permissions.

## 13. Static Files and Media Files

Static files are assets shipped with the application, such as CSS, JavaScript, and images. The project stores source assets in `myproject/static/` and uses:

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
```

Run this command to collect assets into the deployment directory:

```powershell
python manage.py collectstatic
```

WhiteNoise is included in middleware and configured as the static-file storage backend. This makes serving collected static assets simpler for a deployment that does not use a separate web server.

Because the configured storage is `CompressedManifestStaticFilesStorage`, the manifest must be generated before running with `DEBUG=False`:

```powershell
python manage.py collectstatic --noinput
```

Without this step, rendering `base.html` can raise `ValueError: Missing staticfiles manifest entry for 'css/style.css'`, which appears to the browser as a generic HTTP 500 page. This was the cause of the production-mode error in the current project. The command is safe to repeat; Django reports unchanged files and refreshes the manifest when needed.

Media files are user uploads rather than application assets. The project uses `MEDIA_URL`, `MEDIA_ROOT`, and a debug-only URL pattern to serve uploaded files locally. Production deployments should use a dedicated media storage solution and should not rely on Django's development file serving.

## 14. Running and Testing the Application

Start the development server from the directory containing `manage.py`:

```powershell
cd myproject
python manage.py check
python manage.py migrate
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/`.

A practical testing sequence is:

1. Register a new user at `/accounts/register/`.
2. Confirm that login and logout work.
3. Open the protected student, teacher, or course pages.
4. Add a record and verify it appears in the list.
5. Open its detail page, edit it, and delete it.
6. Update the profile and test the profile picture upload.
7. Open `/admin/` with a superuser and inspect the registered models.

Run the automated tests with:

```powershell
python manage.py test
```

The app test modules are currently present and provide the place to add focused tests as each feature grows.

## 15. Daily Development Workflow

A typical model or feature change follows this sequence:

```powershell
cd myproject
.\..\venv\Scripts\Activate.ps1
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver
```

The activation path assumes the virtual environment is stored at the repository root and the command is run from `myproject/`. If the environment is already active, the activation command can be skipped.

When a page does not work, check the URL pattern, view name, template path, authentication decorator, migration state, and browser/server error message in that order. This follows Django's request path from routing to view logic, database access, and template rendering.

## 16. Current Limitations and Next Steps

The project is intended for learning and local development. Before using it as a production application, it should receive additional work in several areas:

- Move the secret key and other environment-specific values out of source code.
- Replace `DEBUG = True` and `ALLOWED_HOSTS = ["*"]` with production-safe settings.
- Add comprehensive automated tests for authentication, permissions, CRUD operations, and relationships.
- Convert direct POST field assignment in CRUD views to validated ModelForms.
- Add permission checks to destructive actions such as delete operations.
- Register and configure the domain models in Django admin where appropriate.
- Review CSRF, secure cookies, media storage, email, and deployment settings.
- Continue the notebook lessons and keep the implementation notes synchronized with new features.

The current codebase already demonstrates the central Django workflow: define models, create migrations, route requests, execute view logic, render templates, validate user input, authenticate users, and serve static and media files.
