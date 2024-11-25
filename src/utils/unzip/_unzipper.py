import shutil
import pathlib
import zipfile

from result import Result, Ok
from colorama import Style, Fore

from src.utils import file_utils
from src.utils.logger import logger
from src.utils.decorators import run_safety


class Unzipper:
    def __init__(self):
        pass

    @run_safety
    def unzip(self, path: pathlib.Path):
        destination = pathlib.Path(path.parent / path.name.replace(".zip", ""))

        self._reset_destination_path(destination)
        self._get_folder_destination_size(destination)

        with zipfile.ZipFile(path) as zip_file:
            filelist = zip_file.infolist()
            total_of_size = sum([file.file_size for file in filelist])

            total_of_size_humanized = f"{Style.DIM}{Fore.BLUE}{file_utils.human_readable_size(total_of_size).ok_value}{Style.RESET_ALL}"
            logger.info(f"Total compressed files: {total_of_size} -> {total_of_size_humanized}")

            for file in filelist:
                logger.info(f"Extracting file: {file.filename}")

                zip_file.extract(file, destination)

    @run_safety
    def _get_folder_destination_size(self, destination_folder: pathlib.Path) -> Result[int, str]:
        total_of_folder_size = 0
        logger.info(f"Getting folder size: {destination_folder}")
        for path in destination_folder.rglob("*"):
            if path.is_file():
                total_of_folder_size += path.stat().st_size
                logger.info("Found file: {path} | Size: {filesize}".format(path=path, filesize=path.stat().st_size))
            else:
                logger.info("Found folder: {path}".format(path=path))

        total_of_size_humanized = f"{Style.DIM}{Fore.BLUE}{file_utils.human_readable_size(total_of_folder_size).ok_value}{Style.RESET_ALL}"
        logger.success(f"Folder Size: {total_of_folder_size} -> {total_of_size_humanized}")
        return Ok(total_of_folder_size)

    @run_safety
    def _reset_destination_path(self, destination_folder: pathlib.Path):
        shutil.rmtree(destination_folder, ignore_errors=True)


if __name__ == '__main__':
    unzipper = Unzipper()
    unzipper.unzip(pathlib.Path(r"C:\Users\pedro\Downloads\OneDrive_2024-11-18\Listas de Exercícios\F02 - 3ª LISTA DE EXERCÍCIOS.zip"))
