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

def init():
    p.load_mode(BallMode)


class BallMode(mode.Base):

    defaults = {
        "id": "ball",
        "label": "Ball Management",
        "priority": 1100
    }

    def setup(self):
        p.balls.total = p.machine.config["PRGame"]["numBalls"]
        self.active = False
        self.troughs = set()
        self.holds = set()
        self.drain = None
        self.events = [
            ["request_check_game_start", self.check_game_start],
        ]
        switches = set()
        for switch in p.machine.switches():
            if "trough" in switch.tags:
                self.troughs.add(switch.name)
                switches.add(switch)
            if "hold" in switch.tags:
                self.holds.add(switch.name)
                switches.add(switch)
            if "drain" in switch.tags:
                self.drain = switch
                switches.add(switch)
        for switch in switches:
            self.events += [["active", switch.name, self.switch_event, 0.1]]
            self.events += [["inactive", switch.name, self.switch_event, 0.1]]
        self.update()
        self.activate()

    def update(self):
        p.balls.free = p.balls.total
        p.balls.trough = 0
        p.balls.held = 0
        troughs = []
        holds = []
        for trough in self.troughs:
            if p.machine.switch(trough).is_active():
                troughs += [trough]
                p.balls.free -= 1
                p.balls.trough += 1
        for hold in self.holds:
            if p.machine.switch(hold).is_active():
                holds += [hold]
                p.balls.free -= 1
                p.balls.held += 1
        if p.balls.free > 0:
            self.active = True
        #log.notify("trough {}, held {}, free {}, troughs {}, holds {}".format(
        #        p.balls.trough, p.balls.held, p.balls.free, troughs, holds))

    def switch_event(self, switch):
        self.update()
        if switch.name == self.drain.name and switch.is_active():
            p.events.trigger("drain")
            log.notify("Drain")
        if self.active and p.balls.trough == p.balls.total:
            p.events.trigger("drain_all")
            log.notify("Balls Secured")
            self.active = False

    def check_game_start(self):
        self.update()
        if p.balls.trough != p.balls.total:
            p.events.trigger("request_ball_search")
        else:
            p.game.start()
