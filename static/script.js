
/* =====================================
   SENTINELOPS - LIVE DASHBOARD
===================================== */

// Chart variables
let cpuChart = null;
let memoryChart = null;
let latencyChart = null;

// Store the last 12 readings
const historyLimit = 12;

const chartHistory = {
    labels: [],
    cpu: [],
    memory: [],
    latency: []
};


/* =====================================
   CREATE CHARTS
===================================== */

function createLineChart(canvasId, label, color) {

    const canvas = document.getElementById(canvasId);

    if (!canvas || typeof Chart === "undefined") {
        console.error("Chart.js or canvas not available:", canvasId);
        return null;
    }

    return new Chart(canvas, {

        type: "line",

        data: {
            labels: [],

            datasets: [{
                label: label,
                data: [],
                borderColor: color,
                backgroundColor: color + "22",
                borderWidth: 2,
                fill: true,
                tension: 0.35,
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },

        options: {

            responsive: true,
            maintainAspectRatio: false,
            animation: false,

            plugins: {
                legend: {
                    display: false
                }
            },

            scales: {

                x: {
                    ticks: {
                        color: "#94a3b8",
                        maxTicksLimit: 6
                    },
                    grid: {
                        color: "rgba(148, 163, 184, 0.08)"
                    }
                },

                y: {
                    beginAtZero: true,

                    ticks: {
                        color: "#94a3b8"
                    },

                    grid: {
                        color: "rgba(148, 163, 184, 0.08)"
                    }
                }

            }

        }

    });

}


/* =====================================
   INITIALIZE CHARTS
===================================== */

function initializeCharts() {

    if (typeof Chart === "undefined") {
        console.error("Chart.js library failed to load.");
        return;
    }

    cpuChart = createLineChart(
        "cpuChart",
        "CPU Usage (%)",
        "#60a5fa"
    );

    memoryChart = createLineChart(
        "memoryChart",
        "Memory Usage (%)",
        "#a78bfa"
    );

    latencyChart = createLineChart(
        "latencyChart",
        "Network Latency (ms)",
        "#34d399"
    );

}


/* =====================================
   UPDATE CHART HISTORY
===================================== */

function updateCharts(telemetry) {

    const cpu = Number(telemetry.cpu_usage);
    const memory = Number(telemetry.memory_usage);
    const latency = Number(telemetry.network_latency);

    // Ignore invalid readings
    if (
        !Number.isFinite(cpu) ||
        !Number.isFinite(memory) ||
        !Number.isFinite(latency)
    ) {
        console.error("Invalid chart telemetry received.");
        return;
    }

    const time = new Date().toLocaleTimeString();

    chartHistory.labels.push(time);
    chartHistory.cpu.push(cpu);
    chartHistory.memory.push(memory);
    chartHistory.latency.push(latency);

    // Keep only the last 12 readings
    if (chartHistory.labels.length > historyLimit) {

        chartHistory.labels.shift();
        chartHistory.cpu.shift();
        chartHistory.memory.shift();
        chartHistory.latency.shift();

    }

    // Update CPU chart
    if (cpuChart) {

        cpuChart.data.labels = [...chartHistory.labels];
        cpuChart.data.datasets[0].data = [...chartHistory.cpu];

        cpuChart.update("none");

    }

    // Update Memory chart
    if (memoryChart) {

        memoryChart.data.labels = [...chartHistory.labels];
        memoryChart.data.datasets[0].data = [...chartHistory.memory];

        memoryChart.update("none");

    }

    // Update Network Latency chart
    if (latencyChart) {

        latencyChart.data.labels = [...chartHistory.labels];
        latencyChart.data.datasets[0].data = [...chartHistory.latency];

        latencyChart.update("none");

    }

}


/* =====================================
   LOAD DASHBOARD
===================================== */

async function loadDashboard() {

    try {

        const response = await fetch("/api/monitor", {
            cache: "no-store"
        });

        if (!response.ok) {
            throw new Error("Failed to fetch telemetry");
        }

        const data = await response.json();
        const telemetry = data.telemetry;

        if (!telemetry) {
            throw new Error("Telemetry data unavailable");
        }


        // 1. INFRASTRUCTURE OVERVIEW

        document.getElementById("cpu").textContent =
            telemetry.cpu_usage + "%";

        document.getElementById("memory").textContent =
            telemetry.memory_usage + "%";

        document.getElementById("disk").textContent =
            telemetry.disk_usage + "%";

        document.getElementById("latency").textContent =
            telemetry.network_latency + " ms";

        document.getElementById("status").textContent =
            telemetry.collector_status;


        // 2. LIVE MONITORING CHARTS

        updateCharts(telemetry);


        // 3. SECURITY ALERTS

        const alertList = document.getElementById("alerts");

        alertList.innerHTML = "";

        if (!data.alerts || data.alerts.length === 0) {

            const item = document.createElement("li");
            item.textContent = "No anomalies detected";

            alertList.appendChild(item);

        } else {

            data.alerts.forEach(alert => {

                const item = document.createElement("li");
                item.textContent = alert;

                alertList.appendChild(item);

            });

        }


        // 4. AI INFRASTRUCTURE ANALYSIS

        const aiStatus = document.getElementById("ai-status");
        const aiMessage = document.getElementById("ai-message");
        const aiScore = document.getElementById("ai-score");

        if (data.ai_analysis) {

            aiStatus.textContent = data.ai_analysis.status;

            aiMessage.textContent =
                data.ai_analysis.message;

            aiStatus.className =
                data.ai_analysis.status === "Anomaly"
                    ? "ai-anomaly"
                    : "ai-normal";

            if (
                typeof data.ai_analysis.anomaly_score === "number" &&
                Number.isFinite(data.ai_analysis.anomaly_score)
            ) {

                aiScore.textContent =
                    data.ai_analysis.anomaly_score.toFixed(4);

            } else {

                aiScore.textContent = "Unavailable";

            }

        } else {

            aiStatus.textContent = "AI analysis unavailable";

            aiMessage.textContent =
                "The backend did not return an AI result.";

            aiStatus.className = "ai-waiting";

            aiScore.textContent = "--";

        }


        // 5. INCIDENT DNA

        const incidentContainer =
            document.getElementById("incidents");

        incidentContainer.innerHTML = "";

        if (!data.incidents || data.incidents.length === 0) {

            incidentContainer.textContent =
                "No correlated incidents detected.";

        } else {

            data.incidents.forEach(incident => {

                const card = document.createElement("div");

                card.className = "incident-card";

                const title = document.createElement("h3");

                title.textContent = incident.incident || "Unnamed Incident";

                const severity = document.createElement("span");

                const severityText =
                    incident.severity || "Unknown";

                severity.className =
                    "severity " + severityText.toLowerCase();

                severity.textContent = severityText;

                const alertsHeading = document.createElement("p");

                alertsHeading.textContent = "Related alerts:";

                const alertItems = document.createElement("ul");

                (incident.related_alerts || []).forEach(alert => {

                    const item = document.createElement("li");

                    item.textContent = alert;

                    alertItems.appendChild(item);

                });

                const explanation = document.createElement("p");

                explanation.textContent =
                    "Possible explanation: " +
                    (incident.possible_explanation || "Not available");

                const recommendation = document.createElement("p");

                recommendation.textContent =
                    "Recommendation: " +
                    (incident.recommendation || "Not available");

                card.appendChild(title);
                card.appendChild(severity);
                card.appendChild(alertsHeading);
                card.appendChild(alertItems);
                card.appendChild(explanation);
                card.appendChild(recommendation);

                incidentContainer.appendChild(card);

            });

        }


        // 6. PRIVACY AUDIT PANEL

        const audit = data.privacy_audit;

        const privacyStatus =
            document.getElementById("privacy-status");

        const approvedCount =
            document.getElementById("approved-count");

        const blockedCount =
            document.getElementById("blocked-count");

        const approvedFields =
            document.getElementById("approved-fields");

        const blockedFields =
            document.getElementById("blocked-fields");

        if (audit) {

            privacyStatus.textContent =
                "Privacy Status: " +
                (audit.privacy_status || "Unknown");

            approvedCount.textContent =
                audit.approved_count ?? "--";

            blockedCount.textContent =
                audit.blocked_count ?? "--";


            // Approved fields

            approvedFields.innerHTML = "";

            (audit.approved_fields || []).forEach(field => {

                const item = document.createElement("li");

                item.textContent = field + " - APPROVED";

                approvedFields.appendChild(item);

            });


            // Blocked fields

            blockedFields.innerHTML = "";

            if (
                !audit.blocked_fields ||
                audit.blocked_fields.length === 0
            ) {

                const item = document.createElement("li");

                item.textContent =
                    "No unapproved fields found in this telemetry sample.";

                blockedFields.appendChild(item);

            } else {

                audit.blocked_fields.forEach(field => {

                    const item = document.createElement("li");

                    item.textContent = field + " - BLOCKED";

                    blockedFields.appendChild(item);

                });

            }


            // Exact approved transfer payload

            document.getElementById("egress-data").textContent =
                JSON.stringify(audit.transfer_payload, null, 4);

        } else {

            privacyStatus.textContent =
                "Privacy audit unavailable";

            approvedCount.textContent = "--";
            blockedCount.textContent = "--";

            approvedFields.textContent =
                "Audit data unavailable";

            blockedFields.textContent =
                "Audit data unavailable";

            document.getElementById("egress-data").textContent =
                "No transfer payload available.";

        }

    } catch (error) {

        console.error("Dashboard error:", error);

        document.getElementById("ai-status").textContent =
            "Connection Error";

        document.getElementById("ai-message").textContent =
            error.message;

        document.getElementById("ai-score").textContent = "--";

        document.getElementById("privacy-status").textContent =
            "Privacy audit unavailable";

    }

}


/* =====================================
   START DASHBOARD
===================================== */

initializeCharts();

// Load dashboard immediately
loadDashboard();

// Refresh every 5 seconds
setInterval(loadDashboard, 5000);
