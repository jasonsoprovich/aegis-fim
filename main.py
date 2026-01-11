import json
import os

from hash_engine import load_baseline, save_baseline, set_baseline


def main():
    target = "./test_dir"

    if not os.path.exists(target):
        print(f"Directory {target} not found.")
        return

    # Crawl target directory and generate hashes for all files
    print(f"Generating baseline for: {target}.")
    current_baseline = set_baseline(target)

    # Save filenames and hashes to new baseline json
    baseline_filename = "./data/baseline.json"
    print(f"Saving baseline file to: {baseline_filename}.")
    save_baseline(current_baseline, baseline_filename)

    # Load baseline json and print results
    print(f"Loading baseline file: {baseline_filename}")
    read_baseline_json = load_baseline(baseline_filename)
    print_output(read_baseline_json)  # debugging


def print_output(output):
    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()
