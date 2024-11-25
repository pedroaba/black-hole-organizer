import os
import zipfile
import urllib.request

from tqdm import tqdm

from src.js_interpreter.constants import NVM_DOWNLOAD_URL, NVM_DOWNLOAD_CHUNK_SIZE
from src.utils import logger
from src.utils.temp import TemporaryFiles


GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


class NvmInstallerWindows:
    def __init__(self, node_version: str):
        self.node_version = node_version
        self._download_nvm_filepath = TemporaryFiles.get_temp_file_path("nvm-setup")

    def install_nvm(self):
        self.download_nvm()

        with zipfile.ZipFile(self._download_nvm_filepath) as zip_file:
            zip_file.extractall(self._download_nvm_filepath.parent)

    def download_nvm(self):
        with urllib.request.urlopen(NVM_DOWNLOAD_URL) as download_response:
            total_size = int(download_response.info().get("Content-Length").strip())
            num_of_bars = total_size // NVM_DOWNLOAD_CHUNK_SIZE

            with open(self._download_nvm_filepath, mode="wb") as file, tqdm(
                total=num_of_bars,
                unit="B",
                unit_scale=True,
                desc="Downloading NVM",
                unit_divisor=NVM_DOWNLOAD_CHUNK_SIZE,
                bar_format=(
                        f"{GREEN}Downloading: {{percentage:.0f}}%|"
                        f"{GREEN}{{bar}}{RESET} {{n_fmt}}/{{total_fmt}} "
                        f"{RED}{{rate_fmt}} eta {BLUE}{{remaining}}{RESET}"
                ),
                ascii=" ▏▎▍▌▋▊▉█",
            ) as progress_bar:
                logger.info(f"Downloading NVM -> {file.name}")

                while True:
                    chunk = download_response.read(NVM_DOWNLOAD_CHUNK_SIZE)
                    if not chunk:
                        break

                    file.write(chunk)
                    progress_bar.update(len(chunk) // NVM_DOWNLOAD_CHUNK_SIZE)


if __name__ == "__main__":
    nvm_installer_windows = NvmInstallerWindows(node_version="latest")
    nvm_installer_windows.install_nvm()
