# project-alpha

Visit our blog at:

http://townhallpinball.org

Town Hall Pinball is working on a customized pinball machine. The overall plan
is to:

* Use an existing pinball machine, "No Fear"
* Completely rebrand it with a new play-field, backglass, and cabinet artwork
* Design a new theme
* Design a new ruleset
* Design and/or use new animations, sound effects, and music
* Design new software

We are using the [P-ROC](http://www.pinballcontrollers.com/index.php/products/p-roc)
to interface with the pinball machine. A general library, called
[pinlib](https://github.com/town-hall-pinball/pinlib), is being developed
by us that extends off the work done on
[pyprocgame](https://github.com/preble/pyprocgame).

Since the theme and the name of the game has not yet been decided,
this repository will be called "project-alpha" for now. It will be renamed
in the future.

## Requirements

* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)

### Mac OS X Specific

* X11, [Xquartz](http://xquartz.macosforge.org/trac/wiki)

### Windows Specific

* [Cygwin](https://www.cygwin.com)
* X11, [Xming](https://sourceforge.net/projects/xming/files/latest/download)

## Running

Setup a development environment as follows:

Open a terminal (open Cygwin in Windows):

```bash
mkdir town-hall-pinball
cd town-hall-pinball
```

If you are not contributing back to the repositories or prefer to use https:
```bash
git clone https://github.com/town-hall-pinball/project-alpha.git
git clone https://github.com/town-hall-pinball/pinlib.git
```

Otherwise, register your SSH key and:
```bash
git clone git@github.com:town-hall-pinball/project-alpha.git
git clone git@github.com:town-hall-pinball/pinlib.git
```

Then:
``` bash
cd project-alpha
vagrant up
```

Wait for the command to complete, and run the software as follows:

```bash
vagrant ssh
pingame
```

A dot-matrix display should appear.

## Controls

Only a simple attract mode is available at the moment.

* ``1``: Left coin slot
* ``2``: Center coin slot
* ``3``: Right coin slot
* ``[``: Left flipper
* ``]``: Right flipper

Operator service mode:

* ``7``: Enter
* ``8``: Up
* ``9``: Down
* ``0``: Exit

## Easter Eggs

For the MM3 easter egg, execute the following commands from the `project-alpha`
directory:

```bash
mkdir ext
cd ext
git clone https://github.com/town-hall-pinball/mm3.git
```

This will not work out-of-the box and requires an external resources pack.
Contact us for the required URL.

Activate the Easter Egg in attract mode with the following:

* Left Flipper x 3
* Right Flipper x 3
* Start Button

## Contributing

It is quite early, but yes, contributions are completely welcome.
Send an email to `admin@townhallpinball.org` to be invited
to the discussion.

## Administrivia

* project-alpha: Copyright &copy; 2014 townhallpinball.org
* pinlib: Copyright &copy; 2014 townhallpinball.org
* pyprocgame: Copyright &copy; 2009-2011 Adam Preble and Gerry Stellenberg

See the [full license](LICENSE.md) for more information.

[Credits](CREDITS.md)
