import os


def list_files_recursively(path="."):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            list_files_recursively(full_path)
        else:
            print(full_path)
