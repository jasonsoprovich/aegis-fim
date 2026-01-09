import os

# def list_files_recursively(path="."):
#     for entry in os.listdir(path):
#         full_path = os.path.join(path, entry)
#         if os.path.isdir(full_path):
#             list_files_recursively(full_path)
#         else:
#             print(full_path)


def set_baseline(directory):
    baseline = {}
    for root, _, files in os.walk(directory):
        for file in files:
            relative_path = os.path.join(root, file)
            abs_path = os.path.abspath(relative_path)
            file_hash = "placeholder function"
            baseline[abs_path] = file_hash

    return baseline


if __name__ == "__main__":
    target = "./test_dir"
    print(f"Scanning {target}")
    current_baseline = set_baseline(target)

    for path, file_hash in current_baseline.items():
        print(f"{path} -> file-hash-placeholder")
