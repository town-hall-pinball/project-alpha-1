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
    p.load_mode(DropTargetMode)

class DropTargetMode(mode.Base):

    defaults = {
        "id": "drop_target",
        "label": "Drop Target",
        "priority": 2314,
        "start": ["activate_playfield"],
        "stop": ["end_of_turn"]
    }

    def setup(self):
        self.events = [
            ["add_player", self.setup_player],
            ["next_player", self.next_player],
            ["active", "dropTarget", self.lower_target],
            ["active", "subwayLeft", self.raise_target]
        ]

    def setup_player(self, player):
        player.state["drop_target"] = "up"

    def next_player(self):
        state = p.state["drop_target"]
        switch = p.machine.switch("dropTarget")
        if state == "up" and switch.is_active():
            self.raise_target()
        elif state == "down" and switch.is_inactive():
            self.lower_target()

    def lower_target(self, sw=None):
        """
        p.state["drop_target"] = "down"
        p.machine.coil("dropTargetDown").pulse(delay=40)
        """

    def raise_target(self, sw=None):
        """
        p.state["drop_target"] = "up"
        p.machine.coil("dropTargetUp").pulse(delay=40)
        """
