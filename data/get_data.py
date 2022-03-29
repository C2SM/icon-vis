import urllib.request
from urllib.parse import urlparse
from pathlib import Path
import ftplib
import os


def get_data():
    dir = Path(__file__).resolve().parent
    ftp_path = 'ftp://iacftp.ethz.ch/pub_read/alauber/'

    file01 = 'my_exp1_atm_3d_ml_20180921T000000Z.nc'
    file01_dir = Path(dir, file01)
    if not file01_dir.is_file():
        file01_ftp = ftp_path + file01
        urllib.request.urlretrieve(file01_ftp, str(file01_dir))

    file02 = 'lfff01000000.nc'
    file02_dir = Path(dir, file02)
    if not file02_dir.is_file():
        file02_ftp = ftp_path + file02
        print(file02_ftp, file02_dir)
        urllib.request.urlretrieve(file02_ftp, str(file02_dir))

    file03 = 'ICON-1E_DOM01.nc'
    file03_dir = Path(dir, file03)
    if not file03_dir.is_file():
        file03_ftp = ftp_path + file03
        urllib.request.urlretrieve(file03_ftp, str(file03_dir))

    file04 = 'icon_19790101T000000Z.nc'
    file04_dir = Path(dir, file04)
    if not file04_dir.is_file():
        file04_ftp = ftp_path + file04
        print(file04_ftp, file04_dir)
        urllib.request.urlretrieve(file04_ftp, str(file04_dir))

    file05 = 'icon_19790101T000000Zc.nc'
    file05_dir = Path(dir, file05)
    if not file05_dir.is_file():
        file05_ftp = ftp_path + file05
        print(file05_ftp, file05_dir)
        urllib.request.urlretrieve(file05_ftp, str(file05_dir))

    file06 = 'my_exp1_diff.nc'
    file06_dir = Path(dir, file06)
    if not file06_dir.is_file():
        file06_ftp = ftp_path + file06
        print(file06_ftp, file06_dir)
        urllib.request.urlretrieve(file06_ftp, str(file06_dir))

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
    get_data()
    get_example_data()
