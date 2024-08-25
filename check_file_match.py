import os
import hashlib


def get_file_hash(filepath):
    """Return the SHA-256 hash of the file."""
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def compare_folders(input_folder1, input_folder2):
    # Get list of files in both folders
    files_folder1 = set(os.listdir(input_folder1))
    files_folder2 = set(os.listdir(input_folder2))

    # Find common files in both folders
    common_files = files_folder1.intersection(files_folder2)

    # Check if the files with the same name are identical
    identical_files = []
    different_files = []

    for file_name in common_files:
        file1_path = os.path.join(input_folder1, file_name)
        file2_path = os.path.join(input_folder2, file_name)

        if os.path.isfile(file1_path) and os.path.isfile(file2_path):
            # Compare file hashes
            if get_file_hash(file1_path) == get_file_hash(file2_path):
                identical_files.append(file_name)
            else:
                different_files.append(file_name)

    return identical_files, different_files


# Example usage
folder1 = 'path_to_first_folder'
folder2 = 'path_to_second_folder'


identical, different = compare_folders(folder1, folder2)

print("Identical files:")
for file in identical:
    print(file)

print("\nDifferent files:")
for file in different:
    print(file)
