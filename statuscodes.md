# HTTP Status Codes for Django

An HTTP status code is the short numeric result sent by a web server after a browser or API client makes a request. It tells you whether the request succeeded, needs another action, or failed. The number does not always identify the root cause by itself, but it tells you where to begin looking.

## The Five Status Code Groups

| Group | Range | Meaning | First place to inspect |
| --- | --- | --- | --- |
| `1xx` | 100-199 | Informational response | Browser, proxy, or connection behavior |
| `2xx` | 200-299 | Request succeeded | Response data, template, or frontend behavior |
| `3xx` | 300-399 | Redirect or cache instruction | `Location` header, authentication, URL logic |
| `4xx` | 400-499 | Client request is invalid or not allowed | URL, request data, permissions, CSRF, authentication |
| `5xx` | 500-599 | Server failed while handling a valid-looking request | Terminal traceback, view, template, model, settings, deployment logs |

## The Most Important Rule

Do not debug from the status code alone. Always collect:

1. The exact URL and HTTP method.
2. The status code.
3. The terminal traceback or server log.
4. The first line in your own project named by the traceback.
5. The recent change that happened before the error.

Run the server from the directory containing `manage.py`:

```powershell
cd C:\Users\USER\Desktop\MMAMC\Django\myproject
.\..\venv\Scripts\Activate.ps1
python manage.py runserver
```

With `DEBUG=True`, Django displays useful exception details during local development. With `DEBUG=False`, the browser normally shows only a generic error page, so read the terminal or hosting-platform logs.

## `1xx` Informational Responses

These are temporary protocol messages. Django developers rarely need to debug them directly.

### `100 Continue`

The client may continue sending a request body. It can appear during large uploads or when a client uses the `Expect` request header.

Check the reverse proxy, upload size limits, and client behavior if an upload stops after this response.

### `101 Switching Protocols`

The server is switching protocols, such as upgrading to WebSocket communication. Standard Django template pages normally do not use this response.

## `2xx` Successful Responses

A `2xx` code means the server completed the request successfully. It does not guarantee that the page contains the right data or that JavaScript and CSS work.

### `200 OK`

The page, form response, or API request succeeded.

If the page looks wrong even though it returns `200`, inspect:

- The view context.
- The rendered HTML.
- Browser Console errors.
- Network requests for CSS, JavaScript, images, and API data.
- Template conditions and loops.
- Database records returned by the view.

### `201 Created`

A new resource was created successfully. This is common for REST API `POST` requests. A normal Django form often returns `302` after saving and redirecting instead.

Inspect the response body or `Location` header to confirm where the new resource can be found.

### `202 Accepted`

The server accepted the request but has not finished processing it. This is used for background jobs or asynchronous work.

If the result never appears, inspect the task queue, worker process, job logs, and database state.

### `204 No Content`

The request succeeded and intentionally returned no response body. This is common for successful delete or update API requests.

A browser page that appears blank may be correct if the endpoint is designed to return `204`. A template view should normally return `200` or redirect instead.

## `3xx` Redirect Responses

A `3xx` response tells the client to use another URL or a cached version. Redirects are not automatically errors.

### `301 Moved Permanently`

The URL has permanently moved. Browsers and search engines may cache this result.

Check URL configuration, proxy rules, and whether a permanent redirect was intended. During development, stale browser cache can make a changed redirect appear to continue happening.

### `302 Found`

The server is redirecting temporarily. This is common in Django after:

- A successful form submission.
- Login or logout.
- `@login_required` sending an anonymous user to the login page.
- A view calling `redirect()`.

Inspect the `Location` header. If the redirect is unexpected, check the view's `redirect()` call, `LOGIN_URL`, `LOGIN_REDIRECT_URL`, authentication state, and URL names.

### `303 See Other`

The client should retrieve the result from another URL, often after a `POST`. It supports the Post/Redirect/Get pattern and helps prevent accidental form resubmission.

### `304 Not Modified`

The browser can use its cached copy because the resource has not changed. This is normally correct behavior for static files.

If old CSS or JavaScript remains visible, hard-refresh the browser, inspect cache headers, and run `collectstatic` when using production static storage.

### `307 Temporary Redirect`

The client should repeat the request at another URL while preserving the HTTP method. A `POST` remains a `POST`.

### `308 Permanent Redirect`

The client should permanently use another URL while preserving the HTTP method. Check carefully before using this because clients may cache it.

## `4xx` Client and Request Errors

A `4xx` response means the server understood the request but could not fulfill it because of the URL, data, authentication, permission, or request format.

### `400 Bad Request`

The request is malformed or invalid before normal view processing can finish.

Common causes:

- Invalid request syntax.
- Malformed JSON.
- Invalid host header or host configuration.
- Bad proxy or web-server rewriting.
- Oversized or malformed request data.

Check the terminal, web-server log, request headers, `ALLOWED_HOSTS`, JSON body, and proxy configuration.

### `401 Unauthorized`

The client must authenticate. This status is especially common in APIs using token or session authentication.

In a normal Django template application, anonymous users are often redirected with `302` instead of receiving `401`. Check authentication middleware, API permissions, credentials, and the `Authorization` header.

### `403 Forbidden`

The server understood the request but refuses to allow it.

Common Django causes:

- Missing or invalid CSRF token on a `POST` request.
- User lacks permission.
- User is authenticated but not staff or not authorized.
- Host or origin is not trusted.
- Web-server access rules deny the request.

Check:

```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```

Then inspect `@login_required`, permission checks, `CSRF_TRUSTED_ORIGINS`, cookies, and server logs.

### `404 Not Found`

The requested URL or object does not exist.

Check in this order:

1. Browser URL spelling and trailing slash.
2. Project `myproject/urls.py` app prefix.
3. App `urls.py` path and URL name.
4. Dynamic parameters such as `<int:pk>`.
5. View parameter names.
6. Record existence in the database.
7. Template links using `{% url %}`.

For an object detail URL such as `/students/student-details/4/`, confirm that the route accepts an integer and the view looks up the same primary key.

Useful search:

```powershell
rg "student-details|student_details" myproject -g "*.py" -g "*.html"
```

A deliberate `get_object_or_404()` result is also a `404`; that usually means the URL is valid but the requested record is missing.

### `405 Method Not Allowed`

The URL exists, but the view does not accept the HTTP method used.

Examples:

- A view accepts `POST` but the client sends `GET`.
- A form submits to a view that only handles display logic.
- An API endpoint permits `GET` but rejects `DELETE`.

Check the form's `method`, the client request, class-based view methods, API view permissions, and the view's `request.method` branches.

### `406 Not Acceptable`

The server cannot return a representation matching the client's requested format. This is more common in APIs using the `Accept` header than in ordinary Django templates.

Check content negotiation, serializer formats, and the `Accept` header.

### `408 Request Timeout`

The server waited too long for the request. Check slow clients, upload size, proxy timeout settings, and network stability.

### `409 Conflict`

The request conflicts with the current state of the resource.

Common examples are duplicate unique values, concurrent edits, or attempting an operation in the wrong state. Inspect database constraints and application state. A Django `IntegrityError` may be returned as a `409` by an API, although a basic unhandled view may produce `500` instead.

### `413 Content Too Large`

The request body or uploaded file exceeds a configured limit.

Check browser upload size, Django settings, reverse-proxy limits, web-server limits, and media storage configuration.

### `415 Unsupported Media Type`

The server does not accept the request's content type.

Common API causes:

- Sending form data where JSON is required.
- Sending JSON without `Content-Type: application/json`.
- Uploading a file without `multipart/form-data`.

For file forms, use:

```html
<form method="post" enctype="multipart/form-data">
```

### `422 Unprocessable Content`

The request format is understood, but the values fail validation. Django forms, ModelForms, and serializers commonly expose this kind of validation failure in API-style applications.

Inspect `form.errors` or `serializer.errors`, required fields, field types, choices, dates, and unique constraints.

### `429 Too Many Requests`

The client sent too many requests in a time period. Check rate limiting, repeated JavaScript requests, retry loops, login attempts, and proxy or hosting rules.

## `5xx` Server Errors

A `5xx` response means the server failed while processing the request. Begin with the terminal traceback or deployment log, not with the browser page.

### `500 Internal Server Error`

This is the most general server failure. In Django, common underlying exceptions include:

| Exception | Usually inspect |
| --- | --- |
| `TemplateDoesNotExist` | Template path, capitalization, `TEMPLATES`, `APP_DIRS` |
| `NoReverseMatch` | `{% url %}`, `redirect()`, URL name, arguments |
| `ValueError` for static manifest | `collectstatic`, `STATIC_ROOT`, asset path |
| `AttributeError` | Object type, model field, context variable |
| `TypeError` | Function arguments, URL parameters, data types |
| `NameError` | Spelling, scope, missing variable |
| `ImportError` | Import path, installed package, circular imports |
| `IntegrityError` | Unique, null, foreign-key, or many-to-many constraints |
| `OperationalError` | Migrations, database path, missing table |
| `ValidationError` | Form, serializer, model field values |
| `PermissionDenied` | User permissions and authorization logic |

Trace it in this order:

1. Read the last exception line.
2. Find the first traceback frame inside your project.
3. Open that file and line.
4. Follow the data into the view, form, serializer, model, or template.
5. Reproduce one request after making one focused change.

For this project, a common production-mode static error is:

```text
ValueError: Missing staticfiles manifest entry for 'css/style.css'
```

Fix it with:

```powershell
python manage.py collectstatic --noinput
```

### `501 Not Implemented`

The server does not support the requested functionality. Check whether the request is reaching the intended Django application or an incomplete proxy/server configuration.

### `502 Bad Gateway`

A proxy or gateway received an invalid response from the upstream application.

Check whether the Django/Gunicorn/Uvicorn process is running, the upstream host and port are correct, and the application logs show startup or import errors.

### `503 Service Unavailable`

The server is temporarily unable to handle the request.

Common causes:

- Application process is stopped.
- Deployment is restarting.
- Database or external service is unavailable.
- Health check failed.
- Server is overloaded.

Check process status, deployment logs, health checks, database availability, and resource usage.

### `504 Gateway Timeout`

A proxy waited too long for the application to respond.

Check slow database queries, infinite loops, external API calls, file processing, worker timeouts, and reverse-proxy timeout settings. Reproduce the request locally and inspect the server timing.

## Status Code and File Map

| Symptom | First file or place | Then inspect |
| --- | --- | --- |
| `404` page | `urls.py` | Route parameters, view, database object |
| `302` unexpected redirect | `views.py` or `settings.py` | `LOGIN_URL`, `redirect()`, authentication |
| `403` form failure | HTML template | CSRF token, form method, permissions |
| `405` method failure | `views.py` | Form method, API method, class-based view |
| `422` validation failure | `forms.py` or `serializers.py` | `errors`, required fields, model constraints |
| `500` during rendering | Traceback first project line | Template, context, `{% url %}`, `{% static %}` |
| `500` during save | `views.py`, `forms.py`, or `models.py` | Migrations, constraints, submitted values |
| CSS/JS `404` | Browser Network tab | `{% static %}`, source static directory, `collectstatic` |
| Login loop | `settings.py`, `accounts/views.py` | Sessions, middleware, redirects, cookies |
| API response wrong | API view and `serializers.py` | Request body, serializer fields, response status |
| `502`, `503`, `504` | Hosting/deployment logs | Process, proxy, worker, database, timeouts |

## Browser Tools for Status Codes

Open browser developer tools and use the Network tab:

- **Status**: the HTTP result.
- **Request URL**: whether the browser called the intended route.
- **Method**: `GET`, `POST`, `PUT`, `PATCH`, or `DELETE`.
- **Response headers**: redirects, caching, content type, and cookies.
- **Response body**: validation errors or server messages.
- **Timing**: slow database or external requests.

Use the Console tab for JavaScript errors. A page can return `200` while JavaScript later fails and prevents a button, table, or form from working.

## Command-Line Checks

Run these from `myproject/`:

```powershell
python manage.py check
python manage.py check --deploy
python manage.py showmigrations
python manage.py makemigrations --check --dry-run
python manage.py findstatic css/style.css --verbosity 2
python manage.py test
```

Search route names, templates, and settings:

```powershell
rg "path\(|name=|redirect\(|render\(" myproject -g "*.py"
rg "extends|include|url |static|csrf_token" myproject -g "*.html"
rg "DEBUG|ALLOWED_HOSTS|STATIC|MEDIA|LOGIN" myproject/myproject/settings.py
```

## A Simple Decision Tree

```text
Did the server start?
    No  -> Read startup traceback -> imports -> settings -> installed packages
    Yes -> Does the request return 2xx?
              Yes -> Inspect content, template context, browser Console, and assets
              No  -> Is it 3xx?
                        Yes -> Inspect Location, login, and redirect logic
                        No  -> Is it 4xx?
                                  Yes -> Check URL, method, CSRF, auth, permissions, and input
                                  No  -> Is it 5xx?
                                            Yes -> Read terminal traceback and first project line
                                            No  -> Inspect proxy, hosting, and browser Network details
```

## Final Rule of Thumb

- `2xx`: the request completed; inspect the result if it is wrong.
- `3xx`: follow the redirect and inspect why it happened.
- `4xx`: inspect the request, URL, method, permissions, or submitted data.
- `5xx`: inspect the server traceback, starting at the first line in your code.

Keep this file beside [django_debugging_checklist.md](django_debugging_checklist.md). Use the status code to choose the branch, then use the checklist to trace the request to the responsible file.
