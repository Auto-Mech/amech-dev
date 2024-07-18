# AutoMech Developer Set-up

This repository provides instructions for installing and running AutoMech from source,
as a developer.

If you are a brand new AutoMech developer, start by following the instructions in
[Appendix A](#appendix-a-new-automech-developers-start-here) to fork the AutoMech
repositories.

## Install

The following steps only need to be done once per machine.

1. If you haven't already, fork this `amech-dev` repository on GitHub.
Then clone your forked repository wherever you want your AutoMech source code to live
and `cd` into it before continuing.
```
git clone git@github.com:<username>/amech-dev.git
cd amech-dev/
```

2. If you haven't already, follow the instructions in
[Appendix B](#appendix-b-install-pixi-for-package-management) to install Pixi.  This
will be your package manager for AutoMech development.
Then run the following command to create the Pixi environment for this project.
```
pixi install
```

3. If you haven't already, follow the instructions in
[Appendix C](#appendix-c-connect-to-github-via-ssh) to set up SSH authentication with
your GitHub account.
Then run the following Pixi task to download the repositories for each of the five
AutoMech modules into `src/` and check out their `dev` branches.
(The bash script for this task is in `scripts/` and can be modified as needed.)
```
pixi run download
```

4. Run the following Pixi task install each of the main AutoMech modules into your Pixi
environment in edit mode.
```
pixi run install
```

5. Check that the installation worked by running the following help command.
You should see some documentation for the AutoMech CLI.
```
pixi shell  # activate the environment
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
pixi run update
```

*Script 2: Check for changes.*
Run the following script to see which repositories you have changed.[^2]
```
pixi run status
```

*Development workflow.*
Other commands, such as `git add` and `git commit`, should be run manually inside the
individual repositories.
The recommended development workflow is as follows:

1. `pixi run update` - update early and often
2. Make changes to the code...
3. Run the code to test your changes...
4. `pixi run status` - see where you made changes
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


## Distribute

You can build the AutoMech conda package as follows:
```
pixi run build
```
If one of the C/C++/Fortran codes in `src/automech-toolbox` needs to be updated, you
would first run the following:
```
pixi run -e build build-toolbox
```
For the AutoMech-Toolbox codes, note that the MESS executables are not compiled from
source.
Instead, they are downloaded from
[the MESS GitHub page](https://github.com/Auto-Mech/MESS/tree/master/static)
and will need to be updated there if MESS has changed.

At the end, the build script will print the appropriate command for you to upload the
package to Anaconda.org, which should look something like the following.
Note that you will need to set the `ANACONDA_API_KEY` environment variable with your API
key from Anaconda.org.
```
export ANACONDA_API_KEY=<API token>
rattler-build upload anaconda -o Auto-Mech output/noarch/*.conda
```


## Appendix A: New AutoMech Developers Start Here

To get started as a new developer, log into GitHub (or create an account) and follow
[these instructions](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#forking-a-repository)
to fork the following five repositories:
 - [AutoChem](https://github.com/Auto-Mech/autochem)
 - [AutoIO](https://github.com/Auto-Mech/autoio)
 - [AutoFile](https://github.com/Auto-Mech/autofile)
 - [MechAnalyzer](https://github.com/Auto-Mech/mechanalyzer)
 - [MechDriver](https://github.com/Auto-Mech/mechdriver)


## Appendix B: Install Pixi for Package Management

This repository is set up to use Pixi for package management.
You can install Pixi by running the following command:
```
curl -fsSL https://pixi.sh/install.sh | bash
```
This script will update your `~/.bash_profile` and you may need to restart your shell
for the changes to take effect.

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


## Appendix C: Connect to GitHub via SSH

To communicate with your forked GitHub repositories, you will need to generate an SSH
key for your machine and add it to your GitHub account.
This will allow you to push to your GitHub forks without a password.
Follow these two steps to get set up:

1. Follow
[these instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key)
to generate a new SSH key, if you haven't already. (You can ignore the other
instructions on the linked page.)
2. Follow
[these instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account#adding-a-new-ssh-key-to-your-account)
to add the new key to your GitHub account.


<!-- Footnotes: -->

[^1]: If syncing your own fork between different machines, you can specify the remote and
branch to update against, i.e. `./update.sh origin dev` (the default is `upstream dev`).
You can also add the `--force` flag to overwrite the history on your GitHub fork when it
gets out of sync, i.e.  `./update.sh upstream dev --force`.

[^2]: This script simply runs `git status` in each repository.
If you want to run a different command, you can pass it as an argument, i.e. `./status.sh git branch -v` to see which branches are checked out.