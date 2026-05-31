(function () {
    "use strict";

    function getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute("content") : "";
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

        const hash = window.location.hash.replace("#", "");
        if (hash === "login") {
            const loginModal = document.getElementById("loginModal");
            if (loginModal) {
                new bootstrap.Modal(loginModal).show();
            }
        } else if (hash === "register") {
            const registerModal = document.getElementById("registerModal");
            if (registerModal) {
                new bootstrap.Modal(registerModal).show();
            }
        }
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

        categoryEl.className = "badge bmi-badge bmi-" + bmi.category.toLowerCase().replace(/\s+/g, "-");
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

        if (weightChart) {
            weightChart.destroy();
        }

        weightChart = new Chart(canvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Weight (kg)",
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
                        pointHoverRadius: 7,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: "#94a3b8" },
                    },
                },
                scales: {
                    x: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(45, 58, 82, 0.5)" },
                    },
                    y: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(45, 58, 82, 0.5)" },
                        title: {
                            display: true,
                            text: "kg",
                            color: "#94a3b8",
                        },
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
                if (!res.ok) throw new Error("Failed to load weight history");
                return res.json();
            })
            .then(function (data) {
                renderWeightChart(data.entries || []);
            })
            .catch(function () {
                const feedback = document.getElementById("weightFeedback");
                if (feedback) {
                    feedback.innerHTML =
                        '<span class="text-danger">Could not load weight history.</span>';
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
                        '<span class="text-warning">Enter a valid weight between 30 and 300 kg.</span>';
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
                                (result.data.error || "Failed to save weight.") +
                                "</span>";
                        }
                        return;
                    }

                    if (feedback) {
                        feedback.innerHTML =
                            '<span class="text-success"><i class="bi bi-check-circle"></i> Weight logged successfully!</span>';
                    }

                    const profileWeight = document.getElementById("profileWeight");
                    if (profileWeight) {
                        profileWeight.textContent = weight + " kg";
                    }

                    if (result.data.bmi) {
                        updateBmiDisplay(result.data.bmi);
                    }

                    loadWeightHistory();
                })
                .catch(function () {
                    btn.disabled = false;
                    if (feedback) {
                        feedback.innerHTML =
                            '<span class="text-danger">Network error. Please try again.</span>';
                    }
                });
        });

        loadWeightHistory();

        const weightTab = document.querySelector('[data-bs-target="#tab-weight"]');
        if (weightTab) {
            weightTab.addEventListener("shown.bs.tab", function () {
                if (weightChart) {
                    weightChart.resize();
                }
            });
        }
    }

    function syncDashNavTabs() {
        const tabContent = document.getElementById("dashboardTabContent");
        const tabNav = document.getElementById("dashTabNav");
        if (!tabContent || !tabNav) return;

        tabContent.querySelectorAll(".tab-pane").forEach(function (pane) {
            pane.addEventListener("shown.bs.tab", function () {
                /* Bootstrap handles pane visibility */
            });
        });

        tabContent.addEventListener("shown.bs.tab", function (event) {
            const trigger = event.target;
            if (!trigger || !trigger.getAttribute("data-bs-target")) return;
            const targetId = trigger.getAttribute("data-bs-target");
            tabNav.querySelectorAll(".nav-link").forEach(function (link) {
                link.classList.remove("active");
                if (link.getAttribute("data-bs-target") === targetId) {
                    link.classList.add("active");
                }
            });
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        initLandingPage();
        initWeightTracker();
        syncDashNavTabs();
    });
})();
