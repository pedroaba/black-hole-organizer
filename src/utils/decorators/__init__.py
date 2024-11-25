import datetime
import inspect
import uuid

from typing import Callable, TypeAlias, Any

from result import Ok, Err

from src.settings import application_config
from src.utils.decorators import _save_call_func_infos
from src.utils.logger import logger


ReturnType = Ok[Any] | Err[Any] | Err[bool]
FuncType: TypeAlias = Callable[..., ReturnType]


def run_safety(func: FuncType) -> FuncType:
    def _safety_func(*args, **kwargs) -> ReturnType:
        try:
            caller_stack = inspect.stack()[1]
            filename = caller_stack.filename
            line_number = caller_stack.lineno

            fully_qualified_name = func.__qualname__
            logger.info(f"Called {fully_qualified_name} at {filename}:{line_number}")
            logger.debug(f"With args: {args}")

            args_filename = application_config.args_log_folder / application_config.execution_id / f"{fully_qualified_name}-{datetime.datetime.now().strftime("%m-%d-%Y-%Hh%Mm%Ss")}"
            _save_call_func_infos.save_call_func_infos(args=args, filename_caller=args_filename)

            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)

            return Err(False)

    return _safety_func
