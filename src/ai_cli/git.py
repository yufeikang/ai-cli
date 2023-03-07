import logging
import os
import subprocess
from typing import Tuple

logger = logging.getLogger(__name__)


def _run_command(command) -> Tuple[int, bytes]:
    """Run a command in a shell.

    Args:
        command (str): The command to run.

    Returns:
        int: The exit code of the command.
        str: The output of the command.
    """
    logger.debug("Run command: {}".format(command))
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.read()
    p.wait()
    logger.debug("Command output: {}".format(output))
    return p.returncode, output


def is_exist_git_repo(path):
    """Check if the path is a git repository.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a git repository, False otherwise.
    """
    # check git command exist
    res, version = _run_command("git --version")
    if res != 0:
        logging.error("git command not found")
        return False
    return os.path.exists(os.path.join(path, ".git"))


def current_branch(path):
    """Get the current branch of the git repository.

    Args:
        path (str): The path to the git repository.

    Returns:
        str: The name of the current branch.
    """
    res, output = _run_command("git rev-parse --abbrev-ref HEAD")
    if res != 0:
        logging.error("git command failed")
        return None
    return output.decode("utf-8").strip()


def get_change_files(target):
    """Get the changed files of the git repository.

    Args:
        target (str): The target to compare with.

    Returns:
        list: The list of changed files.
    """
    res, output = _run_command("git diff --name-only {}".format(target))
    if res != 0:
        logging.error("git command failed")
        return None
    return output.decode("utf-8").strip().split("\n")


def get_file_diff(path, target):
    """Get the diff of the file.

    Args:
        path (str): The path to the file.
        target (str): The target to compare with.

    Returns:
        str: The diff of the file.
    """
    res, output = _run_command("git diff {} {}".format(target, path))
    if res != 0:
        logging.error("git command failed")
        return None
    return output.decode("utf-8").strip()


if __name__ == "__main__":
    import sys

    target = sys.argv[1]
    print(is_exist_git_repo(os.getcwd()))
    print(current_branch(os.getcwd()))
    print(get_change_files(target))
    print(get_file_diff("CHANGELOG.md", target))
