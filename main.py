import argparse
import json
import logging
import os

from rich.logging import RichHandler

from data_manager import export_report, load_baseline, save_baseline
from hash_engine import collect_files, compare_baseline, set_baseline
from ui import (
    create_scan_progress,
    display_errors,
    display_header,
    display_results,
    display_summary,
)

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
    parser.add_argument(
        "path", nargs="?", help="Target directory for integrity analysis"
    )

    parser.add_argument(
        "-b",
        "--baseline",
        default="./data/baseline.json",
        help="Path to the baseline storage file (default: ./data/baseline.json)",
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Interactively update the baseline if discrepancies are identified",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        nargs="+",
        help="List of filenames or directory patterns to exclude from the audit",
    )
    parser.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="Enable persistent real-time filesystem monitoring",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying the stored baseline",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable detailed output, listing every file scanned during the audit",
    )
    parser.add_argument(
        "-e",
        "--export",
        help="Export the audit results to a JSON file",
    )
    parser.add_argument("-c", "--config", help="Path to a JSON configuration file")

    args = parser.parse_args()

    if args.config:
        if os.path.exists(args.config):
            try:
                with open(args.config, "r") as f:
                    config_data = json.load(f)
                for key, value in config_data.items():
                    if hasattr(args, key) and (
                        getattr(args, key) is None or getattr(args, key) is False
                    ):
                        setattr(args, key, value)
                logging.info(f"Configuration loaded from : {args.config}")
            except Exception as e:
                logging.error(f"Failed to load config: {e}")
        else:
            logging.error(f"Config file not found: {args.config}")

    if args.path is None:
        logging.error("No target path provided via CIA or Config")
        return

    target = args.path
    baseline_filename = args.baseline
    update_mode = args.update
    dry_run = args.dry_run
    verbose_mode = args.verbose
    export_mode = args.export

    default_ignores = ["logs", "data", ".DS_Store", ".git"]
    default_ignores.append(os.path.basename(baseline_filename))

    if args.ignore:
        default_ignores.extend(args.ignore)

    if not os.path.exists(target):
        print(f"Directory {target} not found.")
        return

    logging.info(f"Scanning: {target}.")

    files_to_scan = collect_files(target, default_ignores)
    total_files = len(files_to_scan)

    current_scan = {}
    scan_errors = {}

    with create_scan_progress() as progress:
        task = progress.add_task("[cyan]Auditing integrity...", total=total_files)
        current_scan, scan_errors = set_baseline(
            files_to_scan, progress, task, verbose=verbose_mode
        )
        progress.update(task, completed=total_files)

    if scan_errors:
        display_errors(scan_errors)

    old_baseline = load_baseline(baseline_filename)

    if old_baseline is None:
        if dry_run:
            logging.info(
                "[DRY RUN] Initial state captured. Baseline write-back skipped."
            )
        else:
            logging.info("Initial run: Establishing cryptographic baseline.")
            save_baseline(current_scan, baseline_filename)
    else:
        logging.info("Baseline loaded. Commencing integrity comparison.")
        changes = compare_baseline(old_baseline, current_scan)

        has_changes = any(changes.values())

        if not has_changes:
            logging.info("Integrity Verified: No unauthorized changes detected.")
        else:
            display_results(changes)

            display_summary(
                len(current_scan),
                len(changes["new"]),
                len(changes["modified"]),
                len(changes["deleted"]),
                len(changes["metadata_changed"]),
            )

            if export_mode:
                summary_stats = {
                    "total_files": total_files,
                    "new": len(changes["new"]),
                    "modified": len(changes["modified"]),
                    "deleted": len(changes["deleted"]),
                    "metadata_changed": len(changes["metadata_changed"]),
                }
                try:
                    export_report(changes, summary_stats, export_mode)
                    logging.info(f"Audit report exported to: {export_mode}")
                except Exception as e:
                    logging.error(f"Failed to export report: {e}")

            if update_mode:
                if dry_run:
                    logging.info(
                        "[DRY RUN] Update requested. Disk write-back suppressed."
                    )
                else:
                    confirm = input(
                        "\nDiscrepancies found. Synchronize baseline with current state? (y/n):"
                    )
                    if confirm.lower() == "y":
                        save_baseline(current_scan, baseline_filename)
                        logging.info("Baseline successfully synchronized.")

        if args.watch:
            from monitor import start_realtime_monitor

            start_realtime_monitor(target, current_scan, default_ignores)


if __name__ == "__main__":
    main()
