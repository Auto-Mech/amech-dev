# AutoMech Developer Set-up

This repository provides instructions for installing and running AutoMech from source,
as a developer.

If you are a brand new AutoMech developer, start by following the instructions in
Appendix A to fork the AutoMech repositories.

## Install

The following steps only need to be done once per machine.

1. If you haven't already, fork this `amech-dev` repository on GitHub.
Then clone your forked repository wherever you want your AutoMech source code to live
and `cd` into it before continuing.
```
git clone git@github.com:<username>/amech-dev.git
cd amech-dev/
```

2. Run the following script to clone the repositories for each of the five AutoMech
modules into `src/` and check out their `dev` branches.
```
./download.sh
```

3. If you haven't already, follow the instructions in Appendix B to install
[Pixi](https://pixi.sh/latest/).
This will be your package manager for AutoMech development.
Then run the following command to create the Pixi environment for this project.
```
pixi install
```

4. Activate the Pixi project environment and run the install script to install each of
the main AutoMech modules into it in edit mode.
```
pixi shell  # activate the Pixi environment first!
./install.sh
```

5. Check that the installation worked by running the following help command.
You should see some documentation for the AutoMech CLI.
```
automech --help
```

6. Set the following environment variable in your `~/.bashrc` file to turn off Python
output buffering.
```
export PYTHONUNBUFFERED=1
```

## Run

To test that the code is operational, you can run the "simple" example provided in the
MechDriver repository as follows.
```
pixi shell  # activate the environment
cd src/mechdriver/examples/simple/
automech run &> out.log &
```
Running `automech run --help` will allow you to see the options for this command.

To run from a different directory, you can do the following:
```
pixi run --manifest-path /path/to/amech-dev/pixi.toml automech run -p /path/to/job &> out.log &
```

To see available MechAnalyzer commands for things like stereoexpansion and sorting, run `mechanalyzer --help`.


## Contribute

If you followed the instructions above, you are running AutoMech directly from the
source code in `src/` and can make changes to it as needed.
This repository provides two helper scripts for interacting with these repositories all at once...

*Script 1: Update.*
Run the following script early (i.e. *before* you make changes) and often to stay in
sync with other developers and avoid merge conflicts.[^1]
```
./update.sh
```

*Script 2: Check for changes.*
Run the following script to see which repositories you have changed.[^2]
```
./status.sh
```

*Development workflow.*
Other commands, such as `git add` and `git commit`, should be run manually inside the
individual repositories.
The recommended development workflow is as follows:

1. `./update.sh` - update early and often
2. Make changes to the code...
3. Run the code to test your changes...
4. `./status.sh` - see where you made changes
5. `cd src/<repository directory>` - enter a repository with changes (do this for each one)
6. `git add --patch` - answer the prompts to decide which changes to keep
7. `git checkout .` - discard the remaining changes
8. `git commit` - write a meaningful commit message with your choice of
text editor, which can be configured as follows: `git config --global core.editor "vim"` (don't use `-m`!)
9. `git pull --rebase upstream dev` - make sure you are up to date with the central
repository
10. `git push origin dev` - you may need to add `--force` if the rebase pulled in changes
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


## Appendix B: Install Pixi for Package Management

This repository is set up to use Pixi for package management.
You can install Pixi by running the following command:
```
curl -fsSL https://pixi.sh/install.sh | bash
```
The main Pixi commands to be aware of are as follows.
- `pixi install`:
Creates (or updates) an environment in a project directory using a `pixi.toml` file.
- `pixi shell`:
Activates a project environment.
- `pixi add <package name>`:
Adds a package to a project environment.

*Note*:
Adding packages to an environment will automatically update your `pixi.toml` and
`pixi.lock` files with the new dependencies.
If other users will need these in order to run the code, be sure to submit a pull
request with these changes to the main amech-dev repository.
Other developers will then be able to run `pixi install` again to update their environments.

See [here](https://pixi.sh/latest/) for further Pixi documentation.


<!-- Footnotes: -->

[^1]: If syncing your own fork between different machines, you can specify the remote and
branch to update against, i.e. `./update.sh origin dev` (the default is `upstream dev`).
You can also add the `--force` flag to overwrite the history on your GitHub fork when it
gets out of sync, i.e.  `./update.sh upstream dev --force`.

[^2]: This script simply runs `git status` in each repository.
If you want to run a different command, you can pass it as an argument, i.e. `./status.sh git branch -v` to see which branches are checked out.