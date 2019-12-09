import requests
import zipfile
import os

def download_subtitle(url, path):
    clean_folder(path)
    print('Download new subtitle zip file')
    myfile = requests.get(url)
    open(path + '/sub.zip', 'wb').write(myfile.content)
    print('Extract subtitles from zip file')
    with zipfile.ZipFile(path + '/sub.zip', 'r') as zip_ref:
        zip_ref.extractall(path)
    os.remove(path + '/sub.zip')

def clean_folder(path):
    print('Delete all *.srt and *.zip in directory {}'.format(path))
    for r, d, f in os.walk(path, topdown=True):
        for file in f:
                if file.endswith('.srt') or file.endswith('.zip'):
                    os.remove(os.path.join(path, file))
