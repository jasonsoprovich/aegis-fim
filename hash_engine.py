import hashlib
import logging
import os


def get_file_info(filepath):
    try:
        stats = os.stat(filepath)
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return {
            "hash": sha256_hash.hexdigest(),
            "size": stats.st_size,
            "mtime": stats.st_mtime,
            "permissions": format(stats.st_mode & 0o777, "03o"),
        }, None
    except (PermissionError, FileNotFoundError, IOError) as e:
        error_msg = str(e)
        logging.warning(f"Could not process {filepath}: {error_msg}")
        return None, error_msg


def collect_files(directory, ignore_list):
    all_files = []
    root_directory = os.path.abspath(directory)

    for root, dirs, files in os.walk(root_directory):
        dirs[:] = [d for d in dirs if d not in ignore_list]
        for file in files:
            if file in ignore_list:
                continue
            abs_path = os.path.join(root, file)
            if not any(ignored in abs_path for ignored in ignore_list):
                all_files.append(abs_path)
    return all_files


def set_baseline(files_to_scan, progress=None, task=None, verbose=False):
    baseline = {}
    errors = {}

    for abs_path in files_to_scan:
        info, err = get_file_info(abs_path)
        if info:
            baseline[abs_path] = info
            if verbose and progress:
                progress.console.log(f"[grey]Scanned: {abs_path}[/]")
        else:
            errors[abs_path] = err

        if progress and task:
            progress.advance(task)

    return baseline, errors


def compare_baseline(old_baseline, new_baseline):
    results = {"new": [], "modified": [], "deleted": [], "metadata_changed": []}

    if old_baseline is None:
        return results

    for path in new_baseline:
        if path not in old_baseline:
            results["new"].append(path)

        else:
            old_info = old_baseline[path]
            new_info = new_baseline[path]

            if new_info["hash"] != old_info["hash"]:
                results["modified"].append(path)

            if (
                new_info["size"] != old_info["size"]
                or new_info["permissions"] != old_info["permissions"]
            ):
                results["metadata_changed"].append(
                    {
                        "path": path,
                        "old_size": old_info["size"],
                        "new_size": new_info["size"],
                        "old_permissions": old_info["permissions"],
                        "new_permissions": new_info["permissions"],
                    }
                )

    for path in old_baseline:
        if path not in new_baseline:
            results["deleted"].append(path)

    return results
