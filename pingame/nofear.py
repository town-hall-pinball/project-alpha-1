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

def init():
    p.load_mode(GameMode)

magnet_timeout = 100

class GameMode(mode.Base):

    defaults = {
        "id": "no_fear",
        "label": "No Fear",
        "priority": 2200,
        "start": ["game_start"],
        "stop": ["game_over"]
    }

    def setup(self):
        self.events = [
            ["active",   "magnetLeft",    self.activate_magnet_left],
            ["inactive", "magnetLeft",    self.deactivate_magnet_left],
            ["active",   "magnetCenter",  self.activate_magnet_center],
            ["inactive", "magnetCenter",  self.deactivate_magnet_center],
            ["active",   "magnetRight",   self.activate_magnet_right],
            ["inactive", "magnetRight",   self.deactivate_magnet_right],
            ["active",   "subwayCenter",  self.popper_cycle],
        ]

    def popper_cycle(self, sw=None):
        switch = p.machine.switch("popperRight1")
        if switch.is_active():
            p.machine.coil("popperRight").pulse()

    def activate_magnet_left(self, sw=None):
        p.machine.coil("magnetLeft").pulsed_patter(1, 1, magnet_timeout)

    def deactivate_magnet_left(self, sw=None):
        p.machine.coil("magnetLeft").disable()

    def activate_magnet_center(self, sw=None):
        p.machine.coil("magnetCenter").pulsed_patter(1, 1, magnet_timeout)

    def deactivate_magnet_center(self, sw=None):
        p.machine.coil("magnetCenter").disable()

    def activate_magnet_right(self, sw=None):
        p.machine.coil("magnetRight").pulsed_patter(1, 1, magnet_timeout)

    def deactivate_magnet_right(self, sw=None):
        p.machine.coil("magnetRight").disable()
