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
from pingame.cargo import elements, prices

def init():
    p.load_mode(TravelMode)

class TravelMode(mode.Base):

    defaults = {
        "id": "travel",
        "label": "Travel",
        "priority": 2402,
        "start": ["travel"],
    }

    base = 1000000
    messages = []

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

    def start(self):
        cargo = {
            "S": 0,
            "A": 0,
            "V": 0,
            "C": 0,
            "R": 0,
        }
        for item in p.state["cargo"]:
            cargo[item] += 1
        self.messages = []
        dest = p.state["destination"]
        total = 0
        for key, value in cargo.items():
            if value > 0:
                award = self.base * prices[dest][key] * value
                total += award
                p.player.award(award)
                element = elements[key]
                self.messages += [[
                    "{}: {}x".format(element, value),
                    util.format_score(award)
                ]]
        self.messages += [[
            "Total Payment",
            util.format_score(total)
        ]]
        self.next_message()

    def next_message(self):
        if len(self.messages) == 0:
            self.done()
            return
        message = self.messages.pop(0)
        self.line1.show(message[0])
        self.line2.show(message[1])
        self.panel.show()
        p.timers.set(2.0, self.next_message)

    def done(self):
        self.deactivate()
        p.state["cargo"] = []
        p.state["cargo_bins"] += 1
        dest = p.state["destination"]
        p.state["visited"] += [dest]

        switch = p.machine.switch("popperRight1")
        if switch.is_active():
            p.machine.flasher("flasherPopperRight").patter(100, 127)
            p.timers.set(1, self.pop)
        else:
            p.machine.coil("trough").pulse()
        p.events.trigger("score")
        p.events.trigger("load")

    def pop(self):
        p.machine.flasher("flasherPopperRight").disable()
        p.machine.coil("popperRight").pulse(delay=255)



