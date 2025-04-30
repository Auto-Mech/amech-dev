#!/usr/bin/env python
import os
import socket
import subprocess
from collections.abc import Sequence
from pathlib import Path

import click

import mechdriver
from mechdriver import test_utils

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
    mechdriver.subtasks.status_multiple(TEST_UTILS.test_dirs)


@main.command("local", hidden=True)
@click.argument("nodes", nargs=-1)
def local(nodes: Sequence[str]):
    """Run local tests on one or more nodes.

    Runs hidden local_

    :param nodes: A list of nodes
    """
    log_name = "test.log"
    test_cmd = " ".join(["pixi run test local_", *nodes])
    cmd = ["pixi", "run", "node", nodes[-1], log_name, test_cmd]
    print(subprocess.check_output(cmd, text=True))


@main.command("sign")
def sign():
    """Sign off on local tests."""
    sign_()


def pixi_activation_hook() -> str:
    return subprocess.check_output(["pixi", "shell-hook"], text=True)


# Hidden command
@main.command("local_", hidden=True)
@click.argument("nodes", nargs=-1)
def local_(nodes: Sequence[str]):
    """Run local tests on one or more nodes.

    :param nodes: A list of nodes
    """
    print("Process ID:", os.getpid())
    print("Host name:", socket.gethostname())

    TEST_UTILS.setup_tests()
    mechdriver.subtasks.setup_multiple(TEST_UTILS.test_dirs)
    mechdriver.subtasks.run_multiple(
        TEST_UTILS.test_dirs, nodes=nodes, activation_hook=pixi_activation_hook()
    )
    TEST_UTILS.archive_tests()
    sign_()


def sign_():
    """Sign off on local tests."""
    TEST_UTILS.check_for_uncommited_python_changes()
    TEST_UTILS.extract_archived_tests()
    TEST_UTILS.sign_tests()
    TEST_UTILS.archive_tests()
    TEST_UTILS.commit_test_archive()


if __name__ == "__main__":
    main()
