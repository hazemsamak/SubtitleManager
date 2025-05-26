"""
Utility for downloading and managing subtitle files.

This module provides functions to:
- Clean a target folder of existing subtitle-related files (.srt, .zip).
- Download a subtitle zip archive from a URL.
- Extract subtitles from the downloaded zip archive.
- Handle potential errors during download and extraction.
"""
import requests
import zipfile
import os

def download_subtitle(url, path):
    """
    Downloads and extracts subtitles from a given URL into the specified path.

    The process involves:
    1. Cleaning the target path of any pre-existing .srt or .zip files.
    2. Downloading the zip file from the URL.
    3. Extracting all contents of the zip file into the path.
    4. Deleting the downloaded zip file after extraction.

    Args:
        url (str): The URL from which to download the subtitle zip file.
        path (str): The local directory path where the subtitles should be
                    extracted and where the temporary zip file will be stored.

    Prints:
        Informative messages about the download and extraction process.
        Error messages if issues occur during download (e.g., network problems,
        HTTP errors) or zip file processing (e.g., corrupted zip file).
    """
    # Ensure the target directory is clean before downloading new subtitles.
    clean_folder(path)
    print('Downloading new subtitle zip file...')
    zip_file_path = os.path.join(path, 'sub.zip')

    try:
        # Make the GET request to download the file
        myfile = requests.get(url, timeout=10) # Added timeout for robustness
        myfile.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        # Handle network errors, timeout, or bad HTTP status codes
        print(f"Error downloading subtitle from {url}: {e}")
        return # Exit the function if download fails

    try:
        # Write the downloaded content to a local zip file
        with open(zip_file_path, 'wb') as f:
            f.write(myfile.content)
        
        print(f'Extracting subtitles from {zip_file_path} to {path}...')
        # Extract the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(path)
        print('Extraction complete.')
    except zipfile.BadZipFile:
        # Handle cases where the downloaded file is not a valid zip or is corrupted
        print(f"Error: '{zip_file_path}' is not a valid zip file or is corrupted.")
    except Exception as e:
        # Catch other potential errors during file writing or zip extraction
        print(f"An error occurred during zip file processing: {e}")
    finally:
        # Ensure the temporary zip file is removed, even if errors occurred
        if os.path.exists(zip_file_path):
            try:
                os.remove(zip_file_path)
                print(f"Temporary file {zip_file_path} removed.")
            except OSError as e:
                print(f"Error removing temporary file {zip_file_path}: {e}")

def clean_folder(path):
    """
    Removes all .srt and .zip files from the specified directory and its subdirectories.

    Args:
        path (str): The root directory path from which .srt and .zip files
                    will be recursively deleted.

    Prints:
        A message indicating the directory being cleaned.
        Error messages if a file cannot be deleted due to an OSError.
    """
    print(f'Cleaning directory: {path} (deleting *.srt and *.zip files)...')
    # Walk through the directory tree
    for root_dir, _, files_in_dir in os.walk(path): # Renamed variables for clarity
        for file_name in files_in_dir:
            # Check if the file is an .srt or .zip file
            if file_name.endswith('.srt') or file_name.endswith('.zip'):
                file_path_to_remove = os.path.join(root_dir, file_name)
                try:
                    os.remove(file_path_to_remove)
                    # print(f"Deleted: {file_path_to_remove}") # Optional: for verbose logging
                except OSError as e:
                    # Handle errors during file deletion (e.g., permission issues)
                    print(f"Error deleting file {file_path_to_remove}: {e}")
    print(f"Cleaning of {path} complete.")
