import codecs
import os
def get_subtitle_encoding(subtitle_file):

    encodings = ['utf-8', 'windows-1256', 'iso-8859-7']
    for e in encodings:
        try:
            fh = codecs.open(subtitle_file, 'r', encoding=e)
            fh.readlines()
            fh.seek(0)
        except UnicodeDecodeError:
            print('got unicode error with %s , trying different encoding' % e)
        else:
            print('opening the file with encoding:  %s ' % e)
            return e
    return 'not_detected'

def rename_subtitles(path):
    for r, d, f in os.walk(path, topdown=True):
        for file in f:
            print(file)
            if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.avi') :
                filename_without_ext = os.path.splitext(file)[0]
    srtCounter = 0
    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.srt'):
                srtCounter += 1

    try:
        filename_without_ext
    except NameError:
        print("Movie file is not existing")
    else:
        counter = 1
        for root, dirs, files in os.walk(path, topdown=True):
            for file in files:
                if file.endswith('.srt'):
                    if srtCounter == 1:
                        os.rename(os.path.join(path, file), os.path.join(path, filename_without_ext + '.srt'))
                    else:
                        os.rename(os.path.join(path, file), os.path.join(path, filename_without_ext + '.' + str(counter) + '.srt'))
                    counter += 1


def encode_subtitles(path):
    # path = 'C:/Personal/Movies/'
    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.srt'):
                encoding = get_subtitle_encoding(path + '/' + file)

                if(encoding == 'not_detected'):
                    print('Can not encode this subtitle file')

                if(encoding != 'utf-8'):
                    with codecs.open(path + '/' + file, "r", "windows-1256") as myfile:
                        data = myfile.read()
                        file = codecs.open(path + '/' + file, "w", "utf-8")
                        file.write(data)

def main():
    path = input("Enter the movie directory: ")
    encode_subtitles(path)


if __name__ == "__main__":
    main()
