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
from os import system

def init():
    p.load_mode(SkullMode)

class SkullMode(mode.Base):

    defaults = {
        "id": "skull",
        "label": "Skull Time!",
        "priority": 2311,
        "start": ["next_player"],
        "stop": ["end_of_turn"],
        "award": 50000
    }

    def setup(self):
        self.root = ui.Text({
            "padding": 0,
            "text": "Skull Time",
            "font": "medium_bold",
            "opaque": True,
            "enabled": False

        })
        self.display(self.root)

    def sw_subwayCenter_active(self, sw=None):
        self.skull_speak()

    def skull_speak(self):
        self.root.show("Skull Time!", 2.0).effect("pulse")
        p.player.award(self.options["award"])
        log.notify("Skull Time!")
        p.machine.coil("skullMouth").pulse()
