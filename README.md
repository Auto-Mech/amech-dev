# amech-dev

This repository provides instructions for installing and running AutoMech from source,
as a developer.

If you are a brand new AutoMech developer, start by following the instructions at the
very bottom to fork the AutoMech repositories.

## Installing AutoMech with Pixi

The following instructions only need to be done once per machine.

### Install Pixi

If you haven't already, install Pixi with the following command.
```
curl -fsSL https://pixi.sh/install.sh | bash
```

### Install AutoMech in developer mode

1. Clone this `amech-dev` repository wherever you want your AutoMech source code to
live.
Unless you are a core developer, you can clone via HTTP from the main Auto-Mech repo.
(Core developers should fork and clone via SSH, so that they can make changes to this repo as needed.)
```
git clone https://github.com/Auto-Mech/amech-dev.git
```

2. Run Pixi's install command inside the top-level directory for this repository.
```
cd amech-dev/
pixi install
```

3. Run the download script to download the repositories and check out their `dev` branches. These will be placed in `src/`.
```
./download.sh
```

4. Run the install script to install each of the main AutoMech modules into your pixi
environment in edit mode.
```
./install.sh
```

## Running AutoMech and Making Changes

```
pixi shell
```

## First Steps for New Developers

### Fork repositories and add dev branches

Log into GitHub and fork the following five repositories:

 - [AutoMech](https://github.com/Auto-Mech/autochem)
 - [AutoIO](https://github.com/Auto-Mech/autoio)
 - [AutoFile](https://github.com/Auto-Mech/autofile)
 - [MechAnalyzer](https://github.com/Auto-Mech/mechanalyzer)
 - [MechDriver](https://github.com/Auto-Mech/mechdriver)

Then, for each fork, add the `dev` branch of the Auto-Mech repository as follows:

1. On the GitHub page for your fork, add `/branches` to the URL.
2. Click the green button in the upper right that says "New branch".
3. Set `dev` as the branch name and choose the `dev` branch from the main `Auto-Mech` repository as its source.