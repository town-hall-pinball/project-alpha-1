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

class SearchMode(mode.Base):

    defaults = {
        "id": "search",
        "label": "Ball Search",
        "priority": 3900
    }

    def __init__(self, options):
        super(SearchMode, self).__init__(options)
        self.order = options.get("order", [])
        self.conditions = options.get("conditions", {})
        self.searching = False
        self.index = 0

    def setup(self):
        self.message = ui.Text({
            "font": "medium_bold",
            "opaque": True,
            "enabled": False,
        })
        self.display(self.message)
        self.events = [
            ["request_ball_search", self.run]
        ]

    def run(self, message="Ball Search"):
        if self.searching:
            return
        self.searching = True
        self.message.show(message)
        log.notify(message)
        self.fire()

    def fire(self):
        fired = False
        while not fired and self.index < len(self.order):
            coil = p.machine.coil(self.order[self.index])
            if coil.name in self.conditions:
                switch = self.conditions[coil.name]
                if p.machine.switch(switch).is_active():
                    fired = True
            else:
                fired = True
            if fired:
                coil.pulse()
            self.index += 1

        if self.index >= len(self.order):
            self.searching = False
            self.message.hide()
            self.index = 0
        else:
            p.timers.set(0.25, self.fire)
