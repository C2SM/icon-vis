import urllib.request
from pathlib import Path

def get_data():
    dir = Path(__file__).resolve().parent
    ftp_path = 'ftp://iacftp.ethz.ch/pub_read/alauber/'

    file01 = 'my_exp1_atm_3d_ml_20180921T000000Z.nc'
    file01_dir = Path(dir,file01)
    if not file01_dir.is_file():
        file01_ftp = ftp_path+file01
        urllib.request.urlretrieve(file01_ftp,str(file01_dir))

    file02 = 'lfff01000000.nc'
    file02_dir = Path(dir,file02)
    if not file02_dir.is_file():
        file02_ftp = ftp_path+file02
        print(file02_ftp, file02_dir)
        urllib.request.urlretrieve(file02_ftp,str(file02_dir))

    file03 = 'ICON-1E_DOM01.nc'
    file03_dir = Path(dir,file03)
    if not file03_dir.is_file():
        file03_ftp = ftp_path+file03
        urllib.request.urlretrieve(file03_ftp,str(file03_dir))

    file04 = 'icon_19790101T000000Z.nc'
    file04_dir = Path(dir,file04)
    if not file04_dir.is_file():
        file04_ftp = ftp_path+file04
        print(file04_ftp, file04_dir)
        urllib.request.urlretrieve(file04_ftp,str(file04_dir))

    file05 = 'icon_19790101T000000Zc.nc'
    file05_dir = Path(dir,file05)
    if not file05_dir.is_file():
        file05_ftp = ftp_path+file05
        print(file05_ftp, file05_dir)
        urllib.request.urlretrieve(file05_ftp,str(file05_dir))

if __name__=="__main__":
    get_data()
