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
from pingame.cargo import elements

def init():
    p.load_mode(CargoLoadMode)

class CargoLoadMode(mode.Base):

    defaults = {
        "id": "load",
        "label": "Cargo Load",
        "priority": 2400,
        "start": ["next_player", "load"],
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
            ["active",   "rampLeftMiddle",  self.left_ramp_made],
            ["active",   "rampRightExit",   self.right_ramp_made],
            ["active",   "orbitLeft",       self.left_orbit_made],
            ["active",   "orbitRight",      self.right_orbit_made],
            ["active",   "subwayCenter",    self.depart],
        ]

    def start(self):
        p.state["cargo"] = p.state.get("cargo", [])
        p.state["cargo_bins"] = p.state.get("cargo_bins", 3)
        p.state["ready"] = len(p.state["cargo"]) == p.state["cargo_bins"]
        p.state["visited"] = []

        if p.state["ready"]:
            self.ready()
        else:
            self.clear_ready()

    def stop(self):
        p.machine.lamp("scoopLeftArrow1").disable()
        p.machine.lamp("scoopCenterArrow1").disable()

    def left_orbit_made(self, sw=None):
        self.cargo("S")

    def left_ramp_made(self, sw=None):
        self.cargo("A")

    def right_ramp_made(self, sw=None):
        self.cargo("V")

    def right_orbit_made(self, sw=None):
        self.cargo("R")

    def cargo(self, item):
        cargo = p.state["cargo"]
        bins = p.state["cargo_bins"]
        cargo += [item]
        if len(cargo) > bins:
            cargo = cargo[1:bins+1]
        p.state["cargo"] = cargo
        if not p.state["ready"]:
            award = 10000 * len(cargo)
        else:
            award = 10000
        p.player.award(award)
        self.title.show("Loaded {}".format(elements[item]))
        self.score.show(util.format_score(award))
        self.panel.show(2.0)

        if not p.state["ready"] and len(cargo) == bins:
            p.state["ready"] = True
            self.ready()
            p.timers.set(2.0, self.ready_message)

    def ready(self):
        if p.state["drop_target"] != "down":
            p.state["drop_target"] = "down"
            p.machine.coil("dropTargetDown").pulse()
        p.machine.lamp("scoopLeftArrow1").patter()
        p.machine.lamp("scoopCenterArrow1").patter()

    def clear_ready(self):
        if p.state["drop_target"] != "up":
            p.state["drop_target"] = "up"
            p.machine.coil("dropTargetUp").pulse()
        p.machine.lamp("scoopLeftArrow1").disable()
        p.machine.lamp("scoopCenterArrow1").disable()

    def ready_message(self):
        self.title.show("Cleared for")
        self.score.show("Departure")
        self.panel.show(2.0)

    def depart(self, sw=None):
        if not p.state["ready"]:
            return
        p.machine.lamp("scoopLeftArrow1").disable()
        p.machine.lamp("scoopCenterArrow1").disable()
        p.state["popper_hold"] = True
        p.events.trigger("depart")
        self.deactivate()





