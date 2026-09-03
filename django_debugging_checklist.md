# Django Debugging Checklist

Use this checklist whenever the Django server starts but a page, form, API, asset, or database operation misbehaves. Start at the first visible symptom and move through the request path in order. Use [statuscodes.md](statuscodes.md) to understand the HTTP result before following the relevant branch. Do not change several files at once; make one small change, reload, and check whether the error changed.

## 1. Start With the Exact Symptom

Write down four facts before editing anything:

- The exact URL or action that failed.
- The HTTP status code, such as `404`, `403`, `500`, or `302`.
- The exact error text shown in the browser or terminal.
- Whether the problem happens for an anonymous user, a logged-in user, or both.

Keep the development server terminal visible. The browser's error page is often only a summary; the terminal traceback normally contains the real exception, file name, line number, and failing code.

## 2. Confirm the Correct Project and Environment

The active learning project is `myproject/`. Its `manage.py` is inside that directory.

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django
.\venv\Scripts\Activate.ps1
cd myproject
python -c "import sys; print(sys.executable)"
python -m django --version
python manage.py check
```

The Python executable should be inside the repository's `venv\Scripts\` directory. If Django or a package cannot be imported, the wrong interpreter or an inactive virtual environment is usually the first thing to check.

For the separate portfolio project, use its own directory and settings:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\portfolio
python manage.py check
```

Always confirm which `manage.py` you are running. A correct command in the wrong project can produce confusing settings, database, or URL results.

## 3. Run the Server and Read the Traceback

Start the server from the correct project directory:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
python manage.py runserver
```

Reload the failing page and read the newest traceback from top to bottom. Find the first traceback line that points into your own project, such as:

```text
C:\...\myproject\students\views.py, line 42, in student_lists
```

That is usually the best starting file. Lines inside `django\` or `site-packages\` describe the framework's response to the problem; the first line in your app normally identifies where your code sent invalid data or called something incorrectly.

Useful commands while diagnosing:

```powershell
python manage.py check
python manage.py showmigrations
python manage.py test
python manage.py runserver
```

With `DEBUG=True`, Django displays detailed error pages in the browser. With `DEBUG=False`, the browser intentionally shows a generic 500 page, so inspect the server terminal or deployment logs for the traceback.

## 4. Trace the Request in This Order

For a normal Django page, follow this path:

```text
Browser request
    -> project urls.py
    -> app urls.py
    -> view function or class
    -> form or serializer validation
    -> model/database query
    -> template
    -> static/media assets
    -> HTTP response
```

Check the files in this order:

1. `myproject/myproject/urls.py` - Is the app included under the expected prefix?
2. `app/urls.py` - Does the path match the browser URL and point to the correct view?
3. `app/views.py` - Does the view receive the expected parameters and return a response?
4. `app/forms.py` or `serializers.py` - Is submitted or serialized data valid?
5. `app/models.py` - Do field names, relationships, and queries match the schema?
6. `app/Templates/app/page.html` - Does the template use the correct context and URL names?
7. `static/` and `media/` - Do CSS, JavaScript, images, and uploads exist and resolve?

Do not start by opening every file. Let the status code and traceback select the first file to inspect.

## 5. Error Triage by Status Code

### `404 Not Found`

Check routing first:

- Is the URL spelled correctly?
- Is the app included in the project `urls.py`?
- Is the path present in the app `urls.py`?
- Does the trailing slash match the configured route?
- Is the requested object ID or slug valid?
- Did `get_object_or_404` intentionally reject a missing record?

Search for the route and name:

```powershell
rg "student_details|course_lists|profile" myproject -g "*.py" -g "*.html"
```

For a URL such as `/students/student-details/4/`, verify that the route contains `<int:pk>` and that the view accepts `pk` with the same name.

### `403 Forbidden`

Check permissions and security protection:

- Is the user allowed to access the view?
- Is `@login_required` redirecting or is a permission check denying access?
- Is a POST form missing `{% csrf_token %}`?
- Is the CSRF origin or trusted-origin configuration correct?
- Is the request being blocked by a web server or reverse proxy?

For form submissions, confirm the form contains:

```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```

### `302 Redirect` When You Expected the Page

A redirect is often correct behavior. Check the `Location` header and then ask:

- Did `login_required` send an anonymous user to the login page?
- Did a successful form submission redirect to a list page?
- Did an authenticated user get redirected away from login or registration?
- Is a URL name redirect pointing to the intended app and view?

### `500 Internal Server Error`

Read the terminal traceback. Then classify the final exception:

- `TemplateDoesNotExist` -> template path or template directory.
- `NoReverseMatch` -> `{% url %}` name or arguments.
- `VariableDoesNotExist` or `KeyError` -> context name mismatch.
- `AttributeError` -> object or variable is not what the code expects.
- `TypeError` -> wrong function arguments or data type.
- `IntegrityError` -> database constraint, duplicate, or missing required relation.
- `OperationalError` -> database or migration problem.
- `ValidationError` -> invalid model/form data.
- `NameError` or `ImportError` -> missing import or circular import.
- `ValueError: Missing staticfiles manifest entry` -> run `collectstatic` and inspect static paths.

### `200` But the Page Looks Wrong

Check the view context, template inheritance, CSS/JavaScript loading, and browser developer tools. A successful status only proves that a response was returned; it does not prove the data or layout is correct.

## 6. Check `urls.py`

### Project URL Checklist

Open `myproject/myproject/urls.py` and confirm:

- The app is imported with `include`.
- The prefix is spelled correctly.
- The app URL file exists.
- Media URLs are only added for local debug mode.

Example:

```python
path('students/', include('students.urls')),
```

### App URL Checklist

Open the relevant app's `urls.py` and confirm:

- `from . import views` is present.
- The view name exists in `views.py`.
- Dynamic parameter names match the view signature.
- `app_name` matches the namespace used in templates and redirects.
- URL names are unique within the app.
- The browser URL includes the required trailing slash when configured.

Example:

```python
path('student-details/<int:pk>/', views.student_details, name='student_details'),
```

This route must call a view such as `student_details(request, pk)`.

## 7. Check `views.py`

Open the view named by the URL and inspect it in this order:

1. Are all imported functions, models, forms, and decorators available?
2. Are request parameters named the same as the URL parameters?
3. Does the view handle the correct HTTP methods?
4. Are POST values present and validated?
5. Does the database query use real model fields?
6. Does the context use the names expected by the template?
7. Does every path return an `HttpResponse`, `render`, or `redirect`?
8. Do redirects use valid namespaced URL names?
9. Should the view require `@login_required`?
10. Should delete or edit actions require an additional permission check?

A useful temporary inspection is:

```python
print(request.method)
print(request.POST)
print(context)
```

Remove temporary prints after diagnosing the issue. Do not print passwords, secret keys, uploaded private data, or authentication tokens.

For object pages, prefer this pattern:

```python
from django.shortcuts import get_object_or_404

student = get_object_or_404(Student, pk=pk)
```

It gives a clear 404 instead of allowing a missing object to cause an unrelated attribute error.

## 8. Check `models.py` and the Database

When data is missing, duplicated, or rejected, inspect the model first:

- Does the field name match the view, form, template, and query?
- Is the field required, nullable, or allowed to be blank?
- Is the value the correct type, such as a date or integer?
- Is a field marked `unique=True` causing a duplicate error?
- Does a foreign key point to the correct app and model?
- Is `on_delete` behavior appropriate?
- Does a many-to-many relation require `.add()` or `.set()` after saving?
- Does the database contain the record being requested?

After model changes:

```powershell
python manage.py check
python manage.py makemigrations
python manage.py showmigrations
python manage.py migrate
```

If Django says a table does not exist, migrations are usually missing or unapplied. If Django says no changes are detected but the database is wrong, verify that the edited app is in `INSTALLED_APPS` and that you are using the correct database and project.

Inspect records with the Django shell:

```powershell
python manage.py shell
```

```python
from students.models import Student
Student.objects.count()
Student.objects.all()
Student.objects.filter(status='active')
exit()
```

For relationships:

```python
from courses.models import Course
course = Course.objects.first()
course.instructor
course.enrolled_students.all()
```

Do not delete or recreate the database to fix an error until you understand the data loss involved.

## 9. Check `forms.py`

For a form that does not submit or displays errors:

- Is the form instantiated with `request.POST` on POST?
- Is `request.FILES` passed for file uploads?
- Does the HTML form use `method="post"`?
- Does the form include `{% csrf_token %}`?
- Does a file-upload form use `enctype="multipart/form-data"`?
- Does the form's `Meta.fields` include the intended fields?
- Are required fields supplied?
- Is the view checking `form.is_valid()` before saving?
- Are errors rendered in the template?
- Does the form's model match the object being edited?

Recommended pattern:

```python
if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('home:profile')
else:
    form = ProfileForm(instance=profile)
```

To see validation details during development:

```python
print(form.errors)
```

For a form that appears to do nothing, check whether validation is failing silently because the template never renders `form.errors`.

## 10. Check `serializers.py` for API Work

This repository currently uses Django template views rather than a serializer-based API. If you later add Django REST Framework, inspect `serializers.py` when JSON data is missing, rejected, or incorrectly formatted.

Check:

- Is `djangorestframework` installed and in `INSTALLED_APPS`?
- Does the serializer reference the correct model?
- Are the field names correct?
- Are read-only and required fields configured intentionally?
- Does nested relationship data need a custom `create()` or `update()` method?
- Does the view use `serializer.is_valid()` before `save()`?
- Are serializer errors returned or displayed?
- Is the request using the correct content type, usually `application/json`?

Typical validation pattern:

```python
serializer = StudentSerializer(data=request.data)
if serializer.is_valid():
    serializer.save()
else:
    print(serializer.errors)
```

Trace an API request through `urls.py`, API view or viewset, serializer, model, and response format in that order.

## 11. Check Templates and HTML

For `TemplateDoesNotExist`, inspect:

- The exact template string in `render()`.
- The actual capitalization of directories and files.
- Whether the template is inside an app template directory discovered by `APP_DIRS`.
- Whether the project-level template directory matches `TEMPLATES['DIRS']`.
- Whether `{% extends %}` points to the correct base template.

For template rendering problems, inspect:

- Does the context key in the view match the variable in the template?
- Does `{% url %}` use the correct namespace and URL name?
- Does a dynamic URL receive all required arguments?
- Is `{% load static %}` present before `{% static %}` is used?
- Are template tags and filters spelled correctly?
- Does a loop handle an empty queryset?
- Are missing values expected to be blank, or should the view reject them?

Search template references:

```powershell
rg "extends|include|url |static|csrf_token|form\.errors" myproject -g "*.html"
```

For a `NoReverseMatch` error, copy the failing URL name from the traceback and search for its definition and every use:

```powershell
rg "name=['\"]course_lists|courses:course_lists" myproject
```

## 12. Check Static Files, JavaScript, and Media

### CSS and JavaScript

If styles or scripts do not load:

- Confirm `{% load static %}` is in the base template.
- Confirm the source file exists under `myproject/static/`.
- Confirm the path in `{% static 'css/style.css' %}` is correct.
- Open browser developer tools and inspect the Network tab.
- Check whether the asset returns `200` or `404`.
- Check the browser Console tab for JavaScript errors.
- Check whether a CSS selector or JavaScript page condition is wrong.

Useful commands:

```powershell
Test-Path .\static\css\style.css
python manage.py findstatic css/style.css --verbosity 2
```

### `DEBUG=False` Static Errors

This project uses WhiteNoise's compressed manifest storage. If the terminal reports:

```text
ValueError: Missing staticfiles manifest entry for 'css/style.css'
```

run:

```powershell
python manage.py collectstatic --noinput
Test-Path .\staticfiles\staticfiles.json
```

The source asset belongs in `static/`; generated hashed and compressed files belong in `staticfiles/`. Do not manually edit generated static files.

### Media Uploads

For profile-picture or other upload problems, check:

- The form includes `enctype="multipart/form-data"`.
- The view passes `request.FILES`.
- The model field has the intended `upload_to` path.
- `MEDIA_ROOT` exists and is writable.
- `MEDIA_URL` is configured.
- Debug-only media URL serving is present for local development.
- Production uses dedicated media storage rather than Django's development server.

## 13. Check Authentication and Sessions

For login, registration, logout, or protected-page problems:

- Is `django.contrib.auth` installed?
- Is `django.contrib.sessions` installed?
- Is `SessionMiddleware` enabled?
- Is `AuthenticationMiddleware` enabled after session middleware?
- Does the login form use the correct authentication form?
- Does the view call `login(request, user)` after valid credentials?
- Does logout call `logout(request)`?
- Is `LOGIN_URL` a valid URL?
- Does `@login_required` protect the intended view?
- Has the user completed registration and password validation?
- Are you testing with the same browser session?

Use the Django shell to inspect a user without exposing passwords:

```powershell
python manage.py shell
```

```python
from django.contrib.auth.models import User
user = User.objects.get(username='your_username')
user.is_active
user.is_staff
user.is_superuser
exit()
```

A redirect to login is usually expected for an anonymous request to a protected view. It is only a bug if the user is already authenticated or the redirect target is wrong.

## 14. Check Admin and Permissions

For admin problems:

- Does `/admin/` load?
- Was a superuser created with `createsuperuser`?
- Is the user active, staff, and using the correct password?
- Are models registered in the app's `admin.py`?
- Are migrations applied?
- Do admin fields match the current model?

Commands:

```powershell
python manage.py createsuperuser
python manage.py changepassword username
python manage.py check
```

Authentication only proves who the user is. Authorization determines what that user is allowed to do. Add explicit permission checks before exposing edit or delete actions to ordinary users.

## 15. Check Settings and Environment Values

For startup errors, deployment errors, or differences between machines, inspect `myproject/myproject/settings.py`:

- Is `DJANGO_SETTINGS_MODULE` pointing to the correct project?
- Is the expected app in `INSTALLED_APPS`?
- Is the database path correct?
- Is the template directory correct?
- Are `STATIC_URL`, `STATIC_ROOT`, and `STATICFILES_DIRS` correct?
- Are `MEDIA_URL` and `MEDIA_ROOT` correct?
- Is the required middleware installed?
- Is the email backend appropriate for the environment?
- Is `DEBUG` set intentionally?
- Does `ALLOWED_HOSTS` include the host used by the browser?

Check deployment advisories:

```powershell
python manage.py check --deploy
```

For local development, `DEBUG=True` provides useful tracebacks. For deployment, use environment variables for secrets and settings rather than committing credentials or machine-specific values.

## 16. Common Python Errors

### `NameError`

A variable or function name does not exist in the current scope. Check spelling, indentation, and imports.

### `ImportError` or `ModuleNotFoundError`

Check the import path, app name, package installation, and active virtual environment. Avoid importing a module from a path that does not belong to the current project.

### `AttributeError`

The object does not have the attribute being accessed. Print or inspect the object's type and compare the attribute with the model or form definition.

### `TypeError`

The function received the wrong number or type of arguments. Compare the call with the function signature and the URL parameter names.

### `IndentationError` or `SyntaxError`

Run:

```powershell
python -m compileall -q myproject
```

Then open the file and line reported by Python. Fix indentation or punctuation before investigating higher-level behavior.

## 17. Common Database Errors

### `no such table`

Run:

```powershell
python manage.py showmigrations
python manage.py migrate
```

Then verify that the app is installed and that the command is using the intended project.

### `UNIQUE constraint failed`

A value marked unique already exists. Query the database and choose a new value or handle the duplicate with form validation.

### `NOT NULL constraint failed`

A required model field received no value. Check the HTML input name, POST key, form fields, model defaults, and view assignment.

### `FOREIGN KEY constraint failed`

The related object does not exist or is being deleted in an invalid order. Check the foreign-key value and `on_delete` behavior.

### Migration conflict or unexpected migration

Do not delete migrations blindly. First run:

```powershell
python manage.py showmigrations --plan
python manage.py makemigrations --check --dry-run
```

Read the conflicting migration files and understand which schema changes they represent before resolving them.

## 18. Browser Developer Tools

Use browser developer tools alongside the terminal:

- **Console**: JavaScript exceptions and client-side errors.
- **Network**: request URL, status code, redirects, response body, CSS, JavaScript, and image failures.
- **Application/Storage**: cookies and session state.
- **Elements**: rendered HTML and active CSS rules.
- **Sources**: browser-loaded JavaScript and source locations.

For a form problem, inspect the Network request and confirm the method, form data, CSRF cookie, response status, and redirect target.

For a layout problem, inspect the element in Elements and temporarily disable CSS rules to identify the responsible selector.

## 19. A Small Reproduction Method

When the error is unclear, reduce it to one request or one shell query:

```powershell
python manage.py shell
```

```python
from django.test import Client
client = Client()
response = client.get('/')
response.status_code
response.url if hasattr(response, 'url') else None
exit()
```

For a production-style request after collecting static files:

```powershell
python manage.py collectstatic --noinput
```

Then test the server with `DEBUG=False` and inspect its terminal logs. Change only one variable at a time: URL, authentication state, submitted data, database record, or setting.

## 20. Before Asking for Help

Prepare this information:

- The command used to start the server.
- The exact URL or action.
- The HTTP status code.
- The complete traceback from the first project line onward.
- The file and line you think is failing.
- What you expected to happen.
- What actually happened.
- The most recent code or migration change.
- The output of `python manage.py check`.
- Whether `DEBUG` is `True` or `False`.

Never share secret keys, passwords, session cookies, API tokens, or private user data in an error report.

## 21. Daily Debugging Routine

Use this order every time:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django
.\venv\Scripts\Activate.ps1
cd myproject
python manage.py check
python manage.py runserver
```

Then:

1. Reproduce exactly one error.
2. Read the newest terminal traceback.
3. Open the first project file and line named by the traceback.
4. Trace backward through the request path: template, view, URL, model, form, or serializer.
5. Inspect the browser Network and Console tabs.
6. Make one small fix.
7. Reload or rerun the smallest relevant test.
8. Run `python manage.py check` again.
9. Record the cause and fix in your notes.

## 22. Final Pre-Push Checklist

Before pushing changes to GitHub:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py collectstatic --noinput
cd ..
git diff --check
git status --short
git diff --stat
```

Confirm manually:

- The changed files are intentional.
- No passwords, secret keys, databases, media uploads, or virtual-environment files are staged.
- New migrations are included when models changed.
- New templates and static files are in the correct source directories.
- The main page, login, registration, and changed feature work in the browser.
- You understand every line in the diff before committing.

The most valuable debugging habit is to follow evidence: exact request, exact status, exact traceback, first project line, one small change, one focused verification.
