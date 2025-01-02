# AutoMech Developer Set-up

This repository provides instructions for installing and running AutoMech from source,
as a developer.

If you are a brand new AutoMech developer, start by following the instructions in
[Appendix A](#appendix-a-new-automech-developers-start-here) to fork the AutoMech
repositories.

## Install

The following steps only need to be done once per machine.

1. Clone this `amech-dev` repository wherever you want your AutoMech source code to live
and `cd` into it before continuing.[^1]
```
git clone https://github.com/Auto-Mech/amech-dev.git
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
cd src/mechdriver/examples/quick/
automech run &> out.log &
```
Running `automech run --help` will allow you to see the options for this command.

If you want to activate this Pixi environment from within a shell script, the best way to do that is with the following command:
```
eval "$(pixi shell-hook --manifest-path /path/to/amech-dev/pixi.toml)"
```
You will need to edit the path to point to wherever you cloned this repository.

To see available MechAnalyzer commands for things like stereoexpansion and sorting, run `mechanalyzer --help`.

### Run on a node

To run AutoMech (or another command) on a node to which you have SSH access, you can use the following Pixi task:
```
pixi run node <node> <log file> <command>
```
If unspecified, the default command is "automech run" and the default log file is "out.log".

Examples:
```
pixi run node csed-0001  			   	# run AutoMech
pixi run node csed-0001 out.log "g16 run.inp run.out"  	# run Gaussian
```

## Test

Testing MechDriver is a two-step process. First, electronic structure calculations are
run in parallel on a local cluster (requires SSH node access; currently not interfaced
to a workload manager). Then, an end-to-end workflow is run with the filesystem database
from step 1. This second step is what runs on GitHub Actions every time the code is
updated.

### Local Testing

Before running tests, make sure you have merged any changes to the lower-level modules
into their central Auto-Mech GitHub repositories.
Without this, your GitHub Actions workflow will raise an error because the tested
version does not match the current one on GitHub.
If your lower-level modules contain work-in-progress, move it to a feature branch and switch back to `dev` before running tests.

The first time you run tests on a new machine, you will also need to run the following
command to save your GitHub username as a Git configuration variable.
```
git config --global user.name                   # check the current value
git config --global user.name "<username>"      # update the value
```
This configuration variable is used by the `signature.yaml` file described below.

#### Run local tests

Use the following command to run the test cases locally.[^4]
```
pixi run test local <node1> <node2> <...>
```
The nodes can be individually named or expanded as a Bash sequence, e.g.
`csed-00{09..12}`.  The species/reaction-specific subtasks are parallelized across the
given nodes for each task.  Unfortunately, this means that all jobs for a given task
must complete before the workflow can move on to the next one.

At the end of the run, the data from the local test run will be zipped into `.tgz`
archive and added in a separate git commit for use in GitHub Actions workflow testing
(see below).
This archive includes a `provenance.yaml` file recording the current commit hash of each
repository and a `signature.yaml` file which, in this case, records the same
information.
To make sure the recorded provenance is accurate, you will be prevented from running tests if you
have uncommitted changes in any Python files.
The commit hashes in the `siganture.yaml` file are used by the GitHub Actions workflow to check that the tests are up-to-date.
If these do not match the respective GitHub repos, the "signature" test on GitHub
Actions will fail.


#### Check progress

You can check the progress of a local test with the following command.
```
pixi run test status
```
This will display a table showing the status of your jobs and generate a set of
`check_<test name>.log` files, containing the paths to any jobs that have something
other than an `OK` status (including running jobs), along with the last line of the log
file for these jobs.
These files are designed to be easily grep-able:
```
grep "~conf_energy" check_quick.log       # See paths
grep "~conf_energy" -A 1 check_quick.log  # See paths and last lines
```

#### Update `signature.yaml` without re-running local tests

If you only made a small change, or made changes that you are confident will not affect
the tested functionality, you can override the signature test by locally running the
following command before merging:
```
pixi run test sign
```
You will be prompted to approve the changes made to each repo since the tests were last run.
These "overrides" will be recorded in the `signature.yaml` and the signature test will
now pass.


### Remote Testing

GitHub Actions will use the following `pytest` commands to check the `signature.yaml`
file and to run the test cases using the archived electronic structure data.[^5]
```
pytest -v src/mechdriver/tests/ -k "signature"              # check the signature
pytest -n auto -v src/mechdriver/tests/ -k "not signature"  # run test cases
```
You can run these locally as well.

### Adding Tests

Adding a new test is a two-step process:

1. Add a folder containing the MechDriver input for your test to `src/mechdriver/examples`
2. Add the name of this folder to the list in `src/mechdriver/tests/config.yaml`.

The next time you run tests, your new example will now be included.

## Contribute

If you followed the instructions above, you are running AutoMech directly from the
source code in `src/` and can make changes to it as needed.
This repository provides two helper scripts for interacting with these repositories all at once...

*Script 1: Update.*
Run the following script early (i.e. *before* you make changes) and often to stay in
sync with other developers and avoid merge conflicts.[^2]
```
pixi run update
```

*Script 2: Check for changes.*
Run the following script to see which repositories you have changed.[^3]
```
pixi run git status
```

*Development workflow.*
Other commands, such as `git add` and `git commit`, should be run manually inside the
individual repositories.
The recommended development workflow is as follows:

1. `pixi run update` - update early and often
2. Make changes to the code...
3. Run the code to test your changes...
4. `pixi run git status` - see where you made changes
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

[^1]: If changes are made to the `amech-dev` repository, you can update using
`git pull origin main`.
Developers who may want to contribute to this repository should follow the usual
procedure to fork and clone, adding the central `Auto-Mech` repo as the `upstream`
remote.
In this case, you will update your `amech-dev` repository using
`git pull --rebase upstream main && git push --force origin main`.

[^2]: If syncing your own fork between different machines, you can specify the remote and
branch to update against, i.e. `pixi run update origin dev` (the default is `upstream dev`).
You can also add the `--force` flag to overwrite the history on your GitHub fork when it
gets out of sync, i.e.  `pixi run update upstream dev --force`.

[^3]: This script simply runs `git status` in each repository.
If you want to run a different command, you can pass it as an argument, i.e. `pixi run git branch -v` to see which branches are checked out.

[^4]: The first time you do this, you may also need to make sure that your environment
is fully up-to-date:
`git pull https://github.com/Auto-Mech/amech-dev && pixi run update`.

[^5]: The `-n auto` option runs these tests in parallel.
