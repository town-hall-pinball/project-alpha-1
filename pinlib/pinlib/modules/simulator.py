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

def init():
    p.set_defaults({
        "simulator.enabled": False
    })
    p.load_mode(SimulatorMode)


class SimulatorMode(mode.Base):

    defaults = {
        "id": "simulator",
        "label": "Simulator",
        "priority": 1190
    }

    def setup(self):
        self.config = p.machine.config["simulator"]
        self.events = [
            ["switch", self.handle_device],
            ["coil", self.handle_device]
        ]
        self.balls = set()
        self.free = 0
        self.rules = {}
        for condition, rule in self.config["rules"].items():
            self.rules[condition] = rule

        if p.data["simulator.enabled"]:
            self.activate()

    def start(self):
        for name, active in self.config["initial"].items():
            switch = p.machine.switch(name)
            switch.activate(active)
            self.balls.add(name)

    def stop(self):
        balls = set(self.balls)
        for name in balls:
            switch = p.machine.switch(name)
            switch.deactivate()
            self.balls.remove(name)

    def handle_device(self, device, options):
        condition = "{}:{}={}".format(device.hardware, device.name,
                options["schedule"])
        if condition in self.rules:
            for rule in self.rules[condition]:
                self.evaluate_rule(condition, rule)

    def evaluate_rule(self, condition, rule):
        if "disable" in rule:
            p.machine.switch(rule["disable"]).deactivate()
            return

        source = rule.get("from", "")
        target = rule.get("to", "")

        # Is a free ball the source? Is one available?
        if not source and self.free == 0:
            return

        # Is the ball actually at the source location?
        if source and source not in self.balls:
            # Free ball on playfield?
            if self.free > 0:
                source = "" # Grab from playfield
            else:
                return

        # Is the target location blocked by a ball?
        if target in self.balls:
            return

        # If playfield to playfield, ignore
        if not source and not target:
            return

        sw_source = p.machine.switch(source) if source else None
        sw_target = p.machine.switch(target) if target else None

        source_name = sw_source.label if sw_source else "Playfield"
        target_name = sw_target.label if sw_target else "Playfield"
        p.events.trigger("simulate", source_name, target_name)

        if source:
            self.balls.remove(source)
            sw_source.deactivate()
        else:
            self.free -= 1

        if target:
            self.balls.add(target)
            sw_target.activate()
        else:
            self.free += 1

        #print condition, source_name, "to", target_name
        #print "free", self.free, "balls", self.balls
