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

class LaunchMode(mode.Base):

    defaults = {
        "id": "launch",
        "label": "Auto Launcher",
        "priority": 2110,
        "start": ["next_player"],
        "stop": ["end_of_turn"]
    }

    def setup(self):
        self.coil = p.machine.coil(self.options["coil"])
        self.button = p.machine.switch(self.options["button"])
        self.lamp = p.machine.lamp(self.options["lamp"])
        self.lane = p.machine.switch(self.options["lane"])

        self.events = [
            ["active", self.lane.name, self.update_lamp],
            ["active", self.lane.name, self.check_auto_launch, 1],
            ["inactive", self.lane.name, self.shooter_lane_inactive],
            ["active", self.button.name, self.launch_requested]
        ]

    def start(self):
        p.state["launch"] = {
            "auto": False,
            "launched": False,
        }
        self.state = p.state["launch"]

    def stop(self):
        self.state["auto"] = False
        self.lamp.disable()

    def update_lamp(self, sw=None):
        if not self.state["auto"]:
            self.lamp.patter()

    def check_auto_launch(self, sw=None):
        if self.state["auto"]:
            self.coil.pulse()

    def shooter_lane_inactive(self, sw=None):
        self.lamp.disable()

    def launch_requested(self, sw=None):
        ready = self.lane.is_active()
        if not self.state["auto"] and ready:
            self.launch()

    def launch(self):
        self.coil.pulse()
        self.state["auto"] = True
        if not self.state["launched"]:
            p.events.trigger("initial_launch")
            self.state["launched"] = True
        p.events.trigger("launch")
