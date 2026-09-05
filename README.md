# Django Learning Project - MMAMC

This repository contains the Django work completed during the MMAMC web development lessons. It starts with Python and web development fundamentals and grows into a multi-app Django application for managing students, teachers, courses, and user profiles.

**Documentation Navigation:** [README](README.md) | [Detailed Guide](detail.md) | [Commands](command.md) | [Review and Learning](review_and_learning.md) | [Production Settings](track.md) | [Debugging Checklist](django_debugging_checklist.md) | [Status Codes](statuscodes.md) | [ORM Practice](django_orm_practice.md)

**Daily Use:** Start here when you are unsure what to read. Follow the study order below, then use [command.md](command.md) as the central reference for running, checking, reviewing, committing, and pushing the project.

## Current Progress

The main application in `myproject/` currently includes:

- A Django project with SQLite configured as the development database.
- Four domain apps: `home`, `students`, `teachers`, and `courses`.
- An `accounts` app for registration, login, logout, and Django session authentication.
- A project-level `base.html` template plus app-specific templates.
- Static CSS and JavaScript files, image support, and media uploads for profile pictures.
- Models, relationships, choices, timestamps, admin integration points, and migrations.
- Authenticated student, teacher, and course pages with add, list, detail, edit, and delete workflows.
- A staff-only custom admin dashboard with record counts and recent academic records.
- Validated student, teacher, and course ModelForms, safe redirects, and POST-only delete actions.
- A protected profile page using a one-to-one relationship with Django's built-in `User` model.
- Jupyter notebooks covering Python, web development, templates, models, ORM relationships, forms, authentication, and regular expressions.

## Repository Layout

```text
Django/
├── README.md
├── detail.md
├── requirements.txt
├── Day_1_Web Development .ipynb
├── Day_2_Python Fundamentals for Django.ipynb
├── Day_3_Advanced Python Fundamentals.ipynb
├── Day_4_OOP & Django Fundamentals.ipynb
├── Day_5_Django Templates & Static Files.ipynb
├── Day_6_Django Models & Database.ipynb
├── Day_7_Django ORM & Relationships.ipynb
├── Day_8_Forms & User Input.ipynb
├── Day_9_User Authentication & Authorization.ipynb
├── Day_12_regex.ipynb
├── django_orm_practice.md
├── myproject/                 # Main Django learning application
│   ├── manage.py
│   ├── db.sqlite3
│   ├── myproject/             # Settings and root URL configuration
│   ├── accounts/              # Registration and authentication
│   ├── home/                  # Home, dashboard, and user profiles
│   ├── students/              # Student management
│   ├── teachers/              # Teacher management
│   ├── courses/               # Course management and relationships
│   ├── Templates/             # Shared project templates
│   ├── static/                # Source CSS, JavaScript, and images
│   └── media/                 # Uploaded files, including profiles
└── portfolio/                 # Separate portfolio Django project
```

## Application Routes

The root URL configuration includes these app prefixes:

- `/` - Home page
- `/dashboard/` - Dashboard page
- `/admin-dashboard/` - Staff-only custom administration dashboard
- `/accounts/login/` - Log in
- `/accounts/register/` - Create an account
- `/accounts/logout/` - Log out
- `/profile/` - User profile editing
- `/students/` - Student pages
- `/teachers/` - Teacher pages
- `/courses/` - Course pages
- `/admin/` - Django administration

Most management pages are protected with `login_required`. Create an account or a superuser before testing those workflows.

## Requirements

- Python 3.8 or newer
- Django 6.1
- Packages listed in `requirements.txt`
- A terminal such as PowerShell on Windows

## Quick Start

From the repository root, create and activate a virtual environment, install the dependencies, and enter the active project:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
cd myproject
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser. The longer explanation, including what each step does and how the Django pieces work together, is in [detail.md](detail.md).

## Recommended Study Order

Follow this path if you are learning Django from the beginning:

1. Start here: [README.md](README.md) for the project overview and current structure.
2. Learn the setup: [detail.md](detail.md) for Python, virtual environments, Django, apps, models, migrations, templates, and authentication.
3. Practise daily commands: [command.md](command.md) for starting the server, checking code, working with migrations, and using Git.
4. Learn how to review changes: [review_and_learning.md](review_and_learning.md) for the audit method, tests, security fixes, and commit checklist.
5. Learn production configuration: [track.md](track.md) for environment variables, HTTPS, secure cookies, HSTS, and deployment checks.
6. Understand data: [django_orm_practice.md](django_orm_practice.md) for querying and practising the Django ORM.
7. Understand errors: [statuscodes.md](statuscodes.md) to identify what an HTTP status code means.
8. Trace the problem: [django_debugging_checklist.md](django_debugging_checklist.md) to locate the responsible URL, view, form, model, template, or asset.

After the first pass, use [command.md](command.md) during daily work, [django_debugging_checklist.md](django_debugging_checklist.md) whenever something fails, and [statuscodes.md](statuscodes.md) whenever you see an unfamiliar HTTP response.

## Common Development Commands

Run these commands from `myproject/`:

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py test
python manage.py runserver
```

Run `makemigrations` after model changes, then `migrate` to apply the generated schema changes to SQLite. Use `check` as a quick configuration check before starting the server.

When running with `DEBUG=False`, run `collectstatic --noinput` after installing or changing static assets. WhiteNoise uses a compressed manifest in this project, and the manifest must contain every file referenced by `{% static %}` template tags.

## Important Settings

The active project settings configure:

- `home`, `accounts`, `students`, `teachers`, and `courses` in `INSTALLED_APPS`.
- SQLite at `myproject/db.sqlite3`.
- Project-level templates and app template discovery through `APP_DIRS`.
- Source static files in `myproject/static/` and collected files in `staticfiles/`.
- WhiteNoise middleware and compressed static-file storage.
- Uploaded media at `myproject/media/`, served locally while `DEBUG` is enabled.
- Login redirects for authenticated and unauthenticated users.

These settings are intended for learning and local development. Before production use, replace the development secret key, set explicit allowed hosts, disable debug mode, and review the Django deployment checklist.

## Markdown Guides

The notebooks follow the progression from Python fundamentals to Django implementation. Use these Markdown guides as a connected reference:

- [detail.md](detail.md) - Complete setup and implementation explanation.
- [command.md](command.md) - Commands for daily development and project review.
- [django_orm_practice.md](django_orm_practice.md) - ORM concepts and query practice.
- [statuscodes.md](statuscodes.md) - HTTP status-code meanings and first checks.
- [django_debugging_checklist.md](django_debugging_checklist.md) - Step-by-step error tracing.

## Status

This is an educational project under active development. The `portfolio/` directory is retained as a separate Django project and is not part of the `myproject/` commands above.

**Learning Path:** Start here -> [detail.md](detail.md) -> [command.md](command.md) -> [django_orm_practice.md](django_orm_practice.md) -> [statuscodes.md](statuscodes.md) -> [django_debugging_checklist.md](django_debugging_checklist.md) -> return to [README.md](README.md).
