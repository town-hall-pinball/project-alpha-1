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
    p.load_mode(Shoot12GameMode, {})

class Shoot12GameMode(mode.Base):

    defaults = {
        "id": "mini_12",
        "label": "12 Shot Challenge",
        "priority": 100,
        "start": ["game_start_mini_12"]
    }

    shots = {
        "subwayLeft": 2,
        "subwayCenter": 2,
        "rampLeftEnter": 2,
        "rampRightEnter": 2,
        "orbitLeft": 1,
        "orbitRight": 1,
        "standupTargetTop": 1,
        "standupTargetBottom": 1,
    }

    directors = {
        "subwayLeft": ["scoopLeftArrow2", "scoopLeftArrow1"],
        "subwayCenter": ["scoopCenterArrow2", "scoopCenterArrow1"],
        "rampLeftEnter": ["rampLeftCircle1", "rampLeftArrow"],
        "rampRightEnter": ["rampRightArrow2", "rampRightArrow1"],
        "orbitLeft": ["orbitLeftArrow1"],
        "orbitRight": ["orbitRightArrow1"],
        "standupTargetTop": ["standupTargetTop"],
        "standupTargetBottom": ["standupTargetBottom"]
    }

    def __init__(self, options):
        super(Shoot12GameMode, self).__init__(options)

    def setup(self):
        self.events = [
            ["add_player", self.add_player],
            ["next_player", self.next_player]
        ]
        for shot in self.shots.keys():
            self.events += [["active", shot, self.register_shot]]

    def add_player(self, player):
        player.state = {
            "remaining": 12,
            "shots": dict(self.shots)
        }

    def next_player(self):
        self.update()

    def update(self):
        for i in xrange(0, 12):
            lamp = p.machine.lamp("circle{:d}".format(i + 1))
            if i >= self.data["remaining"]:
                lamp.enable()
            else:
                lamp.disable()
        for switch, shots in self.data["shots"].items():
            for i, director in enumerate(self.directors[switch]):
                if shots < i + 1:
                    p.machine.lamp(director).disable()
                elif shots == i + 1:
                    p.machine.lamp(director).patter()
                else:
                    p.machine.lamp(director).enable()

    def register_shot(self, sw):
        shot = sw.name
        if p.state["shots"][shot] > 0:
            p.state["shots"][shot] -= 1
            p.state["remaining"] -= 1
            p.player.award(1)
            self.update()
            log.notify("{} shots remaining".format(self.data["remaining"]))
