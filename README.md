# Django Project - MMAMC

A comprehensive Django educational project demonstrating web development fundamentals, Python concepts, and Django application development.

## Project Overview

This is a multi-app Django project designed for learning and understanding Django web development. It includes apps for managing students, teachers, courses, and home page content with proper template organization and static file management.

## Project Structure

```
Django/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── Day_1_Web Development.ipynb        # Learning materials
├── Day_2_Python Fundamentals for Django.ipynb
├── Day_3_Advanced Python Fundamentals.ipynb
├── Day_4_OOP & Django Fundamentals.ipynb
├── Day_5_Django Templates & Static Files.ipynb
└── myproject/                         # Main Django project
    ├── manage.py                      # Django management script
    ├── db.sqlite3                     # SQLite database
    ├── myproject/                     # Project settings package
    │   ├── settings.py               # Django settings
    │   ├── urls.py                   # URL routing
    │   ├── asgi.py                   # ASGI configuration
    │   └── wsgi.py                   # WSGI configuration
    ├── home/                         # Home app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   └── Templates/
    │       └── home/
    │           ├── home.html
    │           └── about.html
    ├── students/                     # Students app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   └── Templates/
    │       └── students/
    │           ├── home.html
    │           ├── about.html
    │           └── student_list.html
    ├── teachers/                     # Teachers app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   └── Templates/
    │       └── teachers/
    │           ├── home.html
    │           └── about.html
    ├── courses/                      # Courses app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   └── Templates/
    │       ├── home.html
    │       └── about.html
    └── Templates/                    # Project-level base templates
        └── base.html
```

## Installed Apps

- **home** - Home page and general content management
- **students** - Student management and listing
- **teachers** - Teacher management and profiles
- **courses** - Course management and organization

## Requirements

- Python 3.8+
- Django 6.1
- asgiref 3.12.1

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Navigate to Project Directory

```bash
cd myproject
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 5. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Usage

### Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` with your superuser credentials.

### Apps

- **Home** - General website homepage and navigation
- **Students** - Manage and view student information
- **Teachers** - Manage and view teacher profiles
- **Courses** - Manage course offerings and details

## Learning Resources

This project includes Jupyter notebooks for comprehensive learning:

- **Day 1** - Web Development fundamentals
- **Day 2** - Python Fundamentals for Django
- **Day 3** - Advanced Python Fundamentals
- **Day 4** - OOP & Django Fundamentals
- **Day 5** - Django Templates & Static Files

## Development

### Creating Migrations

After modifying models, create migrations with:

```bash
python manage.py makemigrations
```

### Applying Migrations

```bash
python manage.py migrate
```

### Running Tests

```bash
python manage.py test
```

## Project Settings

Key settings in `myproject/settings.py`:
- DEBUG mode is enabled (for development)
- SQLite database (db.sqlite3)
- Installed apps: home, students, teachers, courses
- Static files and template configuration

## Notes

- The project uses SQLite for the database (suitable for development)
- Template structure follows Django best practices with app-specific template directories
- Each app has its own templates folder to maintain organization

## License

This is an educational project created for learning Django web development.

