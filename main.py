import argparse
import json
import os

from hash_engine import compare_baseline, load_baseline, save_baseline, set_baseline


def main():
    parser = argparse.ArgumentParser(description="Aegis File Integrity Monitor")
    parser.add_argument("path", help="The directory to monitor")
    parser.add_argument(
        "-b",
        "--baseline",
        default="./data/baseline.json",
        help="The path to baseline file",
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Update baseline if changes are detected",
    )

    args = parser.parse_args()

    target = args.path
    baseline_filename = args.baseline
    update_mode = args.update

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

        has_changes = changes["new"] or changes["modified"] or changes["deleted"]

        if not has_changes:
            print("No changes detected. Integrity verified.")
        else:
            for path in changes["new"]:
                print(f"[NEW] {path}")
            for path in changes["modified"]:
                print(f"[MODIFIED] {path}")
            for path in changes["deleted"]:
                print(f"[DELETED] {path}")

            if update_mode:
                confirm = input(
                    "\nChanges detected. Would you like to update the baseline? (y/n): "
                )
                if confirm.lower() == "y":
                    save_baseline(current_scan, baseline_filename)
                    print("Baseline updated.")


def print_output(output):
    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()
