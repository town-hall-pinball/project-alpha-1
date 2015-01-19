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

def init():
    p.load_mode(LagrangePointMode)

class LagrangePointMode(mode.Base):

    defaults = {
        "id": "lagrange",
        "label": "Lagrangian Points",
        "priority": 2315,
        "base": 10000,
        "start": ["next_player"],
        "stop": ["end_of_turn"]
    }

    def setup(self):
        self.panel = ui.ColumnPanel({
            "opaque": True,
            "enabled": False
        })
        self.title = ui.Text({
            "font": "medium_bold"
        })
        self.score = ui.Text({
            "font": "medium_bold"
        })
        self.panel.add(self.title)
        self.panel.add(self.score)
        self.display(self.panel)

        self.events = [
            ["active", "eject", self.award, 1]
        ]

    def start(self):
        p.state["lagrange"] = 0

    def award(self, sw=None):
        point = p.state["lagrange"]
        if point == 5:
            self.title.show("Lagrange Point")
            self.score.show("Tour Completed")
        else:
            point += 1
            earned = self.options["base"] * point
            self.title.show("Lagrange Point {}".format(point))
            self.score.show(util.format_score(earned))
            p.player.award(earned)
        p.state["lagrange"] = point
        self.panel.show()
        p.timers.set(2.0, self.release)

    def release(self):
        if p.machine.switch("eject").is_active():
            p.machine.coil("eject").pulse()
        self.panel.hide()
