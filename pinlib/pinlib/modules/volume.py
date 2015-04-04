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
    p.set_defaults({
        "volume": 5
    })
    p.load_mode(VolumeMode, { "start": ["reset"] })


class VolumeMode(mode.Base):

    defaults = {
        "id": "volume",
        "label": "Volume",
        "priority": 3200
    }

    def __init__(self, options):
        super(VolumeMode, self).__init__(options)

    def setup(self):
        self.root = ui.Text({
            "padding": 3,
            "text": "Volume",
            "enabled": False
        })
        self.set_layer(self.root)
        self.set(p.data["volume"])

    def sw_serviceUp_active(self, sw=None):
        self.adjust(1)

    def sw_serviceDown_active(self, sw=None):
        self.adjust(-1)

    def adjust(self, amount):
        volume = p.data["volume"] + amount
        if volume < 0:
            volume = 0
        if volume > 10:
            volume = 10
        p.data["volume"] = volume
        self.set(volume)
        p.save()
        self.root.show("Volume " + str(volume), 2.0)

    def set(self, volume):
        p.sounds.volume = volume
        scaled = (volume * 0.1) ** 2
        p.sounds.set_volume(scaled)
