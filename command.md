# Command Guide for the MMAMC Django Project

This is a practical command reference for working in this repository on Windows with PowerShell. The main application is in `myproject/`, and its `manage.py` file is inside that directory.

**Documentation Navigation:** [README](README.md) | [Detailed Guide](detail.md) | [Commands](command.md) | [Review and Learning](review_and_learning.md) | [Production Settings](track.md) | [Debugging Checklist](django_debugging_checklist.md) | [Status Codes](statuscodes.md) | [ORM Practice](django_orm_practice.md)

**Recommended Next:** Use [django_orm_practice.md](django_orm_practice.md) for data practice, then keep [statuscodes.md](statuscodes.md) and [django_debugging_checklist.md](django_debugging_checklist.md) open during daily development.

**Central Reference:** Use this file for commands. Use [README.md](README.md) for the learning order, [detail.md](detail.md) for concepts, [django_debugging_checklist.md](django_debugging_checklist.md) for error tracing, [statuscodes.md](statuscodes.md) for HTTP results, and [django_orm_practice.md](django_orm_practice.md) for database queries.

## 1. Open the Project

From PowerShell:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django
```

Check the current directory and list its files:

```powershell
Get-Location
Get-ChildItem
```

A short alias version is also common:

```powershell
pwd
ls
```

## 2. Activate the Virtual Environment

Activate the repository virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

Confirm which Python is active:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

The executable should point to:

```text
C:\Users\USER\Desktop\MMAMC\Django\venv\Scripts\python.exe
```

Leave the virtual environment with:

```powershell
deactivate
```

## 3. Install and Inspect Packages

Upgrade `pip` and install the repository requirements:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Show installed packages:

```powershell
python -m pip list
python -m pip freeze
```

Check individual packages:

```powershell
python -m django --version
python -c "import whitenoise; print('WhiteNoise is installed')"
```

When a package is missing, install it into the active environment, then update the requirements file if it belongs to the project:

```powershell
python -m pip install package-name
python -m pip freeze > requirements.txt
```

Review the generated requirements file before keeping it, because freezing can include packages used only by notebooks or local tools.

## 4. Run the Active Django Project

Move into the directory containing the active project's `manage.py`:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
```

Start the development server:

```powershell
python manage.py runserver
```

Open the site at:
```text
http://127.0.0.1:8000/
```

Use another port when necessary:

```powershell
python manage.py runserver 8001
```

Stop the server with `Ctrl+C`.

## 5. Commands Used to Check This Project

Run the standard Django configuration check:

```powershell
python manage.py check
```

Run the stricter deployment check:

```powershell
python manage.py check --deploy
```

The deployment check reports security improvements such as secret-key handling, HTTPS, secure cookies, and production email configuration. These are important for deployment but are not all required for local learning.

Check whether model changes require a migration:

```powershell
python manage.py makemigrations --check --dry-run
```

Show migration status:

```powershell
python manage.py showmigrations
```

Show the complete migration execution plan:

```powershell
python manage.py showmigrations --plan
```

Run the test suite:

```powershell
python manage.py test
```

The main project now includes five focused regression tests. The separate `portfolio/` project currently has no discovered tests, so `Found 0 test(s)` there means only that the test runner completed; it is not meaningful behavioral coverage.

Compile project Python files without compiling the virtual environment:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django
python -m compileall -q myproject portfolio
```

Check Git whitespace errors:

```powershell
git diff --check
```

Check changed and untracked files:

```powershell
git status --short
```

Review changes:

```powershell
git diff
```

Review a summary only:

```powershell
git diff --stat
```

## 6. Commands Used During This Project Review

These are the real checks used while fixing and reviewing the project. They form a useful audit recipe when you want confidence before pushing changes.

### Check the Active Project

Use the repository virtual-environment interpreter explicitly when more than one Python installation exists:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
& ..\venv\Scripts\python.exe manage.py check
& ..\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
& ..\venv\Scripts\python.exe manage.py test
```

Expected results for the current project are no system-check issues, no migration changes, and a successful test command. The project currently has no discovered tests, so `Found 0 test(s)` means the test runner completed but test coverage has not been added yet.

### Check the Separate Portfolio Project

The repository contains a second Django project. Run its command from its own directory:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\portfolio
Remove-Item Env:DJANGO_SETTINGS_MODULE -ErrorAction SilentlyContinue
& ..\venv\Scripts\python.exe manage.py check
& ..\venv\Scripts\python.exe manage.py test
```

The environment-variable command matters when a previous terminal session set `DJANGO_SETTINGS_MODULE` for `myproject`. An inherited setting can make the portfolio command load the wrong settings package.

### Compile Both Projects

Run this from the repository root. It checks project Python syntax without scanning the virtual environment:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django
& .\venv\Scripts\python.exe -m compileall -q myproject portfolio
```

### Reproduce a Production-Style Request

This checks representative pages with `DEBUG=False` without permanently changing `settings.py`:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
@'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()
from django.test import Client, override_settings

with override_settings(DEBUG=False):
    client = Client(raise_request_exception=False)
    for path in ['/', '/accounts/login/', '/accounts/register/', '/courses/']:
        response = client.get(path, HTTP_HOST='127.0.0.1')
        print(path, response.status_code)
'@ | & ..\venv\Scripts\python.exe -
```

Expected output is HTTP `200` for the public pages. If the result is `500`, read the traceback produced by the same script without `raise_request_exception=False` or inspect the running server's terminal.

### Build and Check Static Files

The active project uses WhiteNoise's compressed manifest storage:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
& ..\venv\Scripts\python.exe manage.py collectstatic --noinput
Test-Path .\staticfiles\staticfiles.json
& ..\venv\Scripts\python.exe manage.py findstatic css/style.css --verbosity 1
```

The manifest check should return `True`, and `findstatic` should locate the source stylesheet. Missing the manifest can cause a `DEBUG=False` 500 error when a template uses `{% static %}`.

### Final Review Commands

Run these from the repository root after editing documentation or code:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django
git diff --check
git status --short
git diff --stat
```

These checks catch whitespace problems, show untracked files that might need adding, and provide a compact view of the change size.

### Review New and Staged Files

List every changed path, including untracked files:

```powershell
git status --short
git diff --name-only
```

Read the full tracked diff and inspect new files separately. `git diff` does not show untracked files until they are staged, so review new files directly before adding them.

After staging only intended paths, repeat the checks against the staged snapshot:

```powershell
git diff --cached --check
git diff --cached --stat
git diff --cached
```

Never use `git add .` without first reviewing every untracked directory. Review `git status --short` before staging so unrelated files are not included.

### Test the Dashboard Permission Boundary

This small script checks anonymous, regular-user, and staff access to the custom dashboard:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
@'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()
User.objects.filter(username__in=['__check_user__', '__check_staff__']).delete()
user = User.objects.create_user('__check_user__', password='test-password-123')
staff = User.objects.create_user('__check_staff__', password='test-password-123', is_staff=True)
client = Client()
print('anonymous:', client.get('/admin-dashboard/').status_code)
client.login(username=user.username, password='test-password-123')
print('regular:', client.get('/admin-dashboard/').status_code)
client.logout()
client.login(username=staff.username, password='test-password-123')
print('staff:', client.get('/admin-dashboard/').status_code)
User.objects.filter(pk__in=[user.pk, staff.pk]).delete()
'@ | & ..\venv\Scripts\python.exe -
```

Expected output is `302` for anonymous and regular users, and `200` for a staff user.

### Production Environment Validation

The settings use environment variables so local development can remain convenient while deployment settings are explicit:

```powershell
$env:DJANGO_DEBUG='False'
$env:DJANGO_SECRET_KEY='replace-with-a-long-random-production-secret'
$env:DJANGO_ALLOWED_HOSTS='example.com,www.example.com'
$env:DJANGO_SECURE_SSL_REDIRECT='True'
$env:DJANGO_SESSION_COOKIE_SECURE='True'
$env:DJANGO_CSRF_COOKIE_SECURE='True'
$env:DJANGO_SECURE_HSTS_SECONDS='31536000'
$env:DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS='True'
$env:DJANGO_SECURE_HSTS_PRELOAD='True'
python manage.py check --deploy
```

Do not commit real secrets. Remove temporary environment variables from the current PowerShell session when finished:

```powershell
Remove-Item Env:DJANGO_DEBUG,Env:DJANGO_SECRET_KEY,Env:DJANGO_ALLOWED_HOSTS,Env:DJANGO_SECURE_SSL_REDIRECT,Env:DJANGO_SESSION_COOKIE_SECURE,Env:DJANGO_CSRF_COOKIE_SECURE,Env:DJANGO_SECURE_HSTS_SECONDS,Env:DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS,Env:DJANGO_SECURE_HSTS_PRELOAD -ErrorAction SilentlyContinue
```

### Review and Learning Guide

Read [review_and_learning.md](review_and_learning.md) for the complete explanation of the audit, dashboard, security fixes, tests, green-signal checklist, and safe commit workflow.

## 7. Database and Migration Workflow

After changing a model:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

Create migrations for one app only:

```powershell
python manage.py makemigrations students
python manage.py makemigrations teachers
python manage.py makemigrations courses
```

Apply migrations for one app:

```powershell
python manage.py migrate students
```

Inspect the SQL for a migration:

```powershell
python manage.py sqlmigrate students 0001
```

Open the Django database shell:

```powershell
python manage.py dbshell
```

The SQLite command may require the SQLite executable to be installed separately. You can still inspect data using Django's shell:

```powershell
python manage.py shell
```

Example ORM inspection inside the Django shell:

```python
from students.models import Student
Student.objects.count()
Student.objects.all()
exit()
```

Create an administrator account:

```powershell
python manage.py createsuperuser
```

Then visit:

```text
http://127.0.0.1:8000/admin/
```

## 8. Static Files and DEBUG=False

The active project uses WhiteNoise's compressed manifest storage. Generate the manifest after installing or changing CSS, JavaScript, or image assets:

```powershell
python manage.py collectstatic --noinput
```

Check the production-style configuration:

```powershell
python manage.py check --deploy
```

The important sequence is:

```powershell
python manage.py collectstatic --noinput
python manage.py runserver --insecure
```

`runserver --insecure` is useful for local static-file testing with `DEBUG=False`, but it is not a production server. If the manifest is missing, templates using `{% static %}` can produce a 500 error such as:

```text
ValueError: Missing staticfiles manifest entry for 'css/style.css'
```

Generated files under `myproject/staticfiles/` are ignored by Git. Source assets belong in `myproject/static/`.

## 9. Temporarily Test DEBUG=False

The current settings file has `DEBUG = True` as a development default. To test production-style rendering without permanently editing settings, use a short Django shell script:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
@'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()
from django.test import Client, override_settings

with override_settings(DEBUG=False):
    client = Client(raise_request_exception=False)
    for path in ['/', '/accounts/login/', '/accounts/register/', '/courses/']:
        response = client.get(path, HTTP_HOST='127.0.0.1')
        print(path, response.status_code)
'@ | python -
```

A healthy result prints HTTP `200` for the public pages. Use the project's virtual-environment interpreter explicitly when the active shell may be using another Python:

```powershell
@' ... '@ | & C:\Users\USER\Desktop\MMAMC\Django\venv\Scripts\python.exe -
```

## 10. Find Errors Quickly

Search all Python files for a word or setting:

```powershell
rg "DEBUG|SECRET_KEY|STATIC|login_required" myproject -g "*.py"
```

Search templates for static references:

```powershell
rg "static|url |extends|include" myproject -g "*.html"
```

Find all Django files:

```powershell
rg --files myproject -g "*.py"
rg --files myproject -g "*.html"
rg --files myproject -g "*migration*.py"
```

Find a specific URL name:

```powershell
rg "name=['\"](student_lists|course_lists|profile)" myproject
```

Check whether a file exists:

```powershell
Test-Path .\myproject\staticfiles\staticfiles.json
Test-Path .\myproject\Templates\base.html
```

List files by extension:

```powershell
Get-ChildItem -Recurse -File -Filter *.py
Get-ChildItem -Recurse -File -Filter *.html
```

When a page returns 500, run the server in the terminal and read the traceback. With `DEBUG=True`, Django shows the exception details. With `DEBUG=False`, inspect the server terminal because the browser intentionally shows only a generic error page.

## 11. Daily Workflow

Use this compact routine at the beginning of a work session:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django
.\venv\Scripts\Activate.ps1
cd myproject
python manage.py check
python manage.py showmigrations
python manage.py runserver
```

Before changing a model:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
```

After changing a model:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py check
python manage.py test
```

Before finishing work:

```powershell
python manage.py check
python manage.py test
cd ..
git diff --check
git status --short
```

## 12. Git Basics for Safe Progress

Run Git commands from the repository root:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django
```

Git tracks changes to the project so you can review, restore, share, and safely collaborate on your work. The usual order is **review -> stage -> review staged files -> commit -> verify -> push**. Do not skip the second review: the staged diff is exactly what will enter the commit.

### Review Before Staging

```powershell
git status
git status --short
git diff
git diff --stat
git diff --check
git diff -- myproject\students\views.py
git log -5 --oneline
git branch --show-current
git branch -vv
```

- `git status` shows the branch, staged files, unstaged files, and untracked files.
- `git status --short` gives the same information in a compact two-column format.
- `git diff` shows edits that are not staged yet.
- `git diff --stat` shows only a file and line-change summary.
- `git diff --check` finds whitespace errors before they reach a commit.
- `git diff -- myproject\students\views.py` limits the diff to one file.
- `git log -5 --oneline` shows the five latest commits in a compact format.
- `git branch --show-current` prints the branch you are currently using.
- `git branch -vv` shows local branches and their upstream remote branches.

### Stage the Intended Files

Stage only files you have reviewed:

```powershell
git add README.md command.md detail.md django_debugging_checklist.md django_orm_practice.md statuscodes.md
```

For the complete current update, include the settings and ignore-file changes:

```powershell
git add .gitignore README.md myproject\myproject\settings.py command.md detail.md django_debugging_checklist.md django_orm_practice.md statuscodes.md
```

Use `git add -A` only after checking every new, modified, and deleted file:

```powershell
git add -A
```

- `git add path\to\file` stages one selected file.
- `git add README.md command.md ...` stages only the reviewed files listed in the command.
- `git add -A` stages all changes, including new and deleted files, so use it only after reviewing `git status`.

### Review Staged Changes

```powershell
git status
git diff --cached
git diff --cached --stat
git diff --cached --check
```

- `git status` confirms which files are staged.
- `git diff --cached` shows the exact content that the next commit will contain.
- `git diff --cached --stat` summarizes only staged changes.
- `git diff --cached --check` checks staged changes for whitespace problems.

If an unintended file was staged, unstage it without deleting it:

```powershell
git restore --staged path\to\file
```

`git restore --staged` removes a file from the staging area but keeps your edits on disk. It is the normal fix when you staged a file by mistake.

### Commit and Verify

```powershell
git commit -m "docs: add Django setup, commands, and debugging guides"
git log -1 --oneline
git show --stat --oneline HEAD
git status
```

- `git commit -m "message"` creates a permanent commit from the staged snapshot.
- `git log -1 --oneline` confirms the newest commit message and ID.
- `git show --stat --oneline HEAD` shows what the newest commit changed.
- `git status` confirms whether the working tree is clean after committing.

### Push to GitHub

Confirm the remote and branch before pushing:

```powershell
git remote -v
git branch --show-current
git fetch origin
git push origin main
git status
```

- `git remote -v` displays the GitHub fetch and push URLs.
- `git fetch origin` downloads remote branch information without changing your files.
- `git push origin main` uploads the local `main` commits to GitHub.
- The final `git status` confirms whether the local branch is synchronized with its remote.

For a new branch, publish it and set its upstream:

```powershell
git push -u origin branch-name
```

`git push -u origin branch-name` uploads a new branch and remembers its upstream, so later `git push` and `git pull` commands can omit the remote and branch names.

If Git says the remote has commits you do not have, inspect both sides before trying again:

```powershell
git fetch origin
git log --oneline HEAD..origin/main
git log --oneline origin/main..HEAD
```

- `git log --oneline HEAD..origin/main` shows commits on GitHub that are missing locally.
- `git log --oneline origin/main..HEAD` shows local commits not yet on GitHub.
- Read both lists before deciding whether to pull, merge, rebase, or ask for help.

Do not use `git reset --hard` or `git checkout --` casually. They can destroy work that has not been backed up.

- `git reset --hard` discards local tracked edits and moves the current branch; use only when you fully understand the data loss.
- `git checkout -- path` discards local edits in a file; use `git restore path` only with the same caution.
- Prefer `git restore --staged path` when you only need to unstage a file.

### Complete Current Workflow

Run Django checks first, then review, stage, commit, and push:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
& ..\venv\Scripts\python.exe manage.py check
& ..\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
& ..\venv\Scripts\python.exe manage.py test
cd ..
git diff --check
git status
git diff --stat
git add .gitignore README.md myproject\myproject\settings.py command.md detail.md django_debugging_checklist.md django_orm_practice.md statuscodes.md
git status
git diff --cached --check
git diff --cached --stat
git commit -m "docs: add Django setup, commands, and debugging guides"
git log -1 --oneline
git status
git push origin main
git status
```

## 13. Run the Separate Portfolio Project

The `portfolio/` directory has its own `manage.py` and settings package. Run it independently:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\portfolio
python manage.py check
python manage.py migrate
python manage.py runserver 8001
```

Its site is then available at:

```text
http://127.0.0.1:8001/
```

Always run commands from the project directory whose `manage.py` you intend to use.

## 14. Learn Django by Tracing the Request

When you open a URL, follow this path:

```text
Browser request
    -> root urls.py
    -> app urls.py
    -> view function
    -> model or form logic
    -> template
    -> static and media assets
    -> HTTP response
```

Practice tracing one feature at a time:

1. Find its URL in the app's `urls.py`.
2. Find the view named by that URL.
3. Identify the model query or form validation.
4. Find the template returned by the view.
5. Check the template's `{% url %}` and `{% static %}` references.
6. Test the page while watching the server terminal.

This habit makes errors easier to localize and builds a strong understanding of Django's architecture.

## 15. A Geek-Level Learning Path

Use the commands above as experiments rather than memorized recipes:

1. Change one model field and observe `makemigrations`.
2. Read the generated migration and inspect it with `sqlmigrate`.
3. Query the model in `manage.py shell`.
4. Trace a list page from URL to view to template.
5. Add a test for the view and run only that app's tests.
6. Break a template URL intentionally, read the traceback, and repair it.
7. Run `check --deploy` and resolve one security advisory at a time.
8. Run `collectstatic`, inspect the manifest, and compare source versus generated assets.
9. Use Git diff to understand every line before committing.

Useful focused test commands after tests are added:

```powershell
python manage.py test students
python manage.py test courses
python manage.py test students.tests.StudentViewTests
python manage.py test students.tests.StudentViewTests.test_student_list_requires_login
```

The goal is not to run many commands; it is to understand what each command proves about the application.

**Previous:** [detail.md](detail.md) | **Next:** [django_orm_practice.md](django_orm_practice.md) | **All Guides:** [README.md](README.md)

## 16. Recommended Command Sequence

For ordinary daily work, this is the most useful short sequence:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django
.\venv\Scripts\Activate.ps1
cd myproject
python manage.py check
python manage.py runserver
```

For a model change:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

For a deployment-style check:

```powershell
python manage.py check --deploy
python manage.py collectstatic --noinput
python manage.py runserver --insecure
```

Keep the server terminal visible while developing. The traceback, request path, and line number usually tell you where the problem begins.
