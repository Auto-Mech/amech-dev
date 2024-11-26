#!/usr/bin/env python
import os
import shutil
import socket
import subprocess
import tarfile
import textwrap
import warnings
from collections.abc import Sequence
from pathlib import Path

import automech
import click
import yaml
from pydantic import BaseModel


class Provenance(BaseModel):
    autochem: str
    autoio: str
    autofile: str
    mechanalyzer: str
    mechdriver: str


class Signature(BaseModel):
    provenance: Provenance
    overrides: dict[str, list[str]]
    username: str


COMMIT_MESSAGE = "Updates tests/archive.tgz"

os.chdir(os.environ.get("INIT_CWD"))

ROOT_DIR = Path(os.environ.get("PIXI_PROJECT_ROOT")).resolve()
SRC_DIR = ROOT_DIR / "src"
MECHDRIVER_DIR = SRC_DIR / "mechdriver"
EXAMPLE_ROOT_DIR = MECHDRIVER_DIR / "examples"
TEST_ROOT_DIR = MECHDRIVER_DIR / "tests"
TESTS = [t for t in yaml.safe_load((TEST_ROOT_DIR / "config.yaml").read_text())]
EXAMPLE_DIRS: list[Path] = [EXAMPLE_ROOT_DIR / t for t in TESTS]
TEST_DIRS: list[Path] = [TEST_ROOT_DIR / t for t in TESTS]

PROVENANCE_FILE = TEST_ROOT_DIR / "provenance.yaml"
SIGNATURE_FILE = TEST_ROOT_DIR / "signature.yaml"
ARCHIVE_FILE = TEST_ROOT_DIR / "archive.tgz"


@click.group()
def main():
    """Testing CLI"""
    pass


@main.command("status")
def status():
    """Check the status of local tests."""
    for test in TESTS:
        test_dir = TEST_ROOT_DIR / test
        print(f"Checking status in {test_dir}...")
        automech.subtasks.status(test_dir, check_file=f"check_{test}.log")


@main.command("local")
@click.argument("nodes", nargs=-1)
def local(nodes: Sequence[str]):
    """Run local tests on one or more nodes.

    :param nodes: A comma-separted list of nodes
    """
    print("Process ID:", os.getpid())
    print("Host name:", socket.gethostname())

    # 1. Record the current repository versions
    check_for_uncommited_python_changes(throw_error=True)
    prov = repos_current_version()
    print(f"\nWriting setup repo information to {PROVENANCE_FILE}")
    PROVENANCE_FILE.write_text(yaml.safe_dump(prov.model_dump()))

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

    # 5. Archive the results
    archive()


@main.command("sign")
def sign():
    """Sign off on local tests."""
    check_for_uncommited_python_changes()

    # Unpack archive
    unpack_archive()

    # Compare to tested version and prompt for override as needed
    prov0 = Provenance(**yaml.safe_load(PROVENANCE_FILE.read_text()))
    diff_dct = repos_version_diff(prov0)
    overrides = {}
    print("This assumes that you first ran local tests using `pixi run test local`")
    print("Checking that the tests were run against the current repository versions...")
    for repo, diffs in diff_dct.items():
        print(
            f"WARNING: {repo} does not match the tested version!! "
            f"It has {len(diffs)} additional commits:"
        )
        print(textwrap.indent("\n".join(diffs), "    "))
        answer = input(
            "Do you solemnly swear that these changes will not affect the tests? (yes/no): "
        )
        print()
        if answer == "yes":
            overrides[repo] = diffs
        else:
            print("Thank you for your honesty.")
            print("Please re-run the tests using `pixi run test local`.")
            return

    # Sign
    signature = Signature(
        provenance=repos_current_version(),
        overrides=overrides,
        username=github_username(),
    )
    print(f"\nWriting signed repo information to {SIGNATURE_FILE}")
    SIGNATURE_FILE.write_text(yaml.safe_dump(signature.model_dump()))

    # Archive
    archive()

    # Commit the archive
    subprocess.run(["git", "restore", "--staged", "."], cwd=MECHDRIVER_DIR)
    subprocess.run(["git", "add", str(ARCHIVE_FILE)], cwd=MECHDRIVER_DIR)
    subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], cwd=MECHDRIVER_DIR)


def archive() -> None:
    """Tar a directory in its current location

    :param path: The path to a directory
    """
    exclude = ("subtasks", "run")

    def _filter(obj: tarfile.TarInfo) -> tarfile.TarInfo | None:
        """Filter function for excluding unneeded directories."""
        name = obj.name
        if any(f"{e}/" in name or name.endswith(e) for e in exclude):
            return None
        return obj

    os.chdir(TEST_ROOT_DIR)
    print(f"Creating {ARCHIVE_FILE}...")
    ARCHIVE_FILE.unlink(missing_ok=True)
    with tarfile.open(ARCHIVE_FILE, "w:gz") as tar:
        if PROVENANCE_FILE.exists():
            tar.add(PROVENANCE_FILE, arcname=PROVENANCE_FILE.name)
        if SIGNATURE_FILE.exists():
            tar.add(SIGNATURE_FILE, arcname=SIGNATURE_FILE.name)
        for test in TESTS:
            tar.add(test, arcname=test, filter=_filter)


def unpack_archive() -> None:
    """Un-tar a directory in its current location

    :param path: The path where the AutoMech subtasks were set up
    """
    os.chdir(TEST_ROOT_DIR)
    if ARCHIVE_FILE.exists():
        print(f"Unpacking {ARCHIVE_FILE}...")
        with tarfile.open(ARCHIVE_FILE, "r") as tar:
            tar.extractall()


def repos_current_version() -> Provenance:
    """Get information about the current version of each repo

    :return: One-line summaries of most recent commits
    """
    version_dct = repos_output(["git", "log", "--oneline", "-n", "1"])
    return Provenance(**version_dct)


def repos_version_diff(repo_info: Provenance) -> dict:
    """Get information about differences in the current version of each repo, relative
    to a past version

    :param repo_info: The repository information to compare to
    :return: One-line summaries of each commit since the one given
    """
    command_dct = {
        k: [f"{commit_hash_from_line(v)}..HEAD"] for k, v in dict(repo_info).items()
    }
    diff_dct = repos_output(["git", "log", "--oneline"], command_dct=command_dct)
    diff_dct = {k: v.splitlines() for k, v in diff_dct.items() if v}
    return diff_dct


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
            message = f"{repo} has uncommitted Python changes:\n{status}\n"
            if throw_error:
                message += "Please commit changes before running tests!\n"
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
    for repo in Provenance.model_fields:
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
    return subprocess.check_output(["pixi", "shell-hook"], text=True)


if __name__ == "__main__":
    main()
