# no-fear

Visit our blog at:

http://townhallpinball.org

Since the theme and the name of the game has not yet been decided,
this repository will be called "no-fear" for now. It will be renamed
in the future.

## Requirements

* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)
* X11, [Mac OS X](http://xquartz.macosforge.org/trac/wiki)

### Windows Specific

* [Cygwin](https://www.cygwin.com)
* [Xming](https://sourceforge.net/projects/xming/files/latest/download)

## Running

Setup a development environment as follows:

Open a terminal (open Cygwin in Windows)

```bash
mkdir town-hall-pinball
cd town-hall-pinball
```

If you are not contributing back to the repositories or prefer to use https:
```bash
git clone https://github.com/town-hall-pinball/no-fear.git
git clone https://github.com/town-hall-pinball/pinlib.git
```

Otherwise, register your SSH key and:
```bash
git clone git@github.com:town-hall-pinball/no-fear.git
git clone git@github.com:town-hall-pinball/pinlib.git
```

Then:
``` bash
cd no-fear
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

## Development Notes

* The ``no-fear`` repository contains the code specific for the
machine and ruleset.
* The ``pinlib`` repository contains generic modules that can
be useful for any machine and ruleset. This provides the ``pyprocgame``
library that has custom patches applied and new code to provide
a nicer abstraction layer.

## Contributing

It is quite early, but yes, contributions are completely welcome.
Send an email to `admin@townhallpinball.org` to be invited
to the discussion.

## Administrivia

* Licensed under the [MIT license](LICENSE.md)
* [Credits](CREDITS.md)
