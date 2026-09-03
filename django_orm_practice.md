# Django ORM — Daily Practice Guide

A working reference and daily-practice log for Django ORM, built around the real `Course` model.

## The Model

```python
from django.db import models


class Course(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    SEMESTER_CHOICES = [
        ("Spring 2026", "Spring 2026"),
        ("Fall 2026", "Fall 2026"),
        ("Spring 2027", "Spring 2027"),
        ("Fall 2027", "Fall 2027"),
    ]

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    instructor = models.CharField(max_length=150)
    credits = models.PositiveIntegerField()
    duration = models.CharField(max_length=50)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
```

Key details worth remembering about this model, because they change how you query it:
- `code` is `unique=True` → `.get(code=...)` is always safe to use (never raises `MultipleObjectsReturned`).
- `status` and `semester` use `choices` → you query by the stored value (`"active"`, `"Spring 2026"`), and display the human-readable label with `get_status_display()` / `get_semester_display()`.
- `credits` and `capacity` are `PositiveIntegerField` → no negative values possible, safe with `__gt`, `__lt`, `Sum`, `Avg`, etc.
- `created_at`/`updated_at` are auto-managed — never set them manually; they update themselves on create/save.
- `instructor` is a plain `CharField`, **not** a `ForeignKey` — so there's no reverse relation like `instructor.courses`. If you later want efficient "all courses per instructor" queries or richer instructor data, this is a natural field to convert to `ForeignKey(Instructor, ...)`.

---

## Part 1 — Basic Retrieval

```python
# All rows
Course.objects.all()

# Count all rows
Course.objects.count()

# Filter by exact field value
Course.objects.filter(status="active")
Course.objects.filter(status="inactive")

# Count a filtered QuerySet
Course.objects.filter(status="active").count()

# Get ONE specific row — safe here since `code` is unique
Course.objects.get(code="CSC319")

# Get via filter (returns a QuerySet, never raises DoesNotExist)
Course.objects.filter(code="CSC319")
```

`.get()` vs `.filter()`:
- `.get()` returns a **model instance**. Raises `Course.DoesNotExist` if 0 matches, `Course.MultipleObjectsReturned` if 2+ matches.
- `.filter()` always returns a **QuerySet** — empty, one, or many. Never raises.

Since `code` is unique, `Course.objects.get(code="CSC319")` will never raise `MultipleObjectsReturned`. That guarantee disappears for non-unique fields like `department` or `instructor`.

---

## Part 2 — Choices Fields (`status`, `semester`)

```python
# Filter by the stored value (not the display label)
Course.objects.filter(status="active")
Course.objects.filter(semester="Spring 2026")

# Get the human-readable label from an instance
course = Course.objects.get(code="CSC319")
course.get_status_display()     # -> "Active"
course.get_semester_display()   # -> "Spring 2026"

# All courses for a given semester, active only
Course.objects.filter(semester="Fall 2026", status="active")

# Every distinct semester currently in use
Course.objects.values_list("semester", flat=True).distinct()
```

⚠️ Common mistake: filtering with the *display* label instead of the stored value —
`Course.objects.filter(status="Active")` silently returns nothing, because the stored value is lowercase `"active"`.

---

## Part 3 — Field Lookups

```python
# Case-insensitive exact match
Course.objects.filter(department__iexact="computer science")

# Contains / icontains
Course.objects.filter(name__icontains="data")
Course.objects.filter(instructor__icontains="sharma")

# Starts with / ends with
Course.objects.filter(code__startswith="CSC3")

# In a list
Course.objects.filter(code__in=["CSC316", "CSC319", "CSC321"])

# Numeric comparisons (credits, capacity)
Course.objects.filter(credits__gte=3)
Course.objects.filter(capacity__lt=40)
Course.objects.filter(credits__range=(2, 4))

# Date lookups (created_at / updated_at)
Course.objects.filter(created_at__year=2026)
Course.objects.filter(created_at__month=9)
Course.objects.filter(updated_at__gte="2026-08-01")

# Blank / non-blank description
Course.objects.filter(description__exact="")
Course.objects.exclude(description__exact="")
```

**Try it:** find every course taught by an instructor whose name contains "sharma" (case-insensitive), that's active, and has 3 or more credits.

---

## Part 4 — Ordering & Slicing

```python
Course.objects.order_by("code")                  # ascending
Course.objects.order_by("-created_at")            # newest first
Course.objects.order_by("department", "code")      # multi-field
Course.objects.order_by("-capacity")[:5]           # top 5 by capacity

Course.objects.order_by("code").first()
Course.objects.order_by("-created_at").first()      # most recently added course
```

---

## Part 5 — Q Objects (OR / NOT logic)

```python
from django.db.models import Q

# OR
Course.objects.filter(Q(department="Computer Science") | Q(semester="Fall 2026"))

# NOT
Course.objects.filter(~Q(status="active"))

# Combined: (CS OR IT) AND active
Course.objects.filter(
    Q(department="Computer Science") | Q(department="Information Technology"),
    status="active"
)
```

---

## Part 6 — Aggregation & Annotation

```python
from django.db.models import Count, Avg, Sum, Max, Min

# Whole-table summaries
Course.objects.aggregate(total_credits=Sum("credits"))
Course.objects.aggregate(avg_capacity=Avg("capacity"))
Course.objects.aggregate(max_credits=Max("credits"))

# Per-department course count
Course.objects.values("department").annotate(course_count=Count("id"))

# Per-semester course count, most popular semester first
Course.objects.values("semester").annotate(n=Count("id")).order_by("-n")

# Average capacity per department
Course.objects.values("department").annotate(avg_cap=Avg("capacity"))
```

`aggregate()` → one number/dict for the whole QuerySet.
`annotate()` → one value per row or per group; stays chainable and filterable afterward.

---

## Part 7 — F Expressions

```python
from django.db.models import F

# Compare fields against each other
Course.objects.filter(capacity__gt=F("credits") * 10)

# Bulk-increment a field safely (avoids read-modify-write race conditions)
Course.objects.filter(code="CSC319").update(capacity=F("capacity") + 5)
```

---

## Part 8 — Create, Update, Delete

```python
# Create
Course.objects.create(
    code="CSC401",
    name="Deep Learning",
    department="Computer Science",
    instructor="Dr. Thapa",
    credits=3,
    duration="15 weeks",
    semester="Fall 2026",
    capacity=40,
    status="active",
    description="Neural networks, CNNs, RNNs, and transformers."
)

# get_or_create — avoids IntegrityError from the unique `code`
course, created = Course.objects.get_or_create(
    code="CSC401",
    defaults={
        "name": "Deep Learning",
        "department": "Computer Science",
        "instructor": "Dr. Thapa",
        "credits": 3,
        "duration": "15 weeks",
        "semester": "Fall 2026",
        "capacity": 40,
    }
)

# Update a single instance (triggers auto_now on updated_at)
c = Course.objects.get(code="CSC401")
c.status = "inactive"
c.save()

# Bulk update — fast, but skips .save(), signals, and auto_now!
Course.objects.filter(department="Computer Science").update(status="active")
# Note: bulk .update() does NOT refresh `updated_at` unless set explicitly:
from django.utils import timezone
Course.objects.filter(department="Computer Science").update(status="active", updated_at=timezone.now())

# Delete
Course.objects.get(code="CSC401").delete()
Course.objects.filter(status="inactive").delete()
```

⚠️ Because `code` is `unique=True`, calling `.create()` twice with the same `code` raises `django.db.utils.IntegrityError`. Use `get_or_create()` or `update_or_create()` when you're not sure a row already exists.

```python
# update_or_create — create if missing, update if it exists
Course.objects.update_or_create(
    code="CSC401",
    defaults={"capacity": 45, "status": "active"}
)
```

---

## Part 9 — values() / values_list()

```python
Course.objects.values()                            # dicts, all fields
Course.objects.values("code", "name")               # dicts, selected fields
Course.objects.values_list("code")                  # tuples
Course.objects.values_list("code", flat=True)        # flat list of codes
Course.objects.values("department").distinct()       # unique departments
```

---

## Part 10 — Daily Practice Set

Write these yourself first, then check the hints.

1. All courses in "Spring 2026", ordered by code.
2. Number of courses per instructor.
3. All courses with more than 3 credits AND status "active".
4. All courses whose name contains "Web" (case-insensitive).
5. The single most recently created course.
6. Check (without loading all rows) whether any course has `capacity` over 100.
7. Total credits offered across every active course.
8. Every course NOT in the "Computer Science" department, using `exclude`.
9. Set all "Spring 2026" courses to "inactive" in a single query.
10. Get a flat, sorted list of every unique semester currently used.

<details>
<summary>Hints</summary>

```python
# 1
Course.objects.filter(semester="Spring 2026").order_by("code")

# 2
Course.objects.values("instructor").annotate(n=Count("id"))

# 3
Course.objects.filter(credits__gt=3, status="active")

# 4
Course.objects.filter(name__icontains="web")

# 5
Course.objects.order_by("-created_at").first()

# 6
Course.objects.filter(capacity__gt=100).exists()

# 7
Course.objects.filter(status="active").aggregate(total=Sum("credits"))

# 8
Course.objects.exclude(department="Computer Science")

# 9
Course.objects.filter(semester="Spring 2026").update(status="inactive")

# 10
Course.objects.values_list("semester", flat=True).distinct().order_by("semester")
```
</details>

---

## Quick Reference Table

| Goal | Method |
|---|---|
| All rows | `.all()` |
| Count | `.count()` |
| Filter (AND) | `.filter(a=1, b=2)` |
| Filter (OR) | `.filter(Q(a=1) \| Q(b=2))` |
| Exclude | `.exclude(a=1)` |
| One row, strict | `.get(code="CSC319")` |
| One row, safe | `.filter(code="CSC319").first()` |
| Human-readable choice | `instance.get_status_display()` |
| Unique values | `.values("field").distinct()` |
| Sort | `.order_by("field")` / `"-field"` |
| Limit | `[:n]` |
| Exists check | `.exists()` |
| Group + count | `.values("field").annotate(Count("id"))` |
| Whole-table summary | `.aggregate(Sum/Avg/Max/Min(...))` |
| Compare/update via field | `F("field")` |
| Create, safe on unique field | `.get_or_create(...)` / `.update_or_create(...)` |
| Bulk update | `.update(...)` |
| Delete | `.delete()` |

---

*Log your daily practice below.*

## Practice Log

- **[Date]** — Exercises completed / mistakes made / new things learned:
