import os
import sys
import time
import hashlib
import requests
import platform
from prettytable import PrettyTable


def calculate_hashes(file_path):
    """Calculate MD5, SHA-1, and SHA-256 hashes for a given file.

    Args:
        file_path (str): Path of the file to calculate the hashes for.

    Returns:
        A tuple containing the MD5, SHA-1, and SHA-256 hashes for the file.
    """
    hasher_md5 = hashlib.md5()
    hasher_sha1 = hashlib.sha1()
    hasher_sha256 = hashlib.sha256()

    with open(file_path, 'rb') as file:
        # Read the file in chunks to save memory.
        buf = file.read(65536)
        while len(buf) > 0:
            hasher_md5.update(buf)
            hasher_sha1.update(buf)
            hasher_sha256.update(buf)
            buf = file.read(65536)

    return hasher_md5.hexdigest(), hasher_sha1.hexdigest(), hasher_sha256.hexdigest()


def classify_malware(file_hashes, malware_classification):
    """Classify a file as malware based on its hashes.

    Args:
        file_hashes (tuple): A tuple containing the MD5, SHA-1, and SHA-256 hashes for a file.
        malware_classification (dict): A dictionary mapping hash values to malware types.

    Returns:
        The malware type if the file's hash matches one in the malware_classification dictionary, otherwise "Unknown".
    """
    for hash_value in file_hashes:
        if hash_value in malware_classification:
            return malware_classification[hash_value]
    return "Unknown"


def scan_file(file_path, malicious_hashes, malware_classification, table):
    """Scan a file for malware.

    Args:
        file_path (str): Path of the file to scan.
        malicious_hashes (set): A set containing hash values for known malicious files.
        malware_classification (dict): A dictionary mapping hash values to malware types.
        table (PrettyTable): A pretty table object to display the results.

    Returns:
        None
    """
    file_hashes = calculate_hashes(file_path)
    for hash_value in file_hashes:
        if hash_value in malicious_hashes:
            malware_type = classify_malware(
                file_hashes, malware_classification)
            table.add_row([file_path, malware_type])
            # Clear the console before printing the table.
            os.system('cls' if platform.system() == 'Windows' else 'clear')
            print(table)
            break


def scan_directory(directory, malicious_hashes, malware_classification, counter, table):
    """Scan a directory for malware.

    Args:
        directory (str): Path of the directory to scan.
        malicious_hashes (set): A set containing hash values for known malicious files.
        malware_classification (dict): A dictionary mapping hash values to malware types.
        counter (list): A list containing a counter for the number of files scanned.
        table (PrettyTable): A pretty table object to display the results.

    Returns:
        A list containing the updated counter.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                scan_file(file_path, malicious_hashes,
                          malware_classification, table)
                counter[0] += 1
            except PermissionError:
                # Ignore files that the user does not have permission to read.
                pass
            except KeyboardInterrupt:
                # If the user interrupts the program, stop scanning.
                raise

    return counter


if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/king04aman/Malware-Scanner/main/hashes.txt"
    response = requests.get(url)
    malicious_hashes = set(response.text.splitlines())

    malware_classification = {
        "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8": "Ransomware",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Trojan",
        "8754c2a98e3b9c86aa49d4a35b8835e5fc6d5e6f53d6bce44a7f8db9c524de7a": "Virus",
        "3dc3c3f1bce75e029b1c7a8db9a20dfb2c6f68c925b1898db0d49f7a1d0520a6": "Spyware",
        "d301f9c47a8dd8331c4597feefcb056d08e3a3b4c4f4d03f9c1436a1a5f5b6b5": "Adware",
        "1e8a9f5127d527fb9c97d7fd8be2b883cc7f75e20e437d7b19db69b42c42220c": "Worm"
    }

    if platform.system() == 'Windows':
        directories_to_scan = ["C:\\", "D:\\", "E:\\"]
    elif platform.system() == 'Linux':
        directories_to_scan = ["/usr", "/home", "/"]
    else:
        print("This operating system is not supported.")
        directories_to_scan = []

    start_time = time.time()
    counter = [0]

    table = PrettyTable()
    table.field_names = ["File Path", "Hazard Type"]

    try:
        for directory in directories_to_scan:
            counter = scan_directory(
                directory, malicious_hashes, malware_classification, counter, table)
    except KeyboardInterrupt:
        print("The program has been stopped by the user")

    end_time = time.time()
    elapsed_time = end_time - start_time

    os.system('cls' if platform.system() ==
              'Windows' else 'clear')
    print(table)
    print(f"\nTotal Scanned files: {counter[0]}")
    print(f"Program Execution time: {elapsed_time:.2f} seconds")
