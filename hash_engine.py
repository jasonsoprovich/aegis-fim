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
            abs_path = os.path.abspath(os.path.join(root, file))
            file_hash = "placeholder function"
            baseline[abs_path] = file_hash

    return baseline
