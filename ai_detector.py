
import numpy as np
from sklearn.ensemble import IsolationForest


# Illustrative normal infrastructure training data
training_data = np.array([
    [35, 45, 50, 30, 0],
    [40, 50, 55, 35, 0],
    [45, 55, 60, 40, 1],
    [50, 60, 65, 45, 0],
    [38, 48, 52, 32, 0],
    [42, 53, 58, 38, 1],
    [48, 58, 62, 42, 0],
    [36, 46, 51, 31, 0],
    [44, 54, 59, 39, 0],
    [47, 57, 63, 41, 1],
    [39, 49, 54, 34, 0],
    [43, 52, 57, 37, 0],
    [46, 56, 61, 43, 1],
    [41, 51, 56, 36, 0],
    [49, 59, 64, 44, 0],
    [37, 47, 53, 33, 0],
    [45, 55, 60, 40, 0],
    [52, 62, 67, 48, 1],
    [34, 44, 49, 29, 0],
    [46, 57, 62, 41, 0]
])


# Train the Isolation Forest model
model = IsolationForest(
    n_estimators=150,
    contamination=0.10,
    random_state=42
)

model.fit(training_data)


def detect_ai_anomaly(data):

    required_fields = [
        "cpu_usage",
        "memory_usage",
        "disk_usage",
        "network_latency",
        "packet_loss"
    ]

    # Validate telemetry fields
    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return {
            "status": "Error",
            "message": "Missing telemetry fields: "
                       + ", ".join(missing_fields),
            "anomaly_score": None
        }

    try:
        features = np.array([[
            float(data["cpu_usage"]),
            float(data["memory_usage"]),
            float(data["disk_usage"]),
            float(data["network_latency"]),
            float(data["packet_loss"])
        ]])

    except (TypeError, ValueError):
        return {
            "status": "Error",
            "message": "Telemetry values must be numeric",
            "anomaly_score": None
        }

    # Predict infrastructure behaviour
    prediction = model.predict(features)
    anomaly_score = model.decision_function(features)[0]

    if prediction[0] == -1:
        return {
            "status": "Anomaly",
            "message": "AI detected unusual infrastructure behaviour",
            "anomaly_score": round(float(anomaly_score), 4)
        }

    return {
        "status": "Normal",
        "message": "Infrastructure behaviour appears normal",
        "anomaly_score": round(float(anomaly_score), 4)
    }


# Independent testing
if __name__ == "__main__":

    normal_sample = {
        "cpu_usage": 45,
        "memory_usage": 55,
        "disk_usage": 60,
        "network_latency": 40,
        "packet_loss": 1
    }

    unusual_sample = {
        "cpu_usage": 95,
        "memory_usage": 92,
        "disk_usage": 95,
        "network_latency": 180,
        "packet_loss": 10
    }

    print("\n========== SENTINELOPS AI TEST ==========")

    print("\nNormal Sample:")
    print(detect_ai_anomaly(normal_sample))

    print("\nUnusual Sample:")
    print(detect_ai_anomaly(unusual_sample))

    print("\nMissing Data Test:")
    print(detect_ai_anomaly({"cpu_usage": 50}))
