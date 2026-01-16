import hashlib
import os


def calc_sha256(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def set_baseline(directory, ignore_list=None):
    if ignore_list is None:
        ignore_list = []

    baseline = {}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_list]

        for file in files:
            if file in ignore_list:
                continue

            abs_path = os.path.abspath(os.path.join(root, file))

            if any(ignored in abs_path for ignored in ignore_list):
                continue

            file_hash = calc_sha256(abs_path)
            if file_hash:
                baseline[abs_path] = file_hash

    return baseline


def compare_baseline(old_baseline, new_baseline):
    results = {"new": [], "modified": [], "deleted": []}

    if old_baseline is None:
        return results
        # print(f"No {old_baseline} found. Creating new baseline file")

    for path in new_baseline:
        if path not in old_baseline:
            results["new"].append(path)
            # print(f"New: {path}")
        elif new_baseline[path] != old_baseline[path]:
            results["modified"].append(path)
            # print(f"Modified: {path}")

    for path in old_baseline:
        if path not in new_baseline:
            results["deleted"].append(path)
            # print(f"Deleted: {path}")

    return results
