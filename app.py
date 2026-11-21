from flask import Flask, jsonify, render_template

from collector import collect_telemetry
from privacy_guard import filter_telemetry, generate_privacy_audit
from anomaly_detector import detect_anomalies
from incident_correlator import correlate_incidents
from ai_detector import detect_ai_anomaly

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/monitor")
def monitor():

    raw_data = collect_telemetry()

    safe_data = filter_telemetry(raw_data)

    privacy_audit = generate_privacy_audit(raw_data, safe_data)

    alerts = detect_anomalies(safe_data)

    incidents = correlate_incidents(alerts)

    ai_result = detect_ai_anomaly(safe_data)

    return jsonify({
        "project": "SentinelOps",
        "status": "Running",
        "telemetry": safe_data,
        "alerts": alerts,
        "total_alerts": len(alerts),
        "incidents": incidents,
        "ai_analysis": ai_result,
        "privacy_audit": privacy_audit
    })


if __name__ == "__main__":
    app.run(debug=True)
