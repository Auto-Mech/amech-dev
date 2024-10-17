#!/usr/bin/env python
import os
import shutil
import subprocess
from pathlib import Path

import automech
import click
import yaml
from pydantic import BaseModel


class TestConfig(BaseModel):
    name: str


TEST_DIR = Path("tests").resolve()
EXAMPLE_DIR = Path("examples").resolve()
TESTS = [
    TestConfig(**c) for c in yaml.safe_load((TEST_DIR / "config.yaml").read_text())
]


@click.group()
def main():
    """Testing CLI"""
    pass


@main.command("setup")
def setup():
    """Set up the tests to run."""
    for test in TESTS:
        # Remove the test directory, if it exists
        test_dir = TEST_DIR / test.name
        if test_dir.exists():
            print(f"Removing {test_dir}")
            shutil.rmtree(test_dir)

        # Create a clean test directory
        example_inp_dir = EXAMPLE_DIR / test.name / "inp"
        test_inp_dir = test_dir / "inp"
        print(f"Creating {test_inp_dir} from {example_inp_dir}")
        shutil.copytree(example_inp_dir, test_inp_dir, dirs_exist_ok=True)

        # Create the subtasks
        print(f"Setting up subtasks in {test_dir}")
        os.chdir(test_dir)
        automech.subtasks.setup(".", task_groups=("els",))


@main.command("els")
@click.argument("nodes")
def els(nodes: str):
    """Run electronic structure calculations.

    :param nodes: A comma-separted list of nodes
    """
    for test in TESTS:
        test_dir = TEST_DIR / test.name
        subprocess.run(["pixi", "run", "subtasks", "-t", nodes], cwd=test_dir)


@main.command("status")
def status():
    """Check the status of electronic structure calculations."""
    for test in TESTS:
        test_dir = TEST_DIR / test.name
        print(f"Checking status in {test_dir}...")
        os.chdir(test_dir)
        automech.subtasks.status()


if __name__ == "__main__":
    main()
