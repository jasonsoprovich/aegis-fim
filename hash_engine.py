import hashlib
import json
import os

# def list_files_recursively(path="."):
#     for entry in os.listdir(path):
#         full_path = os.path.join(path, entry)
#         if os.path.isdir(full_path):
#             list_files_recursively(full_path)
#         else:
#             print(full_path)


def calc_sha256(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def set_baseline(directory):
    baseline = {}
    for root, _, files in os.walk(directory):
        for file in files:
            abs_path = os.path.abspath(os.path.join(root, file))
            file_hash = calc_sha256(abs_path)
            baseline[abs_path] = file_hash

    return baseline


def save_baseline(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_baseline(filename):
    if not os.path.exists(filename):
        return None

    with open(filename, "r") as f:
        data = json.load(f)
        return data


def compare_baseline(old_baseline, new_baseline):
    if old_baseline is None:
        print(f"No {old_baseline} found. Creating new baseline file")
        #### create new baseline file

    #### change prints to return dictionaries
    for path in new_baseline:
        if path not in old_baseline:
            print(f"New: {path}")
        elif new_baseline[path] != old_baseline[path]:
            print(f"Modified: {path}")

    for path in old_baseline:
        if path not in new_baseline:
            print(f"Deleted: {path}")
