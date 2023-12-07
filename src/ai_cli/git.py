import logging
import os
import re
import shlex
import subprocess
import sys
from typing import Collection, Tuple, Union

logger = logging.getLogger(__name__)

DIFF_EXCLUDE = [
    "*.lock",
    "package-lock.json",
]


def _run_command(command: Union[str, Collection], output_callback=None) -> Tuple[int, bytes]:
    """Run a command in a shell.

    Args:
        command (str|list): The command to run.

    Returns:
        int: The exit code of the command.
        str: The output of the command.
    """
    if isinstance(command, list):
        command = shlex.join(command)
    logger.debug("Run command: {}".format(command))
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = b""
    if output_callback:
        while True:
            _line = p.stdout.readline()
            if not _line:
                break
            output += _line
            output_callback(_line)
    else:
        output = p.stdout.read()
        p.wait()
        logger.debug("Command output: {}".format(output))
    return p.returncode, output


def is_exist_git_repo():
    """Check if the path is a git repository.

    Returns:
        bool: True if the path is a git repository, False otherwise.
    """
    # check git command exist
    res, version = _run_command("git --version")
    if res != 0:
        logging.error("git command not found")
        return False
    res, _ = _run_command("git rev-parse --is-inside-work-tree")
    if res != 0:
        return False
    return True


def get_git_root_path():
    """Get the root path of the git repository.

    Returns:
        str: The root path of the git repository.
    """
    res, output = _run_command("git rev-parse --show-toplevel")
    if res != 0:
        logging.error("git command failed: git rev-parse --show-toplevel")
        return None
    return output.decode("utf-8").strip()


def current_branch():
    """Get the current branch of the git repository.

    Returns:
        str: The name of the current branch.
    """
    res, output = _run_command("git rev-parse --abbrev-ref HEAD")
    if res != 0:
        logging.error("git command failed: git rev-parse --abbrev-ref HEAD")
        return None
    return output.decode("utf-8").strip()


def get_change_files(target, exclude_files=None):
    """Get the changed files of the git repository.

    Args:
        target (str): The target to compare with.
        exclude_files (list): The list of files to exclude.

    Returns:
        list: The list of changed files.
    """
    if exclude_files is None:
        exclude_files = DIFF_EXCLUDE
    exclude_files_args = " ".join([":(exclude){}".format(f) for f in exclude_files])
    cmd = ["git", "--no-pager", "diff", "--cached", "--name-only", target, exclude_files_args]
    res, output = _run_command(cmd)
    if res != 0:
        logging.error("git command failed, cmd: {}".format(cmd))
        return None
    return output.decode("utf-8").strip().split("\n")


def get_file_diff(path, target):
    """Get the diff of the file.

    Args:
        path (str|list): The path to the file. If it is a list, it will be joined
        target (str): The target to compare with.

    Returns:
        str: The diff of the file.
    """
    git_root = get_git_root_path()
    current = os.getcwd()

    def _join_path(_path):
        logger.debug("path: {}".format(_path))
        if isinstance(_path, list):
            return [_join_path(p) for p in _path]
        if current != git_root:
            _path = os.path.join(git_root, _path).split(current + "/")[1]
        return _path

    cmd = ["git", "--no-pager", "diff", "--cached", "--", target]
    _path = _join_path(path)
    if _path:
        cmd.extend([_path] if isinstance(_path, str) else _path)
    res, output = _run_command(cmd)
    if res != 0:
        logging.error("git command failed, cmd: {}".format(cmd))
        return None
    content = output.decode("utf-8").strip()
    if _is_subproject_changes(content) and isinstance(path, str):
        content = _get_subproject_changes(target, path)
    return content


def commit(message):
    """Commit the changes of the git repository.

    Args:
        message (str): The commit message.

    """
    _run_command(["git", "commit", "-m", message], lambda x: sys.stdout.write(x.decode("utf-8")))


if __name__ == "__main__":
    import sys

    logger.setLevel(logging.DEBUG)
    target = sys.argv[1]
    print(is_exist_git_repo())
    print(current_branch())
    files = get_change_files(target)
    print(files)
    print(get_file_diff(files[0], target))


def _is_subproject_changes(diff_content):
    """Check if the diff is subproject changes.

    Args:
        diff_content (str): The diff content.

    Returns:
        bool: True if the diff is subproject changes, False otherwise.
    """
    return bool(re.search(r"^-Subproject commit", diff_content, re.MULTILINE))


def _get_subproject_changes(target, subproject):
    """Get the subproject changes.

    Args:
        target (str): The target to compare with.
        subproject (str): The subproject name.

    Returns:
        list: The list of subproject changes.
    """
    logger.debug("Get subproject changes, target: {}, subproject: {}".format(target, subproject))
    cmd = ["git", "--no-pager", "diff", "--cached", target, "--submodule=diff", "--", subproject]
    res, output = _run_command(cmd)
    if res != 0:
        logging.error("git command failed, cmd: {}".format(cmd))
        return None
    return output.decode("utf-8").strip()
