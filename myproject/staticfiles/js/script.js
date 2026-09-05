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
    // Course search + filters
    // ==============================

    var searchInput = document.getElementById("search-input");
    var deptFilter = document.getElementById("dept-filter");
    var statusFilter = document.getElementById("status-filter");

    var rows = document.querySelectorAll("#courses-body tr");

    if (searchInput && rows.length) {

        function applyFilters() {

            var q = searchInput.value.trim().toLowerCase();

            var dept = deptFilter
                ? deptFilter.value
                : "";

            var status = statusFilter
                ? statusFilter.value
                : "";

            var visibleCount = 0;


            rows.forEach(function (row) {

                var text =
                    row.getAttribute("data-search") || "";

                var rowDept =
                    row.getAttribute("data-dept") || "";

                var rowStatus =
                    row.getAttribute("data-status") || "";


                // Case-insensitive search
                text = text.toLowerCase();


                var matches =
                    (!q || text.includes(q)) &&
                    (!dept || rowDept === dept) &&
                    (!status || rowStatus === status);


                row.style.display =
                    matches ? "" : "none";


                if (matches) {
                    visibleCount++;
                }

            });


            // Empty state
            var empty =
                document.getElementById("empty-state");

            if (empty) {
                empty.style.display =
                    visibleCount ? "none" : "block";
            }

        }


        searchInput.addEventListener(
            "input",
            applyFilters
        );


        if (deptFilter) {
            deptFilter.addEventListener(
                "change",
                applyFilters
            );
        }


        if (statusFilter) {
            statusFilter.addEventListener(
                "change",
                applyFilters
            );
        }

    }

});