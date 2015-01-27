# Project Alpha

Visit our blog for news, updates, and videos:

http://townhallpinball.org

## About

Town Hall Pinball Studios is working on a customized pinball machine. The
overall plan is to:

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

Feel free to clone the repository and see development in action. This code
can be run without an actual pinball machine. Anything and everything can be
broken at anytime.

## Requirements

* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)

#### Mac OS X Specific

* X11, [Xquartz](http://xquartz.macosforge.org/trac/wiki)

#### Windows Specific

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

## Keyboard Controls

Operator service mode:

* ``7``: Enter
* ``8``: Down
* ``9``: Up
* ``0``: Exit

Important to know:

* ``1``: Coin slot (left)
* ``[``: Left flipper
* ``]``: Right flipper
* ``s``: Start Button
* ``p``: Ball Launch Button
* ``d``: Drain (Trough, 4)
* ``\``: Slam Tilt (Useful for quickly ending a game)

Other game switches:

* ``v``: Drop Target
* ``b``: Left subway entrance (behind drop target)
* ``n``: Center subway entrance (skull)
* ``/``: Spinner
* ``c``: Saucer
* ``'``: Tilt
* ``i``: Left Ramp, Enter
* ``k``: Left Ramp, Middle
* ``o``: Right Ramp, Enter
* ``l``: Right Ramp, Exit
* ``x``: Buy Extra Ball

## Web Console

The web console is enabled by default. To use, navigate to the following:

http://localhost:9000

See the video of the
[web console](https://www.youtube.com/watch?v=--j8BTRcH3A)
in action.

The web service can be enabled or disable in the service menu under
``Utilities -> Server``

## Ruleset

Completely boring at the moment, but it is a start:

* Ball save is active for five seconds. Only one save per ball.
* Kickback is lit at the start of each ball. Relight by hitting both standup
targets within a period of nine seconds.
* Hitting the drop target lowers the target. A shot to the left subway raises
the drop target. State of the drop target is preserved across balls.
* The scoop behind the drop target or the skull awards a Skull Time
value of 50,000.
* Center orbit shot awards a gravity assist. Each gravity assist increases the
spinner multipler by one to a maximum of ten. Once the maximum has been
reached, each additional shot awards 10,000. The spinner multiplier is reset
at the start of each ball.
* The spinner awards 100 times the amount of the spinner multiplier.
* Each visit to the saucer tours a Lagrange point. Points are as follows:
  * L1: 10,000 points
  * L2: 20,000 points
  * L3: 30,000 points
  * L4: 40,000 points
  * L5: 50,000 points
* No points are awarded once the Lagrange tour is complete. Visits are reset at
the start of each ball.
* Slingshots award 10 points.


## Mini-Games

Start the game by pressing *Buy Extra Ball* instead of *Start* to access the
mini-game menu. Work in progress. Expected mini-games:

* Timed 12-shot Challenge
* Multiball Madness

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
* Left Flipper
* Right Flipper

## Contributing

It is quite early, but yes, contributions are completely welcome.
Send an email to `admin@townhallpinball.org` to be invited
to the discussion.

## Administrivia

* project-alpha: Copyright &copy; 2014-2015 townhallpinball.org
* pinlib: Copyright &copy; 2014-2015 townhallpinball.org
* pyprocgame: Copyright &copy; 2009-2011 Adam Preble and Gerry Stellenberg

See the [full license](LICENSE.md) for more information.

Test (@mike-mcgann)

[Credits](CREDITS.md)
