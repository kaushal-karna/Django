/* =========================================================
   script.js — small helpers only. No data storage.
   All course data lives directly in the HTML as static markup.
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {

  // Highlight the current tab in the nav, based on <body data-page="...">
  var current = document.body.getAttribute('data-page');
  document.querySelectorAll('nav.catalog-tabs a').forEach(function (link) {
    if (link.getAttribute('data-tab') === current) link.classList.add('active');
  });

  // Footer year
  var yearEl = document.getElementById('footer-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---- Course list page: search + filter over the static table rows ----
  var searchInput = document.getElementById('search-input');
  var deptFilter = document.getElementById('dept-filter');
  var statusFilter = document.getElementById('status-filter');
  var rows = document.querySelectorAll('#courses-body tr');

  if (searchInput && rows.length) {
    var applyFilters = function () {
      var q = searchInput.value.trim().toLowerCase();
      var dept = deptFilter ? deptFilter.value : '';
      var status = statusFilter ? statusFilter.value : '';
      var visibleCount = 0;

      rows.forEach(function (row) {
        var text = row.getAttribute('data-search') || '';
        var rowDept = row.getAttribute('data-dept') || '';
        var rowStatus = row.getAttribute('data-status') || '';

        var matches =
          (!q || text.indexOf(q) !== -1) &&
          (!dept || rowDept === dept) &&
          (!status || rowStatus === status);

        row.style.display = matches ? '' : 'none';
        if (matches) visibleCount++;
      });

      var empty = document.getElementById('empty-state');
      if (empty) empty.style.display = visibleCount ? 'none' : 'block';
    };

    searchInput.addEventListener('input', applyFilters);
    if (deptFilter) deptFilter.addEventListener('change', applyFilters);
    if (statusFilter) statusFilter.addEventListener('change', applyFilters);
  }

  // ---- Delete buttons: demo-only, just removes the row/card after confirm ----
  document.querySelectorAll('[data-delete]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var name = btn.getAttribute('data-delete');
      if (!confirm('Remove "' + name + '" from the catalog? (demo only, not saved)')) return;

      var row = btn.closest('tr');
      if (row) {
        row.remove();
      } else {
        // course-details page: no row to remove, just head back to the list
        window.location.href = 'courses.html';
        return;
      }
      showToast('"' + name + '" removed.');
    });
  });
});

// Small toast used by a couple of pages above
function showToast(message) {
  var toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(showToast._t);
  showToast._t = setTimeout(function () {
    toast.classList.remove('show');
  }, 2400);
}
document.addEventListener("DOMContentLoaded", function () {
    const currentPage = document.body.dataset.page;

    const tabs = document.querySelectorAll(".catalog-tabs a");

    tabs.forEach(function (tab) {
        if (tab.dataset.tab === currentPage) {
            tab.classList.add("active");
        }
    });
});