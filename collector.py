
import random
from datetime import datetime, timezone


def collect_telemetry():

    scenarios = [
        {
            "cpu_usage": random.randint(35, 60),
            "memory_usage": random.randint(40, 70),
            "disk_usage": random.randint(50, 75),
            "network_latency": random.randint(20, 80),
            "packet_loss": random.randint(0, 2),
            "failed_logins": random.randint(0, 2),
            "collector_status": "Online"
        },

        {
            "cpu_usage": random.randint(85, 98),
            "memory_usage": random.randint(70, 85),
            "disk_usage": random.randint(60, 80),
            "network_latency": random.randint(110, 180),
            "packet_loss": random.randint(0, 3),
            "failed_logins": random.randint(0, 2),
            "collector_status": "Online"
        },

        {
            "cpu_usage": random.randint(40, 70),
            "memory_usage": random.randint(50, 75),
            "disk_usage": random.randint(60, 85),
            "network_latency": random.randint(120, 250),
            "packet_loss": random.randint(6, 12),
            "failed_logins": random.randint(0, 2),
            "collector_status": "Online"
        },

        {
            "cpu_usage": random.randint(35, 65),
            "memory_usage": random.randint(45, 75),
            "disk_usage": random.randint(50, 80),
            "network_latency": random.randint(20, 90),
            "packet_loss": random.randint(0, 2),
            "failed_logins": random.randint(5, 10),
            "collector_status": "Online"
        }
    ]

    telemetry = random.choice(scenarios)

    telemetry["source_id"] = "SOURCE-001"

    telemetry["event_timestamp"] = (
        datetime.now(timezone.utc).isoformat()
    )

    return telemetry
