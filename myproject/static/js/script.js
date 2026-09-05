document.addEventListener("DOMContentLoaded", function () {

    // ==============================
    // Active navigation tab
    // ==============================

    console.log("Script Loading....")

    var current = document.body.getAttribute("data-page");

    document.querySelectorAll("nav.catalog-tabs a").forEach(function (link) {
        if (link.getAttribute("data-tab") === current) {
            link.classList.add("active");
        }
    });


    // ==============================
    // Footer year
    // ==============================

    var yearEl = document.getElementById("footer-year");

    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }


    // ==============================
    // ==============================
    // Generic Table Search & Filters
    // ==============================

    function setupTableFilter(inputId, deptId, statusId, tbodySelector, emptyId) {
        var searchInput = document.getElementById(inputId);
        var deptFilter = document.getElementById(deptId);
        var statusFilter = document.getElementById(statusId);
        var tbody = document.querySelector(tbodySelector);
        if (!tbody) return;

        var rows = tbody.querySelectorAll("tr");
        if (!rows.length && !searchInput) return;

        function applyFilters() {
            var q = searchInput ? searchInput.value.trim().toLowerCase() : "";
            var dept = deptFilter ? deptFilter.value : "";
            var status = statusFilter ? statusFilter.value : "";
            var visibleCount = 0;

            rows.forEach(function (row) {
                var text = (row.getAttribute("data-search") || "").toLowerCase();
                var rowDept = row.getAttribute("data-dept") || "";
                var rowStatus = row.getAttribute("data-status") || "";

                var matches =
                    (!q || text.includes(q)) &&
                    (!dept || rowDept === dept) &&
                    (!status || rowStatus === status);

                row.style.display = matches ? "" : "none";
                if (matches) {
                    visibleCount++;
                }
            });

            var empty = document.getElementById(emptyId);
            if (empty) {
                empty.style.display = visibleCount ? "none" : "block";
            }
        }

        if (searchInput) {
            searchInput.addEventListener("input", applyFilters);
        }

        if (deptFilter) {
            deptFilter.addEventListener("change", applyFilters);
        }

        if (statusFilter) {
            statusFilter.addEventListener("change", applyFilters);
        }
    }

    // Initialize filters for Courses, Students, and Teachers
    setupTableFilter("search-input", "dept-filter", "status-filter", "#courses-body", "empty-state");
    setupTableFilter("student-search-input", "student-dept-filter", "student-status-filter", "#students-body", "student-empty-state");
    setupTableFilter("teacher-search-input", "teacher-dept-filter", "teacher-status-filter", "#teachers-body", "teacher-empty-state");


    // ==============================
    // Delete Action Confirmation
    // ==============================

    document.querySelectorAll("button[data-delete]").forEach(function (button) {
        button.addEventListener("click", function (e) {
            var name = button.getAttribute("data-delete") || "this record";
            var confirmed = window.confirm("Are you sure you want to delete \"" + name + "\"? This action cannot be undone.");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

});