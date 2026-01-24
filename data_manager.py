import datetime
import json
import os


def save_baseline(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        raise IOError(f"Failed to save baseline: {e}")


def load_baseline(filename):
    if not os.path.exists(filename):
        return None

    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        raise IOError(f"Failed to load baseline: {e}")


def export_report(changes, scan_summary, filename):
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": scan_summary,
        "details": changes,
    }
    try:
        if os.path.dirname(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(report, f, indent=4)
        return True
    except IOError as e:
        raise IOError(f"Failed to export report: {e}")
