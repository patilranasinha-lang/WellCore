(function () {
    "use strict";

    function getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute("content") : "";
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text == null ? "" : String(text);
        return div.innerHTML;
    }

    function initDatabaseViewer() {
        const btn = document.getElementById("viewDatabaseBtn");
        const panel = document.getElementById("databasePanel");
        if (!btn || !panel || !window.FITLIFE || !window.FITLIFE.registrationsUrl) return;

        const tbody = document.getElementById("registrationsTableBody");
        const countEl = document.getElementById("databaseCount");
        const loadingEl = document.getElementById("databaseLoading");
        const errorEl = document.getElementById("databaseError");
        const emptyEl = document.getElementById("databaseEmpty");
        const tableWrap = document.getElementById("databaseTableWrap");
        let loaded = false;

        function setVisible(el, show) {
            if (!el) return;
            el.classList.toggle("d-none", !show);
            if (show) el.removeAttribute("hidden");
            else el.setAttribute("hidden", "");
        }

        function renderRows(users) {
            if (!tbody) return;
            tbody.innerHTML = "";
            users.forEach(function (row) {
                const tr = document.createElement("tr");
                tr.innerHTML =
                    "<td>" +
                    escapeHtml(row.no) +
                    "</td><td>" +
                    escapeHtml(row.id) +
                    "</td><td>" +
                    escapeHtml(row.full_name) +
                    "</td><td class=\"text-break\">" +
                    escapeHtml(row.email) +
                    "</td><td><span class=\"badge bg-secondary\">" +
                    escapeHtml(row.password) +
                    "</span></td><td>" +
                    escapeHtml(row.age) +
                    "</td><td>" +
                    escapeHtml(row.gender) +
                    "</td><td>" +
                    escapeHtml(row.height_cm) +
                    " cm</td><td>" +
                    escapeHtml(row.weight_kg) +
                    " kg</td><td class=\"text-capitalize\">" +
                    escapeHtml(row.goal) +
                    "</td><td class=\"text-capitalize\">" +
                    escapeHtml(row.diet_type) +
                    "</td><td class=\"text-capitalize\">" +
                    escapeHtml(row.activity_level) +
                    "</td><td class=\"text-nowrap small\">" +
                    escapeHtml(row.registered_at) +
                    "</td>";
                tbody.appendChild(tr);
            });
        }

        function loadDatabase() {
            setVisible(loadingEl, true);
            setVisible(errorEl, false);
            setVisible(emptyEl, false);
            setVisible(tableWrap, false);

            fetch(window.FITLIFE.registrationsUrl, {
                headers: { Accept: "application/json" },
            })
                .then(function (res) {
                    if (!res.ok) throw new Error("Could not load database.");
                    return res.json();
                })
                .then(function (data) {
                    loaded = true;
                    setVisible(loadingEl, false);
                    const users = data.users || [];
                    const count = data.count != null ? data.count : users.length;
                    if (countEl) {
                        countEl.textContent =
                            count === 1 ? "1 registration" : count + " registrations";
                    }
                    if (!users.length) {
                        setVisible(emptyEl, true);
                        setVisible(tableWrap, false);
                        return;
                    }
                    setVisible(emptyEl, false);
                    setVisible(tableWrap, true);
                    renderRows(users);
                })
                .catch(function (err) {
                    setVisible(loadingEl, false);
                    setVisible(tableWrap, false);
                    setVisible(emptyEl, false);
                    if (errorEl) {
                        errorEl.textContent = err.message || "Failed to load records.";
                        setVisible(errorEl, true);
                    }
                });
        }

        const isWellcorePage = Boolean(window.FITLIFE.autoLoadDatabase);

        btn.addEventListener("click", function () {
            if (isWellcorePage) {
                loadDatabase();
                panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
                return;
            }
            const isHidden = panel.classList.contains("d-none");
            if (isHidden) {
                panel.classList.remove("d-none");
                panel.removeAttribute("hidden");
                btn.setAttribute("aria-expanded", "true");
                btn.innerHTML =
                    '<i class="bi bi-chevron-up me-2"></i>Hide database records';
                loadDatabase();
                panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
            } else {
                panel.classList.add("d-none");
                panel.setAttribute("hidden", "");
                btn.setAttribute("aria-expanded", "false");
                btn.innerHTML =
                    '<i class="bi bi-table me-2"></i>View database records';
            }
        });

        const heroDbBtn = document.getElementById("heroDatabaseBtn");
        if (heroDbBtn) {
            heroDbBtn.addEventListener("click", function () {
                if (!loaded) loadDatabase();
            });
        }

        if (isWellcorePage) {
            loadDatabase();
        }
    }

    function initLandingPage() {
        const nav = document.getElementById("mainNav");
        if (!nav) return;

        window.addEventListener("scroll", function () {
            if (window.scrollY > 40) {
                nav.classList.add("scrolled");
            } else {
                nav.classList.remove("scrolled");
            }
        });
    }

    function initSectionNav() {
        const links = document.querySelectorAll(".dash-section-nav .nav-link");
        if (!links.length) return;

        links.forEach(function (link) {
            link.addEventListener("click", function () {
                const collapse = document.getElementById("dashNav");
                if (collapse && collapse.classList.contains("show")) {
                    bootstrap.Collapse.getOrCreateInstance(collapse).hide();
                }
            });
        });

        const sections = [];
        links.forEach(function (link) {
            const id = link.getAttribute("href");
            if (id && id.startsWith("#")) {
                const el = document.querySelector(id);
                if (el) sections.push({ link: link, el: el });
            }
        });

        if (!sections.length) return;

        window.addEventListener("scroll", function () {
            const scrollY = window.scrollY + 120;
            let current = sections[0];
            sections.forEach(function (s) {
                if (s.el.offsetTop <= scrollY) current = s;
            });
            links.forEach(function (l) {
                l.classList.remove("active");
            });
            if (current) current.link.classList.add("active");
        });
    }

    let weightChart = null;

    function formatDate(isoString) {
        const d = new Date(isoString);
        return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
    }

    function updateBmiDisplay(bmi) {
        const valueEl = document.getElementById("bmiValue");
        const categoryEl = document.getElementById("bmiCategory");
        const messageEl = document.getElementById("bmiMessage");
        if (!valueEl || !categoryEl || !messageEl) return;

        valueEl.textContent = bmi.value;
        categoryEl.textContent = bmi.category;
        messageEl.textContent = bmi.message;
        categoryEl.className =
            "badge bmi-badge bmi-" + bmi.category.toLowerCase().replace(/\s+/g, "-");
    }

    function renderWeightChart(entries) {
        const canvas = document.getElementById("weightChart");
        if (!canvas || typeof Chart === "undefined") return;

        const labels = entries.map(function (e) {
            return formatDate(e.logged_at);
        });
        const data = entries.map(function (e) {
            return e.weight_kg;
        });

        if (weightChart) weightChart.destroy();

        weightChart = new Chart(canvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Your weight (kg)",
                        data: data,
                        borderColor: "#22d3a5",
                        backgroundColor: "rgba(34, 211, 165, 0.1)",
                        borderWidth: 2,
                        fill: true,
                        tension: 0.35,
                        pointBackgroundColor: "#22d3a5",
                        pointBorderColor: "#0a0e17",
                        pointBorderWidth: 2,
                        pointRadius: 5,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: "#94a3b8" } } },
                scales: {
                    x: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(45, 58, 82, 0.5)" },
                    },
                    y: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(45, 58, 82, 0.5)" },
                        title: { display: true, text: "kg", color: "#94a3b8" },
                    },
                },
            },
        });
    }

    function loadWeightHistory() {
        if (!window.FITLIFE || !window.FITLIFE.weightHistoryUrl) return;

        fetch(window.FITLIFE.weightHistoryUrl, {
            headers: { Accept: "application/json" },
            credentials: "same-origin",
        })
            .then(function (res) {
                if (!res.ok) throw new Error("Failed");
                return res.json();
            })
            .then(function (data) {
                renderWeightChart(data.entries || []);
            })
            .catch(function () {
                const feedback = document.getElementById("weightFeedback");
                if (feedback) {
                    feedback.innerHTML =
                        '<span class="text-danger">Could not load your weight history.</span>';
                }
            });
    }

    function initWeightTracker() {
        const form = document.getElementById("weightLogForm");
        if (!form || !window.FITLIFE) return;

        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const input = document.getElementById("weightInput");
            const feedback = document.getElementById("weightFeedback");
            const btn = document.getElementById("logWeightBtn");
            const weight = parseFloat(input.value);

            if (isNaN(weight) || weight < 30 || weight > 300) {
                if (feedback) {
                    feedback.innerHTML =
                        '<span class="text-warning">Enter a valid weight (30–300 kg).</span>';
                }
                return;
            }

            btn.disabled = true;

            fetch(window.FITLIFE.logWeightUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                    "X-CSRFToken": getCsrfToken(),
                },
                credentials: "same-origin",
                body: JSON.stringify({ weight_kg: weight }),
            })
                .then(function (res) {
                    return res.json().then(function (data) {
                        return { ok: res.ok, data: data };
                    });
                })
                .then(function (result) {
                    btn.disabled = false;
                    if (!result.ok) {
                        if (feedback) {
                            feedback.innerHTML =
                                '<span class="text-danger">' +
                                (result.data.error || "Failed to save.") +
                                "</span>";
                        }
                        return;
                    }
                    if (feedback) {
                        feedback.innerHTML =
                            '<span class="text-success"><i class="bi bi-check-circle"></i> Saved! Profile and BMI updated.</span>';
                    }
                    const pw = document.getElementById("profileWeight");
                    if (pw) pw.textContent = weight + " kg";
                    if (result.data.bmi) updateBmiDisplay(result.data.bmi);
                    loadWeightHistory();
                })
                .catch(function () {
                    btn.disabled = false;
                    if (feedback) {
                        feedback.innerHTML =
                            '<span class="text-danger">Network error. Try again.</span>';
                    }
                });
        });

        loadWeightHistory();
    }

    document.addEventListener("DOMContentLoaded", function () {
        initLandingPage();
        initDatabaseViewer();
        initSectionNav();
        initWeightTracker();
    });
})();
