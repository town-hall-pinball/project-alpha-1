# no-fear

Town Hall Pinball is working on a customized pinball machine. The
overall plan is to:

* Use an existing pinball machine, likely "No Fear"
* Completely rebrand it with a new play-field, backglass, and cabinet
  artwork
* Design a new theme
* Design a new ruleset
* Design and/or use new animations, sound effects, and music
* Design new software

Since the theme and the name of the game has not yet been decided,
this repository will be called "no-fear" for now. It will be renamed
in the future.

We are very early in the process and it will probably be some time
until real progress is made. In the mean time, feel free to clone
this repository and see development in action.

## Requirements

* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)
* X11, [Mac OS X](http://xquartz.macosforge.org/trac/wiki)

## Running

Setup a development environment as follows:

```bash
mkdir town-hall-pinball
cd town-hall-pinball
git clone https://github.com/town-hall-pinball/no-fear.git
git clone https://github.com/town-hall-pinball/pinlib.git
git clone https://github.com/town-hall-pinball/pyprocgame.git
cd no-fear
vagrant up
```

Wait for the command to complete, and run the software as follows:

```bash
vagrant ssh
( cd /vagrant ; python -m pingame )
```

A dot-matrix display should appear.

## Controls

Only a simple attract mode is available at the moment, but the
operator service mode can be controlled with:

* ``7``: Enter
* ``8``: Up
* ``9``: Down
* ``0``: Exit

## Development Notes

* The ``no-fear`` repository contains the code specific for the
machine and ruleset.
* The ``pinlib`` repository contains generic modules that can
be useful for any machine and ruleset. It also provides an
abstraction layer over pyprocgame in certain areas.
* The ``pyprocgame`` repository is a fork to fix certain issues
that cannot be monkey-patched or abstracted away. Issues for this
repository should be filed in the ``pinlib`` repository.

## Contributing

It is quite early, but yes, contributions are completely welcome.
Send an email to `admin@townhallpinball.org` to be invited
to the discussion.

## Administrivia

* Licensed under the [MIT license](LICENSE.md)
* [Credits](CREDITS.md)
