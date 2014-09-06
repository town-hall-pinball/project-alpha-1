#
# Copyright (c) 2014 townhallpinball.org
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

from procgame import game
from pinlib import attract, frame

class AttractMode(attract.AttractMode):

    def __init__(self, sys):
        super(AttractMode, self).__init__(sys)
        self.sys = sys

    def mode_started(self):
        self.layer = (frame.Builder(self.sys.fonts)
            .move_y(7)
            .font("plain")
            .println("TOWN HALL PINBALL")
            .font("bold")
            .move_y(2)
            .println("PRESENTS")
            .end(3.0)
            .move_y(12)
            .println("NO FEAR")
            .end(3.0)
            .transition("push", direction="north")
            .empty(10.0)
            .script()
        )
