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

from pinlib import p, log, mode, util
from pinlib.dmd import ui

def init():
    p.set_defaults({
        "tilt.warnings":2
    })

class TiltMode(mode.Base):

    defaults = {
        "id": "tilt",
        "label": "Tilt",
        "priority": 2890,
        "start": ["game_reset"]
    }
    wait = None

    def setup(self):
        self.root = ui.Text({
            "padding": 0,
            "text": "Tilt",
            "font": "medium_bold",
            "opaque": True,
            "enabled": False
        })
        self.display(self.root)
        self.events = [
            ["next_player", self.next_turn],
            ["drain_all", self.settled],
            ["active", "tilt", self.warning],
            ["active", "tiltSlam", self.slam_tilt]
        ]

    def next_turn(self):
        p.state["tilt"] = False
        p.state["tilt.warnings"] = 0

    def warning(self, tilt_level):
        max_warnings = p.data["tilt.warnings"]
        p.state["tilt.warnings"] += 1
        if p.state["tilt.warnings"] > max_warnings:
            self.tilt()
        else:
            self.root.show("Warning!", 2.0)

    def slam_tilt(self, sw=None):
        self.root.show("CHEATIN SON OF A GUN!", 2.0).effect("pulse")
        p.game.over()

    def tilt(self):
        p.state["tilt"] = True
        p.game.end_of_turn()
        self.root.show("Tilt")
        log.notify("Tilt")
        p.timers.set(1, self.release)
        self.wait = p.timers.set(3, self.settle_check)

    def release(self):
        delay = 0
        for switch, coil in self.options.get("releases", []):
            if p.machine.switch(switch).is_active():
                p.machine.coil(coil).pulse(delay=delay)
                delay += 250

    def settle_check(self):
        self.wait = None
        if p.balls.trough == p.balls.total:
            self.settled()

    def settled(self):
        if not self.wait and p.state.get("tilt", False):
            self.root.hide()
            p.timers.set(0.1, p.game.next_player)
