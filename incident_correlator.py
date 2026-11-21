
def correlate_incidents(alerts):
    incidents = []

    if not alerts:
        return incidents

    # 1. Infrastructure performance issue
    performance_alerts = [
        alert for alert in [
            "High CPU usage detected",
            "High memory usage detected",
            "High disk usage detected",
            "High network latency detected"
        ]
        if alert in alerts
    ]

    if len(performance_alerts) >= 2:
        incidents.append({
            "incident": "Infrastructure Performance Issue",
            "severity": "HIGH",
            "related_alerts": performance_alerts,
            "possible_explanation": (
                "Multiple infrastructure performance anomalies "
                "were detected together."
            ),
            "recommendation": (
                "Investigate system resource usage and "
                "network performance."
            )
        })

    # 2. Authentication security issue
    if "Repeated failed login attempts detected" in alerts:
        incidents.append({
            "incident": "Authentication Security Alert",
            "severity": "CRITICAL",
            "related_alerts": [
                "Repeated failed login attempts detected"
            ],
            "possible_explanation": (
                "Multiple failed login attempts were detected."
            ),
            "recommendation": (
                "Review authentication activity and verify "
                "access policies."
            )
        })

    # 3. Network issue
    network_alerts = [
        alert for alert in [
            "High network latency detected",
            "Network packet loss detected"
        ]
        if alert in alerts
    ]

    if len(network_alerts) == 2:
        incidents.append({
            "incident": "Network Connectivity Issue",
            "severity": "HIGH",
            "related_alerts": network_alerts,
            "possible_explanation": (
                "High latency and packet loss indicate "
                "possible network instability."
            ),
            "recommendation": (
                "Investigate network connectivity and "
                "infrastructure performance."
            )
        })

    # 4. Collector issue
    if "Collector is offline" in alerts:
        incidents.append({
            "incident": "Telemetry Collector Failure",
            "severity": "HIGH",
            "related_alerts": ["Collector is offline"],
            "possible_explanation": (
                "The telemetry collector is not reporting "
                "an online status."
            ),
            "recommendation": (
                "Check collector availability and restore "
                "telemetry collection."
            )
        })

    # 5. Fallback incident
    if not incidents:
        incidents.append({
            "incident": "General Infrastructure Alert",
            "severity": "MEDIUM",
            "related_alerts": alerts,
            "possible_explanation": (
                "One or more infrastructure anomalies "
                "were detected."
            ),
            "recommendation": (
                "Investigate the reported alerts."
            )
        })

    return incidents


# Independent test
if __name__ == "__main__":

    test_alerts = [
        "High CPU usage detected",
        "High network latency detected",
        "Network packet loss detected",
        "Repeated failed login attempts detected",
        "Collector is offline"
    ]

    print("\n========== INCIDENTDNA TEST ==========")

    detected_incidents = correlate_incidents(test_alerts)

    for incident in detected_incidents:
        print("\nIncident:", incident["incident"])
        print("Severity:", incident["severity"])
        print("Related Alerts:", incident["related_alerts"])

    print("\nTotal Incidents:", len(detected_incidents))
