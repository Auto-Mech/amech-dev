#!/usr/bin/env python
import os
import re
import shutil
import subprocess
import tarfile
import warnings
from collections.abc import Sequence
from pathlib import Path

import automech
import click
import yaml
from pydantic import BaseModel


class RepoInfo(BaseModel, extra="allow"):
    autochem: str | list[str]
    autoio: str | list[str]
    autofile: str | list[str]
    mechanalyzer: str | list[str]
    mechdriver: str | list[str]


SRC_DIR = Path("src").resolve()
EXAMPLE_ROOT_DIR = Path("src/mechdriver/examples").resolve()
TEST_ROOT_DIR = Path("src/mechdriver/tests").resolve()
TESTS = [t for t in yaml.safe_load((TEST_ROOT_DIR / "config.yaml").read_text())]
EXAMPLE_DIRS: list[Path] = [EXAMPLE_ROOT_DIR / t for t in TESTS]
TEST_DIRS: list[Path] = [TEST_ROOT_DIR / t for t in TESTS]

RUN_PROV_FILE = TEST_ROOT_DIR / "run_prov.yaml"
SIGN_PROV_FILE = TEST_ROOT_DIR / "sign_prov.yaml"
ARCHIVE_FILE = TEST_ROOT_DIR / "archive.tgz"


@click.group()
def main():
    """Testing CLI"""
    pass


@main.command("local")
@click.argument("nodes", nargs=-1)
def local(nodes: Sequence[str]):
    """Run local tests on one or more nodes.

    :param nodes: A comma-separted list of nodes
    """
    assert len(TESTS) == 1, "Not yet ready for more than one test."

    # 1. Record the current repository versions
    check_for_uncommited_python_changes(throw_error=True)
    run_prov = repos_current_version()
    print(f"\nWriting setup repo information to {RUN_PROV_FILE}")
    RUN_PROV_FILE.write_text(yaml.safe_dump(dict(run_prov)))

    # 2. Copy the example directories over
    for test_dir, example_dir in zip(TEST_DIRS, EXAMPLE_DIRS, strict=True):
        if test_dir.exists():
            print(f"Removing {test_dir}")
            shutil.rmtree(test_dir)

        print(f"Creating {test_dir} from {example_dir}")
        shutil.copytree(example_dir / "inp", test_dir / "inp", dirs_exist_ok=True)

    # 3. Set up subtasks
    automech.subtasks.setup_multiple(TEST_DIRS)

    # 4. Run subtasks
    automech.subtasks.run_multiple(
        TEST_DIRS, nodes=nodes, activation_hook=pixi_activation_hook()
    )


@main.command("status")
def status():
    """Check the status of electronic structure calculations."""
    for test in TESTS:
        test_dir = TEST_ROOT_DIR / test.name
        print(f"Checking status in {test_dir}...")
        os.chdir(test_dir)
        automech.subtasks.status()


@main.command("sign")
def sign():
    """Sign off on electronic structure calculations."""
    setup_repo_info = RepoInfo(**yaml.safe_load(RUN_PROV_FILE.read_text()))
    signed_repo_info = repos_version_diff(setup_repo_info)
    print(f"\nWriting signed repo information to {SIGN_PROV_FILE}")
    signed_dct = {"username": github_username(), **dict(signed_repo_info)}
    SIGN_PROV_FILE.write_text(yaml.safe_dump(signed_dct))


def repos_current_version() -> RepoInfo:
    """Get information about the current version of each repo

    :return: One-line summaries of most recent commits
    """
    check_for_uncommited_python_changes()
    version_dct = repos_output(["git", "log", "--oneline", "-n", "1"])
    return RepoInfo(**version_dct)


def repos_version_diff(repo_info: RepoInfo) -> RepoInfo:
    """Get information about differences in the current version of each repo, relative
    to a past version

    :param repo_info: The repository information to compare to
    :return: One-line summaries of each commit since the one given
    """
    check_for_uncommited_python_changes()
    command_dct = {
        k: [f"{commit_hash_from_line(v)}..HEAD"] for k, v in dict(repo_info).items()
    }
    diff_dct = repos_output(["git", "log", "--oneline"], command_dct=command_dct)
    diff_dct = {k: v.splitlines() for k, v in diff_dct.items()}
    return RepoInfo(**diff_dct)


class UncommittedChangesError(Exception):
    pass


START_YELLOW = "\033[93m"
END_COLOR = "\033[0m"
warnings.formatwarning = lambda m, c, *_: f"{START_YELLOW}{c.__name__}{END_COLOR}: {m}"


def check_for_uncommited_python_changes(throw_error: bool = False) -> None:
    """Assert that there are no uncommited Python changes in any repo.

    :param throw_error: Throw an error if there are uncommitted changes?
    """
    status_dct = repos_output(["git", "status", "-s", "*.py"])
    for repo, status in status_dct.items():
        if status:
            message = (
                f"{repo} has uncommitted Python changes:\n{status}\n"
                f"Make sure your repositories are clean before running tests!\n"
            )
            if throw_error:
                raise UncommittedChangesError(message)
            else:
                warnings.warn(message)


def commit_hash_from_line(line: str) -> str:
    """Get the commit hash from a one-line log summary

    :param line: A one-line log summary
    :return: The commit hash
    """
    return line.split()[0]


def repos_output(
    command: list[str], command_dct: dict[str, list[str]] | None = None
) -> dict[str, str]:
    """Get output from a command in each repo

    :param command: A command to run for each repo
    :param command_dct: Additional repo-specific commands, by repo name
    :return: One-line summaries of most recent commits
    """
    command_dct = {} if command_dct is None else command_dct
    output_dct = {}
    for repo in RepoInfo.model_fields:
        repo_dir = SRC_DIR / repo
        full_command = command + command_dct.get(repo, [])
        output_dct[repo] = subprocess.check_output(
            full_command, text=True, cwd=repo_dir
        ).strip()
    return output_dct


def github_username() -> str:
    """Return the current user's GitHub username as a string

    Requires the username to be configured:

        git config --global user.name

    :return: The username
    """
    return subprocess.check_output(
        ["git", "config", "--global", "user.name"], text=True
    ).strip()


def pixi_activation_hook() -> str:
    result = subprocess.run(["pixi", "shell-hook"], capture_output=True, text=True)
    return result.stdout


@main.command("archive")
def archive() -> None:
    """Tar a directory in its current location

    :param path: The path to a directory
    """
    exclude = ("subtasks/", "run/")

    os.chdir(TEST_ROOT_DIR)
    print(f"Creating {ARCHIVE_FILE}...")
    ARCHIVE_FILE.unlink(missing_ok=True)
    with tarfile.open(ARCHIVE_FILE, "w:gz") as tar:
        if RUN_PROV_FILE.exists():
            tar.add(RUN_PROV_FILE, arcname=RUN_PROV_FILE.name)
        if SIGN_PROV_FILE.exists():
            tar.add(SIGN_PROV_FILE, arcname=SIGN_PROV_FILE.name)
        for test in TESTS:
            tar.add(
                test,
                arcname=test,
                filter=lambda x: None if any(e in x.name for e in exclude) else x,
            )


@main.command("unpack")
def unpack_archive() -> None:
    """Un-tar a directory in its current location

    :param path: The path where the AutoMech subtasks were set up
    """
    os.chdir(TEST_ROOT_DIR)
    if ARCHIVE_FILE.exists():
        print(f"Unpacking {ARCHIVE_FILE}...")
        with tarfile.open(ARCHIVE_FILE, "r") as tar:
            tar.extractall()


if __name__ == "__main__":
    main()
