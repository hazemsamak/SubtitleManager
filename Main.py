from SubtitleDownloader import download_subtitle
from SubtitleUtils import *

def main():
    path = input("Enter the movie directory: ")
    # path = 'C:/Personal/Movies/Arctic (2018) [BluRay] [1080p] [YTS.AM]'
    # url = 'https://subscene.com/subtitles/arabic-text/3BOzjl8fipkftcdka8dUn4NgCJS8M9MSjySWO_Xsi0ADZt7bskeUGFrUJAaivMScqYB_rzXh8gQIGNcgZstjTMke2ok3IP182OVKvCceWxHHYNa81-IIqae8VMoek-SW0'
    url = input("Enter subtitle download url: ")
    download_subtitle(url, path)
    rename_subtitles(path)
    encode_subtitles(path)

if __name__ == "__main__":
    main()