#!/usr/bin/env python
import os
import socket
import subprocess
from collections.abc import Sequence
from pathlib import Path

import automech
import click
from automech import test_utils

os.chdir(os.environ.get("INIT_CWD"))

ROOT_DIR = Path(os.environ.get("PIXI_PROJECT_ROOT")).resolve()
TEST_UTILS = test_utils.TestUtils(ROOT_DIR / "src" / "mechdriver")


@click.group()
def main():
    """Testing CLI"""
    pass


@main.command("status")
def status():
    """Check the status of local tests."""
    for test_dir in TEST_UTILS.test_dirs:
        print(f"Checking status in {test_dir}...")
        automech.subtasks.status(test_dir, check_file=f"check_{test_dir.name}.log")


@main.command("local")
@click.argument("nodes", nargs=-1)
def local(nodes: Sequence[str]):
    """Run local tests on one or more nodes.

    :param nodes: A comma-separted list of nodes
    """
    print("Process ID:", os.getpid())
    print("Host name:", socket.gethostname())

    TEST_UTILS.setup_tests()
    automech.subtasks.setup_multiple(TEST_UTILS.test_dirs)
    automech.subtasks.run_multiple(
        TEST_UTILS.test_dirs, nodes=nodes, activation_hook=pixi_activation_hook()
    )
    TEST_UTILS.archive_tests()


@main.command("sign")
def sign():
    """Sign off on local tests."""
    TEST_UTILS.check_for_uncommited_python_changes()
    TEST_UTILS.extract_archived_tests()
    TEST_UTILS.sign_tests()
    TEST_UTILS.archive_tests()
    TEST_UTILS.commit_test_archive()


def pixi_activation_hook() -> str:
    return subprocess.check_output(["pixi", "shell-hook"], text=True)


if __name__ == "__main__":
    main()
