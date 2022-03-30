import urllib.request
from urllib.parse import urlparse
from pathlib import Path
import ftplib
import os


def get_example_data():
    dir = Path(__file__).resolve().parent
    ftp_path = 'ftp://iacftp.ethz.ch/pub_read/alauber/'
    url_parts = urlparse(ftp_path)
    domain = url_parts.netloc
    path = url_parts.path
    ftp = ftplib.FTP(domain)
    ftp.login()
    ftp.cwd(path)
    filenames = ftp.nlst()
    example_data_dir = Path(dir, 'example_data')

    if not example_data_dir.exists():
        os.mkdir(example_data_dir)
    for directory in filenames:
        try:
            ftp.cwd(directory)
            print(' ')
            print('Getting data from folder: ' + str(directory))
            filenames = ftp.nlst()
            for file_to_retrieve in filenames:
                target_dir = Path(example_data_dir, directory)
                if not target_dir.exists():
                    os.mkdir(target_dir)
                target_loc = Path(target_dir, file_to_retrieve)
                if not target_loc.is_file():
                    source_file = ftp_path + directory + '/' + file_to_retrieve
                    print(str(source_file) + ' --> ' + str(target_loc))
                    urllib.request.urlretrieve(source_file, str(target_loc))
            ftp.cwd(path)
        except ftplib.error_perm as detail:
            continue  # print("It's probably not a directory:", detail)
    ftp.quit()


if __name__ == "__main__":
    get_example_data()
