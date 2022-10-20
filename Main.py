from SubtitleDownloader import download_subtitle
from SubtitleUtils import *

def main():
    # Test modifying the file
    path = input("Enter the movie directory: ")
    url = input("Enter subtitle download url: ")
    download_subtitle(url, path)
    rename_subtitles(path)
    encode_subtitles(path)

if __name__ == "__main__":
    main()