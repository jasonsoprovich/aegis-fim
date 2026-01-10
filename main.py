import os

from hash_engine import save_baseline, set_baseline


def main():
    target = "./test_dir"

    if not os.path.exists(target):
        print(f"Directory {target} not found.")
        return

    print(f"Generating baseline for: {target}.")
    current_baseline = set_baseline(target)

    baseline_filename = "./data/baseline.json"
    print(f"Saving baseline file to: {baseline_filename}.")
    save_baseline(current_baseline, baseline_filename)


# Display file:hash output
# for abs_path, file_hash in current_baseline.items():
#     short_path = os.path.relpath(abs_path, os.getcwd())

#     print(f"File: {short_path}")
#     print(f"Hash: {file_hash}")
#     print("-" * 20)


if __name__ == "__main__":
    main()
