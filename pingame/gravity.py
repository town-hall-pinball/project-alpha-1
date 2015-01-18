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
    p.load_mode(GravityAssistMode)

class GravityAssistMode(mode.Base):

    defaults = {
        "id": "gravity",
        "label": "Gravity Assist",
        "priority": 2210,
        "start": ["game_start"],
        "stop": ["game_over"],
        "max_bonus": 100000
    }

    def setup(self):
        self.events = [
            ["active", "uTurn", self.award]
        ]

    def award(self, sw=None):
        mult = p.state["spinner.multiplier"]
        message = ui.Message("Gravity Assist")
        if mult < 10:
            mult += 1
            message.add("{}x".format(mult))
        else:
            message.add(util.format_score(self.options["max_bonus"]))
            p.player.award(self.options["max_bonus"])
        self.display(message)
        message.show(2.0)
        p.state["spinner.multiplier"] = mult