from pathlib import Path

from src.settings import application_config


class TemporaryFiles:
    @staticmethod
    def get_temp_file_path(filename: str) -> Path:
        return application_config.temp_folder / f'{filename}.temp'
