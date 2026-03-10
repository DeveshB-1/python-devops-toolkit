#!/usr/bin/env python3
"""
System Health Monitor
Checks CPU, memory, disk, and service status — sends alerts on threshold breach
"""
import subprocess
import sys
import json
import os
from datetime import datetime

THRESHOLDS = {
    "cpu_percent": 85,
    "memory_percent": 90,
    "disk_percent": 80,
}

SERVICES = ["nginx", "docker", "kubelet"]


def get_cpu_usage():
    result = subprocess.run(
        ["top", "-bn1"], capture_output=True, text=True
    )
    for line in result.stdout.split("\n"):
        if "Cpu(s)" in line:
            idle = float(line.split(",")[3].split()[0])
            return round(100 - idle, 1)
    return 0.0


def get_memory_usage():
    with open("/proc/meminfo") as f:
        info = {}
        for line in f:
            key, val = line.split(":")[0], line.split(":")[1].strip().split()[0]
            info[key] = int(val)
    total = info["MemTotal"]
    available = info["MemAvailable"]
    used_pct = round((1 - available / total) * 100, 1)
    return used_pct


def get_disk_usage(path="/"):
    result = subprocess.run(["df", "-h", path], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    if len(lines) > 1:
        pct = int(lines[1].split()[4].replace("%", ""))
        return pct
    return 0


def check_service(name):
    result = subprocess.run(
        ["systemctl", "is-active", name], capture_output=True, text=True
    )
    return result.stdout.strip() == "active"


def main():
    report = {
        "timestamp": datetime.now().isoformat(),
        "metrics": {},
        "services": {},
        "alerts": []
    }

    report["metrics"]["cpu_percent"] = get_cpu_usage()
    report["metrics"]["memory_percent"] = get_memory_usage()
    report["metrics"]["disk_percent"] = get_disk_usage()

    for metric, value in report["metrics"].items():
        if value > THRESHOLDS[metric]:
            report["alerts"].append(f"ALERT: {metric} = {value}% (threshold: {THRESHOLDS[metric]}%)")

    for svc in SERVICES:
        status = check_service(svc)
        report["services"][svc] = "active" if status else "INACTIVE"
        if not status:
            report["alerts"].append(f"ALERT: Service {svc} is not running")

    print(json.dumps(report, indent=2))

    if report["alerts"]:
        print("\nALERTS:", file=sys.stderr)
        for alert in report["alerts"]:
            print(f"  {alert}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
