# Review and Learning Guide

This guide records the work completed during the final review of the MMAMC Django workspace. It is written as a study path: understand the problem, inspect the owning code, make a small fix, validate it, and only then prepare a commit. Read [track.md](track.md) for the detailed production-settings explanation.

## 1. Workspace Scope

The workspace contains two independent Django projects:

- `myproject/` is the main academic management application.
- `portfolio/` is a separate portfolio application.

The unused `portfolio/students/` app was removed because the portfolio does not need student management or student records. The portfolio database was checked and contains no student tables.

The main project contains the `home`, `accounts`, `students`, `teachers`, and `courses` apps. The repository also contains learning notebooks, Markdown guides, SQLite databases, static assets, uploaded media, and an archive file.

The final review intentionally kept the two Django projects separate. A passing check in `myproject/` does not prove that `portfolio/` works, so each project has its own check commands.

## 2. What Was Built

A staff-only custom admin dashboard was added at `/admin-dashboard/`.

The dashboard:

- Uses `@staff_member_required` so ordinary authenticated users cannot open it.
- Counts students, teachers, and courses.
- Shows active student, teacher, and course counts.
- Displays the five most recently created records in each area.
- Links to existing detail pages and the built-in Django admin.
- Adds a staff-only navigation link.

The built-in Django admin was already registered for `Profile`, `Student`, `Teacher`, and `Course`, so the custom dashboard complements it rather than replacing it.

## 3. Problems Found and Fixed

### Security and Configuration

The original settings contained a hard-coded development secret key, `DEBUG = True`, and a wildcard host list. The settings now read these values from environment variables with local-development defaults.

Production controls are also configurable:

- `DJANGO_SECURE_SSL_REDIRECT`
- `DJANGO_SESSION_COOKIE_SECURE`
- `DJANGO_CSRF_COOKIE_SECURE`
- `DJANGO_SECURE_HSTS_SECONDS`
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `DJANGO_SECURE_HSTS_PRELOAD`

For deployment, use a real random secret key, explicit hosts, HTTPS, secure cookies, and an appropriate HSTS policy.

### Authentication and Authorization

The login view originally trusted the `next` query parameter. It now uses Django's `url_has_allowed_host_and_scheme` helper, which prevents redirects to an external host.

Delete operations now require both:

- an authenticated user; and
- an HTTP POST request containing a CSRF token.

A browser GET request must never silently delete a record.

### Data Validation

Student, teacher, and course create/edit views now use `ModelForm` classes. Forms validate required fields, data types, unique fields, dates, and model choices before saving.

This is safer than assigning every value directly from `request.POST`.

The student edit bug that assigned to the nonexistent `enrolled_course` field was removed. Course, teacher, and student detail pages now point to the correct edit and delete routes.

### Reliability

A URL referenced `courses.views.course_display`, but that view was missing. The view was restored so Django could load the URL configuration.

Debug `print()` calls were removed from request handlers. Logs should not expose submitted form data or become accidental production output.

## 4. How to Review a Django Change

Use this local reasoning loop:

1. Identify the URL that exposes the behavior.
2. Follow it to the app URL file.
3. Follow the route to the view.
4. Inspect the model and form used by the view.
5. Inspect the template that submits or displays the data.
6. Check authentication, authorization, HTTP method, CSRF, and validation.
7. Run the cheapest focused test.
8. Run the broader project checks.
9. Inspect the diff and repository status before committing.

A useful hypothesis should be falsifiable. For example:

> The delete link is unsafe because it uses GET, so requesting its URL without a form submission may delete a database row.

A cheap check is to send a GET request to that URL and confirm the response is `405 Method Not Allowed` and the row still exists.

## 5. Testing Concepts Used

The new tests cover behavior rather than implementation details.

- Anonymous access to the admin dashboard redirects to login.
- A regular authenticated user is rejected from the staff dashboard.
- A staff user receives a successful dashboard response.
- An external login redirect falls back to the safe home page.
- A GET request cannot delete a student.
- A course form rejects missing required data.

The main project now reports five passing tests. The portfolio project currently has no discovered tests, so `Found 0 test(s)` means only that the test runner completed; it is not meaningful behavioral coverage.

## 6. Green-Signal Checklist

Before committing the main project, all of these should be true:

- `manage.py check` passes.
- `makemigrations --check --dry-run` reports no changes.
- `manage.py test` passes.
- Production-style representative requests return `200` where expected.
- `manage.py check --deploy` is clean with production environment variables.
- The same functional and deployment checks pass for the separate `portfolio/` project.
- Python compilation passes for both projects.
- Editor diagnostics show no relevant errors.
- `git diff --check` passes.
- `git status --short` contains only intended files.
- The diff has been read, including new untracked files.

The current code checks are green. Review `git status --short` before committing so only intended files are staged.

## 7. Commit and Push Safety

Do not use `git add .` until every untracked path has been reviewed. Prefer adding the intended paths explicitly.

A safe sequence is:

```powershell
git status --short
git diff --check
git add myproject README.md detail.md command.md review_and_learning.md
git diff --cached --check
git diff --cached --stat
git commit -m "Harden Django management workflows"
git status --short
git push origin <branch-name>
```

The push command changes the remote repository, so it should happen only after the user confirms the branch, commit, and remote are correct.

## 8. What to Learn Next

The next useful improvements are:

- Add tests for every create, edit, and delete workflow.
- Replace remaining raw HTML form markup with reusable form rendering where appropriate.
- Add authorization rules beyond `login_required`, such as staff or per-app permissions.
- Add pagination and query optimization for larger record lists.
- Add CI to run checks automatically on every pull request.
- Decide whether any future untracked files belong in the change before staging them.
