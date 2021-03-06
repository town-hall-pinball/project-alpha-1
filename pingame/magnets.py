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
    p.load_mode(MagnetsMode)

magnet_timeout = 100

class MagnetsMode(mode.Base):

    defaults = {
        "id": "magnets",
        "label": "Magnets",
        "priority": 2317,
        "start": ["next_player"],
        "stop": ["end_of_turn"]
    }

    def setup(self):
        self.events = [
            ["active",   "magnetLeft",    self.on],
            ["inactive", "magnetLeft",    self.off],
            ["active",   "magnetCenter",  self.on],
            ["inactive", "magnetCenter",  self.off],
            ["active",   "magnetRight",   self.on],
            ["inactive", "magnetRight",   self.off],
        ]

    def on(self, switch):
        p.machine.coil(switch.name).pulsed_patter(1, 1)

    def off(self, switch):
        p.machine.coil(switch.name).disable()
