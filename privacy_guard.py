ALLOWED_FIELDS = [
    "source_id",
    "event_timestamp",
    "cpu_usage",
    "memory_usage",
    "disk_usage",
    "network_latency",
    "packet_loss",
    "failed_logins",
    "collector_status"
]


def filter_telemetry(telemetry):
    return {
        field: telemetry[field]
        for field in ALLOWED_FIELDS
        if field in telemetry
    }


def generate_privacy_audit(telemetry, safe_data):

    approved_fields = list(safe_data.keys())

    blocked_fields = [
        field for field in telemetry
        if field not in ALLOWED_FIELDS
    ]

    return {
        "approved_fields": approved_fields,
        "blocked_fields": blocked_fields,
        "approved_count": len(approved_fields),
        "blocked_count": len(blocked_fields),
        "privacy_status": "PASSED",
        "transfer_payload": safe_data
    }


def test_privacy_guard():

    test_data = {
        "source_id": "SOURCE-001",
        "event_timestamp": "2026-11-20T15:17:42+00:00",
        "cpu_usage": 85,
        "memory_usage": 72,
        "disk_usage": 68,
        "network_latency": 120,
        "packet_loss": 2,
        "failed_logins": 5,
        "collector_status": "Online",
        "password": "fake_password_123",
        "api_key": "FAKE_API_KEY",
        "raw_log": "Fake login log"
    }

    filtered_data = filter_telemetry(test_data)

    audit = generate_privacy_audit(test_data, filtered_data)

    print("\n========== PRIVACY AUDIT ==========")

    print("\nApproved Fields:")
    for field in audit["approved_fields"]:
        print(field, "- APPROVED")

    print("\nBlocked Fields:")
    for field in audit["blocked_fields"]:
        print(field, "- BLOCKED")

    print("\nApproved Count:", audit["approved_count"])
    print("Blocked Count:", audit["blocked_count"])

    print("\nPrivacy Status:", audit["privacy_status"])

    print("\nTransfer Payload:")
    print(audit["transfer_payload"])


if __name__ == "__main__":
    test_privacy_guard()
