"""
Utility functions for subtitle manipulation.

This module provides functionalities to:
- Detect the encoding of subtitle files (.srt).
- Rename subtitle files to match associated movie files.
- Convert subtitle files to UTF-8 encoding.
"""
import codecs
import os

def get_subtitle_encoding(subtitle_file_path):
    """
    Attempts to detect the encoding of a given subtitle file.

    It tries a list of common encodings ('utf-8', 'windows-1256', 'iso-8859-7').
    The first encoding that successfully decodes the file is returned.

    Args:
        subtitle_file_path (str): The full path to the subtitle file.

    Returns:
        str: The detected encoding string if successful (e.g., 'utf-8').
             Returns 'not_detected' if the file is not found or if none of the
             tried encodings work.
    
    Prints:
        Error messages if the file is not found.
        Messages indicating which encoding is being tried.
        Success or failure messages for encoding detection.
    """
    encodings = ['utf-8', 'windows-1256', 'iso-8859-7'] # Common encodings to try

    # Check if the subtitle file exists
    if not os.path.exists(subtitle_file_path):
        print(f"Error: File not found at {subtitle_file_path}")
        return 'not_detected'

    for e in encodings:
        try:
            # Attempt to open and read the file with the current encoding
            with codecs.open(subtitle_file_path, 'r', encoding=e) as fh:
                fh.readlines()  # Try reading the lines to trigger UnicodeDecodeError if encoding is wrong
            # If open and readlines were successful, this encoding is correct
            print(f'Successfully opened and read file {subtitle_file_path} with encoding: {e}')
            return e
        except UnicodeDecodeError:
            # This encoding is incorrect, try the next one
            print(f'Got unicode error with {e} for file {subtitle_file_path}, trying different encoding.')
        except Exception as ex:
            # This catches other errors like invalid encoding name for codecs.open itself,
            # or other OS related errors during open.
            print(f"Error opening/reading file {subtitle_file_path} with encoding {e}: {ex}")
            # It's considered safer to continue to the next encoding if one attempt fails
            # for reasons other than UnicodeDecodeError.
    
    # If loop completes, no suitable encoding was found
    print(f"Could not determine encoding for {subtitle_file_path} after trying {', '.join(encodings)}.")
    return 'not_detected'

def rename_subtitles(path):
    """
    Renames .srt subtitle files in a directory to match a movie file name.

    It first searches for a movie file (extensions: .mp4, .mkv, .avi) in the
    specified path. If found, it uses its name (without extension) as the base
    for renaming .srt files.
    If multiple .srt files exist, they are numbered (e.g., movie.1.srt, movie.2.srt).
    If only one .srt file exists, it's renamed to movie.srt.
    Renaming occurs in the original directory of each .srt file.

    Args:
        path (str): The directory path to search for movie and subtitle files.
                    This function will walk through subdirectories as well.
    
    Prints:
        Informative messages about files found, renaming actions, or errors.
    """
    filename_without_ext = None # To store the movie filename without its extension
    movie_files_found = False
    
    # Search for a movie file to use its name as a base
    # os.walk will go through the 'path' directory and all its subdirectories
    for r, d, f_list in os.walk(path): # r=root, d=directories, f_list=files
        for file_name in f_list:
            if file_name.endswith(('.mp4', '.mkv', '.avi')): # Check for common movie extensions
                filename_without_ext = os.path.splitext(file_name)[0]
                movie_files_found = True
                # Assuming one primary movie file per folder structure,
                # or the first one found in the walk will be used.
                # Break from inner loop once a movie file is found in current directory
                break 
        if movie_files_found:
            # Break from outer loop if movie file is found to prevent using a movie file from a deeper subdirectory
            # if one exists at a higher level. This prioritizes movie files closer to the initial 'path'.
            break

    # If no movie file was found anywhere in the path, cannot proceed with renaming.
    if not movie_files_found:
        print(f"No movie files (.mp4, .mkv, .avi) found in '{path}' or its subdirectories. Cannot rename subtitles.")
        return

    srt_files = [] # To store full paths of all .srt files found
    # Walk again (or could collect during first walk if logic is more complex)
    # to find all .srt files in the directory and subdirectories.
    for r, dirs, files_in_dir in os.walk(path):
        for file_name in files_in_dir:
            if file_name.endswith('.srt'):
                srt_files.append(os.path.join(r, file_name)) # Store the full path

    srtCounter = len(srt_files)

    if srtCounter == 0:
        print(f"No subtitle files (.srt) found in '{path}' or its subdirectories.")
        return

    # Rename the collected .srt files
    counter = 1 # For numbering if multiple srt files
    for srt_file_full_path in srt_files:
        original_dir = os.path.dirname(srt_file_full_path) # Get the directory of the current .srt file
        
        # Determine the new name for the subtitle file
        if srtCounter == 1: # Only one srt file
            new_subtitle_name = filename_without_ext + '.srt'
        else: # Multiple srt files, append a counter
            new_subtitle_name = f"{filename_without_ext}.{counter}.srt"
        
        new_file_path = os.path.join(original_dir, new_subtitle_name) # Construct full path for the new name

        try:
            # Perform the rename operation
            os.rename(srt_file_full_path, new_file_path)
            print(f"Renamed '{srt_file_full_path}' to '{new_file_path}'")
        except OSError as e:
            # Handle potential errors during renaming (e.g., file locked, permissions)
            print(f"Error renaming file {srt_file_full_path} to {new_file_path}: {e}")
        counter += 1


def encode_subtitles(path):
    """
    Converts all .srt files within the specified path (and its subdirectories) to UTF-8 encoding.

    For each .srt file:
    1. Its current encoding is detected using `get_subtitle_encoding`.
    2. If the encoding is 'not_detected' or already 'utf-8', the file is skipped.
    3. Otherwise, the file is read using its detected encoding and then
       overwritten with its content re-encoded in UTF-8.

    Args:
        path (str): The root directory path to search for .srt files.
    
    Prints:
        Messages about skipping files, re-encoding actions, or errors encountered.
    """
    # Walk through the directory tree
    for root, dirs, files_in_dir in os.walk(path):
        for file_name in files_in_dir:
            if file_name.endswith('.srt'):
                subtitle_full_path = os.path.join(root, file_name)
                
                # Step 1: Detect current encoding
                print(f"Processing encoding for: {subtitle_full_path}")
                encoding = get_subtitle_encoding(subtitle_full_path)

                # Step 2: Check if re-encoding is needed
                if encoding == 'not_detected':
                    print(f'Cannot determine encoding for {subtitle_full_path}. Skipping re-encoding.')
                    continue # Move to the next file
                if encoding == 'utf-8':
                    print(f'{subtitle_full_path} is already UTF-8. Skipping re-encoding.')
                    continue # Move to the next file
                
                # Step 3: Re-encode to UTF-8
                print(f"Re-encoding '{subtitle_full_path}' from {encoding} to UTF-8...")
                try:
                    # Read the file with its original encoding
                    with codecs.open(subtitle_full_path, "r", encoding=encoding) as myfile:
                        data = myfile.read()
                    
                    # Write the file back in UTF-8
                    # Note: It's generally safer to write to a temporary file first, then replace the original.
                    # For simplicity in this context, it overwrites the original file directly.
                    with codecs.open(subtitle_full_path, "w", "utf-8") as outfile:
                        outfile.write(data)
                    print(f"Successfully re-encoded '{subtitle_full_path}' to UTF-8.")
                except Exception as e:
                    # Handle potential errors during file reading or writing
                    print(f"Error re-encoding file {subtitle_full_path}: {e}")
