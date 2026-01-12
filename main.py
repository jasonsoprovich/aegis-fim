import json
import os

from hash_engine import compare_baseline, load_baseline, save_baseline, set_baseline


def main():
    target = "./test_dir"
    baseline_filename = "./data/baseline.json"

    if not os.path.exists(target):
        print(f"Directory {target} not found.")
        return

    print(f"Scanning: {target}.")
    current_scan = set_baseline(target)
    old_baseline = load_baseline(baseline_filename)

    if old_baseline is None:
        print("First run detected. Saving baseline.")
        save_baseline(current_scan, baseline_filename)
        print("Baseline established. Run again to scan for changes.")
    else:
        print("Existing baseline found. Comparing files.")
        changes = compare_baseline(old_baseline, current_scan)

        if not changes["new"] and not changes["modified"] and not changes["deleted"]:
            print("No changes detected. Integrity verified.")
        else:
            for path in changes["new"]:
                print(f"[NEW] {path}")
            for path in changes["modified"]:
                print(f"[MODIFIED] {path}")
            for path in changes["deleted"]:
                print(f"[DELETED] {path}")


def print_output(output):
    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()
