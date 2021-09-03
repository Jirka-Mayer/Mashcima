import os
import appdirs
import shutil
import requests
import tqdm
import zipfile


def download_file(url, path):
    print("Downloading " + url)
    print("and saving it to " + path)
    
    # taken from:
    # https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests/37573701
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm.tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR: Download failed")
        exit(1)


class Config:
    DEFAULT_CONFIG = None
    MASHCIMA_DIR = appdirs.user_data_dir(
        appname="mashcima",
        appauthor="Jirka-Mayer"
    )
    
    @staticmethod
    def load_default():
        """Loads the DEFAULT_CONFIG static variable"""
        if Config.DEFAULT_CONFIG is None:
            Config.DEFAULT_CONFIG = Config.automatic_download_config()
        return Config.DEFAULT_CONFIG
    
    @staticmethod
    def automatic_download_config(download=True):
        cfg = Config(
            muscima_pp_path=os.path.join(
                Config.MASHCIMA_DIR,
                "MUSCIMA-pp_v1.0"
            ),
            primus_path=os.path.join(
                Config.MASHCIMA_DIR,
                "primusCalvoRizoAppliedSciences2018.tgz"
            )
        )
        
        if download:
            cfg.download_muscima_pp()
            cfg.download_primus()

        return cfg

    @staticmethod
    def manual_download_config(muscima_pp_path: str, primus_path: str):
        """
        Creates a config that uses datasets that you have yourself downloaded.

        :param str muscima_pp_path: Path to extracted MUSCIMA++ v1.0 dataset
            folder. It should contain 'data', 'specifications', 'README', ...
        :param str primus_path: Path to the compressed primus dataset
            (the file primusCalvoRizoAppliedSciences2018.tgz)
        """
        return Config(muscima_pp_path, primus_path)

    def __init__(self, muscima_pp_path: str, primus_path: str):
        self.MUSCIMA_PP_PATH = muscima_pp_path
        self.MUSCIMA_PP_CROP_OBJECT_DIRECTORY = os.path.join(
            muscima_pp_path,
            "data/cropobjects_withstaff"
        )
        self.PRIMUS_PATH = primus_path
        self.MUSCIMA_PP_DOCUMENTS_CACHE_PATH = os.path.join(
            Config.MASHCIMA_DIR,
            "muscima-pp-documents-cache.pkl"
        )

    def check_mashcima_dir(self):
        """Creates the mashcima dir if not preset"""
        if not os.path.isdir(Config.MASHCIMA_DIR):
            os.mkdir(Config.MASHCIMA_DIR)

    def download_muscima_pp(self):
        if os.path.isdir(self.MUSCIMA_PP_PATH):
            return # already downloaded

        print("Downloading MUSCIMA++ dataset...")
        downloaded_zip = os.path.join(Config.MASHCIMA_DIR, "MUSCIMA-pp_v1.0.zip")
        self.check_mashcima_dir()
        download_file(
            "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-2372/MUSCIMA-pp_v1.0.zip",
            downloaded_zip
        )
        print("Extracting the zip...")
        with zipfile.ZipFile(downloaded_zip, 'r') as zip_ref:
            zip_ref.extractall(Config.MASHCIMA_DIR)
        print("Moving to position...")
        os.remove(downloaded_zip)
        os.rename(
            os.path.join(Config.MASHCIMA_DIR, "v1.0"),
            self.MUSCIMA_PP_PATH
        )
        print("Done.")

    def download_primus(self):
        if os.path.isfile(self.PRIMUS_PATH):
            return # already downloaded

        print("Downloading PrIMuS dataset...")
        self.check_mashcima_dir()
        download_file(
            "https://grfia.dlsi.ua.es/primus/packages/primusCalvoRizoAppliedSciences2018.tgz",
            self.PRIMUS_PATH
        )
        print("Done.")

    def delete_mashcima_dir(self):
        """Deletes the mashcima directory, cleaning up all datasets"""
        print("Cleaning up mashcima files...")
        if os.path.isdir(Config.MASHCIMA_DIR):
            shutil.rmtree(Config.MASHCIMA_DIR)
            print("Done.")
        else:
            print("There were no files to begin with. Done.")
