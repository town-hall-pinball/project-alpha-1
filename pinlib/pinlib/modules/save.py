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

import math
from pinlib import p, log, mode, util
from pinlib.dmd import ui

def init():
    p.set_defaults({
        "save.duration": 15
    })

class BallSaveMode(mode.Base):

    defaults = {
        "id": "ball_save",
        "label": "Ball Saver",
        "priority": 2111,
        "start": ["initial_launch"],
        "stop": ["end_of_turn"]
    }

    def setup(self):
        self.coil = p.machine.coil(self.options["coil"])
        self.flasher = p.machine.flasher(self.options["flasher"])

        self.panel = ui.Message("Ball Saved")
        self.panel.hide()
        self.display(self.panel)
        self.timer = None
        self.events = [
            ["drain_all", self.save],
        ]

    def start(self):
        self.flasher.patter(100, 127)
        self.timer = p.timers.set(p.data["save.duration"], self.timeout);
        p.state["saving"] = True

    def stop(self):
        self.flasher.disable()
        self.panel.hide()
        p.state["saving"] = False

    def save(self):
        if not p.state["saving"]:
            return
        log.notify("Ball Saved")
        p.timers.clear(self.timer)
        self.panel.show()
        self.coil.pulse()
        p.timers.set(2, self.deactivate)
        p.timers.defer(self.saved)

    def saved(self):
        p.state["saving"] = False

    def timeout(self):
        self.deactivate()
