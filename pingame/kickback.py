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
    p.load_mode(KickbackMode)

class KickbackMode(mode.Base):

    defaults = {
        "id": "kickback",
        "label": "Kickback",
        "priority": 2316,
        "start": ["next_player"],
        "stop": ["end_of_turn"],
        "award_target_active": 10000,
        "award_target_inactive": 1000,
        "hurry_up_duration": 9,
        "blink_time": 500
    }
    timer = None
    hurry_up_lamp = None

    def setup(self):
        self.interval = self.options["hurry_up_duration"] / 3.0
        self.blink_time = self.options["blink_time"]
        self.target_lamps = {
            "top":    p.machine.lamp("standupTargetTop"),
            "bottom": p.machine.lamp("standupTargetBottom")
        }
        self.events = [
            ["active", "standupTargetTop", self.target],
            ["active", "standupTargetBottom", self.target],
            ["active", "kickback", self.kickback]
        ]

    def start(self):
        if "kickback" not in p.state:
            p.state["kickback"] = {
                "active": True,
            }
        self.state = p.state["kickback"]
        self.state["targets"] = {
            "top": False,
            "bottom": False
        }
        p.machine.lamp("kickback").enable()
        self.disable_target_lamps()

    def stop(self):
        p.machine.lamp("kickback").disable()
        self.disable_target_lamps()

    def disable_target_lamps(self):
        self.target_lamps["top"].disable()
        self.target_lamps["bottom"].disable()

    def target(self, switch):
        target = "top" if switch.name == "standupTargetTop" else "bottom"
        if self.state["active"] or self.state["targets"][target]:
            p.player.award(self.options["award_target_inactive"])
            return

        self.state["targets"][target] = True
        p.player.award(self.options["award_target_active"])

        if self.state["targets"]["top"] and self.state["targets"]["bottom"]:
            self.light_kickback()
        else:
            other = "bottom" if target == "top" else "top"
            self.target_lamps[target].enable()
            self.target_lamps[other].patter(self.blink_time)
            self.hurry_up_lamp = self.target_lamps[other]
            self.timer = p.timers.set(self.interval, self.hurry_up_1)

    def hurry_up_1(self):
        self.hurry_up_lamp.patter(self.blink_time / 2.0)
        self.timer = p.timers.set(self.interval, self.hurry_up_2)

    def hurry_up_2(self):
        self.hurry_up_lamp.patter(self.blink_time / 3.0)
        self.timer = p.timers.set(self.interval, self.timeout)

    def timeout(self):
        self.state["targets"]["top"] = False
        self.state["targets"]["bottom"] = False
        self.disable_target_lamps()

    def light_kickback(self):
        p.timers.clear(self.timer)
        self.state["active"] = True
        p.machine.lamp("kickback").enable()

        self.state["targets"]["top"] = False
        self.state["targets"]["bottom"] = False
        self.disable_target_lamps()

    def kickback(self, sw=None):
        if self.state["active"]:
            p.machine.coil("kickback").pulse()
            p.machine.lamp("kickback").disable()
            p.timers.clear(self.timer)
            self.state["active"] = False
