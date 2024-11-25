import os
import uuid
import platform

from pathlib import Path
from typing import Literal
from dataclasses import dataclass

from appdata import AppDataPaths

from src.exceptions.system import UnknownOperationalSystem

APP_NAME = "BOO"


@dataclass(frozen=True, init=False)
class AppConfig:
    app_name: str = APP_NAME
    app_id: str = f"{APP_NAME}__{uuid.uuid4()}"
    _app_data = AppDataPaths(APP_NAME)

    @property
    def execution_id(self):
        return f"{self.app_id}__{self.running_os}__{os.getpid()}"

    @property
    def log_folder(self) -> Path:
        return Path(self._app_data.logs_path)

    @property
    def app_folder(self) -> Path:
        return Path(self._app_data.app_data_path)

    @property
    def config_file(self) -> Path:
        return Path(self._app_data.config_path)

    @property
    def temp_folder(self) -> Path:
        temp_folder = self.app_folder / "temp"
        if not temp_folder.exists():
            temp_folder.mkdir(exist_ok=True)
        return temp_folder

    @property
    def args_log_folder(self) -> Path:
        args_log_folder = self.log_folder / "args"
        if not args_log_folder.exists():
            args_log_folder.mkdir(exist_ok=True)
        return args_log_folder

    @property
    def running_os(self) -> Literal["windows", "linux", "macos"]:
        system = platform.system()
        match system.upper():
            case "WINDOWS":
                return "windows"
            case "LINUX":
                return "linux"
            case "DARWIN":
                return "macos"
            case _:
                raise UnknownOperationalSystem(f"Unknown OS: {system}!")

    @property
    def current_execution_path(self) -> Path:
        return Path(__file__).parent.parent

    def get_log_filepath(self, filename: str, *, _extra_folders: list[str] = None) -> Path:
        filepath = self.log_folder
        if _extra_folders is not None:
            for folder in _extra_folders:
                filepath /= folder
        return filepath / filename

    def __repr__(self):
        return f"<App appname='{self.app_name}'>"
