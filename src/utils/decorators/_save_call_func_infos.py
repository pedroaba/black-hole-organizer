import pickle
from pathlib import Path

from typing import Any, Tuple


def save_call_func_infos(args: Tuple[Any, ...], filename_caller: Path) -> None:
    try:
        if not filename_caller.parent.exists():
            filename_caller.parent.mkdir(parents=True)

        with open(f"{filename_caller}.pickle", 'wb') as file:
            pickle.dump(args, file=file, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print(e)
