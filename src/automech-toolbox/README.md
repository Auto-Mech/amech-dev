# AutoMech-Toolbox

This repository contains source code and build scripts for static executables used by
AutoMech.
It also contains a recipe for a conda package that places these executables in a
user's bin.
You will need `CMake` and `rattler-build` installed to build and upload the conda
package.
The following instructions will guide you through the process.

## Build

The following script will compile the code and build the conda package for it.
```
./build.sh
```

At the end, the build script will print the appropriate command for you to upload the
package to Anaconda.org, which should look something like the following.
Note that you will need to set the `ANACONDA_API_KEY` environment variable with your API
key from Anaconda.org.
```
export ANACONDA_API_KEY=<API token>
rattler-build upload anaconda -o Auto-Mech output/noarch/*.conda
```

## Test

To test that build worked, you can create an environment from your local copy of the conda package as follows.
```
conda create -n test /path/to/file.conda
```
Alternatively, you can test that the upload worked by getting the conda package
from Anaconda.org as follows.
```
conda create -n test -c auto-mech <package name>
```
You can test that it worked as follows.
```
conda activate test  # Or . /path/to/conda/bin/activate test
which <executable name>  # The executables should appear in your environment bin
# Then, run the executables to test that they work
```

On subsequent tests, use the following commands to remove the environment and
clear the cache before creating the test environment.
Clearing the cache is important.
If the version number hasn't changed and you don't clear the cache, conda will
use its own archived copy of your package instead of the newly created one.
```
conda env remove -n test
conda clean --all  # Remove the cached version of test-mess
```
