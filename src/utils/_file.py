from result import Result, Ok

from src.utils.decorators import run_safety


class FileUtils:
    @staticmethod
    @run_safety
    def human_readable_size(size: int) -> Ok[str]:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return Ok(f"{size:.2f} {unit}")
            size /= 1024.0
        return Ok(f"{size:.2f} PB")
