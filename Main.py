"""
Main script for the Subtitle Processing Tool.

This script orchestrates the downloading, renaming, and re-encoding of subtitles.
It prompts the user for a movie directory and a subtitle download URL,
then uses utility modules to perform the necessary operations.
"""
from SubtitleDownloader import download_subtitle
from SubtitleUtils import rename_subtitles, encode_subtitles # Explicitly import for clarity

def main():
    """
    Main function to drive the subtitle processing workflow.

    Prompts the user for a movie directory and a subtitle download URL.
    It then calls functions to:
    1. Download subtitles from the given URL to the specified directory.
    2. Rename the downloaded .srt files to match the movie file name.
    3. Encode the .srt files to UTF-8.
    Includes basic error handling for the overall process.
    """
    try:
        # Get user input for movie directory and subtitle URL
        path = input("Enter the movie directory: ")
        if not path: # Basic validation for path
            print("Movie directory cannot be empty.")
            return

        url = input("Enter subtitle download url: ")
        if not url: # Basic validation for URL
            print("Subtitle download URL cannot be empty.")
            return

        print(f"\nStarting subtitle processing for directory: {path}")
        
        # Step 1: Download subtitles
        print("\n--- Downloading subtitles ---")
        download_subtitle(url, path)
        
        # Step 2: Rename subtitles
        print("\n--- Renaming subtitles ---")
        rename_subtitles(path)
        
        # Step 3: Encode subtitles
        print("\n--- Encoding subtitles ---")
        encode_subtitles(path)
        
        print("\nSubtitle processing completed successfully.")
        
    except Exception as e:
        # Catch-all for any unexpected errors during the process
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check the input values, network connection, and ensure the target directory and files are accessible.")

if __name__ == "__main__":
    # This ensures main() is called only when the script is executed directly
    main()