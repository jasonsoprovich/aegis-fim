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
    print(f"{read_baseline_json}")


# Display file:hash output
# for abs_path, file_hash in current_baseline.items():
#     short_path = os.path.relpath(abs_path, os.getcwd())

#     print(f"File: {short_path}")
#     print(f"Hash: {file_hash}")
#     print("-" * 20)


if __name__ == "__main__":
    main()
