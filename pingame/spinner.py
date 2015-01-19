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
    p.load_mode(SpinnerMode)

class SpinnerMode(mode.Base):

    defaults = {
        "id": "spinner",
        "label": "Spinner",
        "priority": 2313,
        "points": 100,
        "start": ["next_player"],
        "stop": ["end_of_turn"],
    }

    def setup(self):
        self.events = [
            ["next_player", self.next_turn],
            ["active", "spinner", self.award],
        ]

    def next_turn(self):
        p.state["spinner.multiplier"] = 1

    def award(self, sw=None):
        base = self.options["points"]
        mult = p.state["spinner.multiplier"]
        p.player.award(base * mult)
