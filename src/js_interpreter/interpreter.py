import subprocess

from typing import TypedDict, Optional, Union
from result import Result, Err, Ok


class InterpreterProps(TypedDict):
    node_version: Optional[str]


class Interpreter:
    def __init__(self, props: InterpreterProps):
        self._props = props

        self._check_if_node_is_installed()
        self._node_version_on_machine = self._check_if_node_is_installed()
        if self._node_version_on_machine not in [None, "unknown"]:
            print("Installing node version specified")

    @staticmethod
    def _check_if_node_is_installed() -> Result[bool, str]:
        try:
            node_version_output_command = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
            node_version_detected = node_version_output_command.stdout.strip()

            print(f"Detected Node: {node_version_detected}")
            return Ok(True)
        except subprocess.CalledProcessError:
            return Ok(False)
        except FileNotFoundError:
            return Ok(False)
        except Exception as e:
            print(e)  # upload to log platform

            return Err("Occurred unable to execute interpreter")


    @staticmethod
    def _check_node_version() -> Result[Union[str, None], str]:
        try:
            node_version_output_command = subprocess.run(["node", "--version"], capture_output=True, text=True,
                                                         check=True)
            node_version_detected = node_version_output_command.stdout.strip()

            return Ok(node_version_detected)
        except subprocess.CalledProcessError:
            return Ok(None)
        except FileNotFoundError:
            return Ok(None)
        except Exception as e:
            print(e)  # upload to log platform

            return Err("unknown")


if __name__ == '__main__':
    interpreter = Interpreter({"node_version": "20"})
