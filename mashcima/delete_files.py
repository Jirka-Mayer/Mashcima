# If you lanuch this script via:
#
#    python -m mashcima.delete_files
#
# it will clean up any downloaded datasets and cached data.
# Use this command before uninstalling mashcima from your machine.

from mashcima.Config import Config

if __name__ == "__main__":
    cfg = Config.automatic_download_config(download=False)
    cfg.delete_mashcima_dir()
