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
    json_string = json.dumps(data, sort_keys=True, indent=4)
    with open(filename, "w") as file:
        file.write(json_string)
