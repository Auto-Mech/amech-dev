# amech-dev

This repository provides instructions for installing and running AutoMech from source,
as a developer.

If you are a brand new AutoMech developer, start by following the instructions in
Appendix A to fork the AutoMech repositories.

## Install

The following steps only need to be done once per machine.

1. If you don't have Pixi or Mamba installed, follow the instructions in Appendix B
below to install one of these as your package manager.

2. Clone this `amech-dev` repository wherever you want your AutoMech source code to
live and `cd` into it before continuing.
Unless you are a core developer, you can clone via HTTP from the main Auto-Mech repo.
(Core developers may wish to fork and clone via SSH so that they can make changes to
this repo.)
```
git clone https://github.com/Auto-Mech/amech-dev.git
cd amech-dev/
```

3. Run the following script to clone the repositories for each of the five AutoMech
modules into `src/` and check out their `dev` branches.
```
./download.sh
```

4. Activate the `amech-dev` environment as described in Appendix B and run the install
script to install each of the main AutoMech modules into it in edit mode.
```
# activate your Pixi or Mamba environment, then run:
./install.sh
```

## Run

Every time you start a new shell, you will need to activate your Pixi or Mamba
environment as described in Appendix B.
```
pixi shell  # if using Pixi (in this directory)
ca amech-dev  # if using Mamba
```
[Link to documentation for learning how to run here]

## Contribute

If you followed the instructions above, you can directly edit your locally installed
version of AutoMech by making changes to the repositories in `src/`.
This repository provides two helper scripts for interacting with these repositories all at once...

*Script 1: Update.*
Run the following script early (i.e. *before* you make changes) and often to stay in
sync with other developers and avoid merge conflicts.
```
./update.sh
```
If syncing your own fork between different machines, you can specify the remote and
branch to update against, i.e. `./update.sh origin dev` (the default is `upstream dev`).
You can also add the `--force` flag to overwrite the history on your GitHub fork when it
gets out of sync, i.e.  `./update.sh upstream dev --force`.

*Script 2: Check for changes.*
Run the following script to see which repositories you have changed.
```
./status.sh
```
This script simply runs `git status` in each repository.
If you want to run a different command, you can pass it as an argument, i.e. `./status.sh git branch -v` to see which branches are checked out.

*Development workflow.*
Other commands, such as `git add` and `git commit`, should be run manually inside the
individual repositories.
The recommended development workflow is as follows:

1. `./update.sh` - Do this early and often
2. Make changes to the code...
3. Run the code to test your changes (ideally, run tests where we have them) ...
4. `./status.sh` - Check where you made changes
5. `cd src/<repository directory>` - Enter a repository with changes (do this for each one)
6. `git add --patch` - Answer the prompts to decide which changes you want to keep
7. `git checkout .` - Discard the remaining changes (e.g. debug print statements)
8. `git commit` - Don't use `-m`! Instead, use a text editor to write an informative
description of your commit. You can configure the text editor as follows: `git config
--global core.editor "vim"`
9. `git pull --rebase upstream dev` - Double-check again that you are up to date with the
central repository.
10. `git push origin dev` - You may need to add `--force` if the rebase pulled in changes from before your commit.
11. On GitHub, submit a pull request with your changes.

As always, small, frequent commits are preferable to large, infrequent ones.


## Appendix A: New AutoMech Developers Start Here

To get started as a new developer, follow these instructions to fork each repository and get its dev branch.

*Step 1: Fork the repositories.*
Log into GitHub and fork the following five repositories:

 - [AutoMech](https://github.com/Auto-Mech/autochem)
 - [AutoIO](https://github.com/Auto-Mech/autoio)
 - [AutoFile](https://github.com/Auto-Mech/autofile)
 - [MechAnalyzer](https://github.com/Auto-Mech/mechanalyzer)
 - [MechDriver](https://github.com/Auto-Mech/mechdriver)

*Step 2: Add the `dev` branches to your forked repositories.*

1. On the GitHub page for your fork, add `/branches` to the URL.
2. Click the green button in the upper right that says "New branch".
3. Set `dev` as the branch name and choose the `dev` branch from the main `Auto-Mech` repository as its source.


## Appendix B: Install a Package Manager

You may use either [Pixi](https://pixi.sh/latest/) or
[Mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) as
your package manager.
See [here](https://prefix.dev/blog/pixi_a_fast_conda_alternative) for a comparison of
the two.

Steps 1 and 2 below only need to be done once per machine, whereas Step 3, activating
the environment, needs to be done every time you start a new shell.

#### Option 1: Pixi

*Step 1: Install the package manager.*
Install Pixi with the following command.
```
curl -fsSL https://pixi.sh/install.sh | bash
```

*Step 2: Create the environment.*
Enter this directory and run the following command.
```
pixi install
```

*Step 3: Activate the environment.*
Enter this directory and run the following command.
```
pixi shell
```

#### Option 2: Mamba

*Step 1: Install the package manager.*
Install Mamba with the following command.
When prompted, set the install prefix to a directory with plenty of space, since this is where all of your environments will be stored.
Also, if you have the `TMPDIR` environment variable set (check with `echo $TMPDIR`),
make sure this directory exists by running `mkdir -p $TMPDIR` beforehand.
```
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

*Step 2: Create the environment.*
Enter this directory and run the following command.
```
mamba env create -f mamba.yml
```

*Step 3: Activate the environment.*
Add the following line to your `~/.bashrc` for activating environments.
```
alias caa='. <path to conda installation>/bin/activate amech-dev'
```
Then either restart your session or run `source ~/.bashrc`.
You will now be able to activate the environment using the alias `caa`.
