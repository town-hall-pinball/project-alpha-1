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
from pingame.cargo import systems

def init():
    p.load_mode(DepartMode)

class DepartMode(mode.Base):

    defaults = {
        "id": "Depart",
        "label": "Depart",
        "priority": 2401,
        "start": ["depart"],
    }

    destinations = None

    def setup(self):
        self.panel = ui.ColumnPanel({
            "opaque": True,
            "enabled": False
        })
        self.line1 = ui.Text({
            "font": "medium_bold"
        })
        self.line2 = ui.Text({
            "font": "medium_bold"
        })
        self.panel.add(self.line1)
        self.panel.add(self.line2)
        self.display(self.panel)

        self.events = [
            ["active",   "flipperLeft",      self.left_flipper],
            ["active",   "flipperRight",     self.right_flipper],
            ["active",   "ballLaunchButton", self.select]
        ]

    def start(self):
        available = []
        for system in systems:
            if system not in p.state["visited"]:
                available += [system]
        self.destinations = util.CycleIterator(available)
        self.update()
        p.machine.lamp("ballLaunchButton").pulse()

    def stop(self):
        p.machine.lamp("ballLaunchButton").disable()

    def update(self):
        self.line1.show("Select Port")
        self.line2.show(self.destinations.get())
        self.panel.show()

    def left_flipper(self, sw=None):
        self.destinations.previous()
        self.update()

    def right_flipper(self, sw=None):
        self.destinations.next()
        self.update()

    def select(self, sw=None):
        self.deactivate()
        p.state["destination"] = self.destinations.get()
        p.events.trigger("travel")




