import json
import os


def save_baseline(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_baseline(filename):
    if not os.path.exists(filename):
        return None

    with open(filename, "r") as f:
        data = json.load(f)
        return data
