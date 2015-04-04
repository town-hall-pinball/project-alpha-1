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

from pinlib import p
from pinlib.dmd import ui
from pinlib.modules.script import Script as BaseScript
from demo.base import Base

def init():
    p.load_mode("demo.modes.Script",    { "start": ["script"] })


class Script(BaseScript, Base):

    def __init__(self, options):
        super(Script, self).__init__(options, priority=1001)
        self.script = ui.ScriptPanel()
        for i in xrange(4):
            reverse = i % 2 != 0
            fill = 0xf if reverse else None
            frame = ui.Panel({
                "fill": fill
            })
            text = ui.Text({
                "font": "medium_bold",
                "text": "Panel " + str(i),
                "fill": fill,
                "reverse": reverse
            })
            frame.add(text)
            self.script.add(frame, duration=3.0)
        self.set_layer(self.script)
