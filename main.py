import argparse
import logging
import os

from rich.logging import RichHandler

from data_manager import load_baseline, save_baseline
from hash_engine import compare_baseline, set_baseline
from ui import display_header, display_results, display_summary, status_update

os.makedirs("./logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        logging.FileHandler("./logs/audit.log"),
        RichHandler(rich_tracebacks=True),
    ],
)


def main():
    display_header()

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

    logging.info(f"Scanning: {target}.")
    with status_update("[bold green]Hashing files..."):
        current_scan = set_baseline(target, default_ignores)
    old_baseline = load_baseline(baseline_filename)

    if old_baseline is None:
        print("First run detected. Saving baseline.")
        save_baseline(current_scan, baseline_filename)
        print("Baseline established. Run again to scan for changes.")
    else:
        logging.info("Existing baseline found. Comparing files.")
        changes = compare_baseline(old_baseline, current_scan)

        has_changes = changes["new"] or changes["modified"] or changes["deleted"]

        if not has_changes:
            logging.info("No changes detected. Integrity verified.")
        else:
            display_results(changes)

            new_count = len(changes["new"])
            mod_count = len(changes["modified"])
            del_count = len(changes["deleted"])
            total_files = len(current_scan)

            display_summary(total_files, new_count, mod_count, del_count)

            if update_mode:
                confirm = input(
                    "\nChanges detected. Would you like to update the baseline? (y/n): "
                )
                if confirm.lower() == "y":
                    save_baseline(current_scan, baseline_filename)
                    print("Baseline updated.")


if __name__ == "__main__":
    main()
