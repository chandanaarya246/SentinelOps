
def detect_anomalies(data):
    alerts = []

    # CPU usage check
    if data.get("cpu_usage", 0) > 80:
        alerts.append("High CPU usage detected")

    # Memory usage check
    if data.get("memory_usage", 0) > 85:
        alerts.append("High memory usage detected")

    # Disk usage check
    if data.get("disk_usage", 0) > 90:
        alerts.append("Disk space is running low")

    # Network latency check
    if data.get("network_latency", 0) > 100:
        alerts.append("High network latency detected")

    # Packet loss check
    if data.get("packet_loss", 0) > 5:
        alerts.append("Network packet loss detected")

    # Failed login attempts check
    if data.get("failed_logins", 0) > 3:
        alerts.append("Repeated failed login attempts detected")

    # Collector status check
    if data.get("collector_status") != "Online":
        alerts.append("Collector is offline")

    return alerts


# Test anomaly detection independently
if __name__ == "__main__":

    test_data = {
        "cpu_usage": 90,
        "memory_usage": 90,
        "disk_usage": 95,
        "network_latency": 150,
        "packet_loss": 8,
        "failed_logins": 5,
        "collector_status": "Offline"
    }

    print("\n========== SENTINELOPS ANOMALY TEST ==========")

    detected_alerts = detect_anomalies(test_data)

    for alert in detected_alerts:
        print("[ALERT]", alert)

    print("\nTotal Alerts:", len(detected_alerts))

    if len(detected_alerts) == 7:
        print("Test Result: PASSED")
    else:
        print("Test Result: CHECK REQUIRED")
