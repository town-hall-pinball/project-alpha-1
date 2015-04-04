#
# Copyright (c) 2014 - 2015 townhallpinball.org
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from pinlib import p, mode, util
from pinlib.dmd import ui

class SplashMode(mode.Base):

    defaults = {
        "id": "splash",
        "label": "Splash Screen",
        "priority": 1690,
        "duration": 2
    }

    def __init__(self, options):
        super(SplashMode, self).__init__(options)
        self.name = p.machine.config.get("game.name", "Name")
        self.version = p.machine.config.get("game.version", "")
        self.release = p.machine.config.get("game.release", "")

    def setup(self):
        self.root = (ui.Message()
            .add(self.name, font="medium_bold", margin=3)
            .add(self.version, font="small_narrow")
            .add(self.release, font="small_narrow_full"))
        self.display(self.root)

    def start(self):
        p.timers.set(self.options["duration"], self.deactivate)
