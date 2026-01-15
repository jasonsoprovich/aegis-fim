import argparse
import json
import logging
import os

from hash_engine import compare_baseline, load_baseline, save_baseline, set_baseline

os.makedirs("./logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("./logs/audit.log"), logging.StreamHandler()],
)


def main():
    parser = argparse.ArgumentParser(description="Aegis File Integrity Monitor")
    parser.add_argument("path", help="The directory to monitor")
    parser.add_argument(
        "-b",
        "--baseline",
        default="./data/baseline.json",
        help="Baseline storage file (JSON)",
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Update baseline if changes are detected",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        nargs="+",
        help="Space-separated list of files or directories to ignore",
    )

    args = parser.parse_args()

    target = args.path
    baseline_filename = args.baseline
    update_mode = args.update

    default_ignores = ["logs", "data", ".DS_Store", ".git"]
    default_ignores.append(os.path.basename(baseline_filename))
    if args.ignore:
        default_ignores.extend(args.ignore)

    if not os.path.exists(target):
        print(f"Directory {target} not found.")
        return

    print(f"Scanning: {target}.")
    current_scan = set_baseline(target, default_ignores)
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
            logging.info("No changes detected. Integrity verified.")
        else:
            for path in changes["new"]:
                logging.warning(f"[NEW] {path}")
            for path in changes["modified"]:
                logging.warning(f"[MODIFIED] {path}")
            for path in changes["deleted"]:
                logging.warning(f"[DELETED] {path}")

            new_count = len(changes["new"])
            mod_count = len(changes["modified"])
            del_count = len(changes["deleted"])
            total_files = len(current_scan)

            logging.info(f"Scan complete. Total files checked: {total_files}")
            if has_changes:
                logging.info(
                    f"Summary: {new_count} New, {mod_count} Modified, {del_count} Deleted."
                )

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
