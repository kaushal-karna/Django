# Course Management — Frontend Demo (Static)

Plain HTML/CSS/JS front end for the "Courses" module of a school management
system. No build step, no backend, no localStorage — every page's course
data is written directly into the HTML as static markup.

## Pages
- `index.html` — Dashboard with static summary stats and a static "recently added" table
- `courses.html` — Full course list, hardcoded as table rows; search box and
  department/status dropdowns filter those rows client-side (no data fetching)
- `add-course.html` — A course form; submitting just shows a confirmation
  toast and returns to the list (demo only, nothing is saved)
- `course-details.html` — A single static example course record

All four pages share the same header (branding + nav) and footer, written
directly into each HTML file, and the same two shared files:

- `css/style.css` — design tokens + all component styles
- `js/script.js` — one small script: highlights the active nav tab, filters
  the static table rows on `courses.html`, confirms + removes a row on
  "Delete", and shows a toast on form submit. No data storage of any kind.

## Running it
Just open `index.html` in a browser — everything runs client-side.
Editing the course data means editing the HTML rows directly.
