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

from pinlib import util
from pinlib.modes import attract

class Mode(attract.Mode):

    def __init__(self, options):
        super(Mode, self).__init__(options)
        self.set_layer(self.graphics(self.widgets)
            .image("Splash")
            .end(3.0)
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

            .move_y(12)
            .println("GAME OVER")
            .end(6.0)

            .move_y(5)
            .font("bold")
            .println("FREE PLAY", "credits")
            .move_y(4)
            .println("PRESS START", "credits_message")
            .end(6.0)

            .move_y(5)
            .font("bold")
            .println("GRAND CHAMPION")
            .move_y(4)
            .align("left")
            .left(3)
            .prints("---", "gc.name")
            .align("right")
            .right(3)
            .println("0", "gc.score")
            .end(3.0)

            .move_y(12)
            .println("HIGHEST SCORES")
            .end(3.0)

            .move_y(5)
            .align("left")
            .left(3)
            .prints("1. ")
            .prints("---", "hs1.name")
            .align("right")
            .right(3)
            .println("0", "hs1.score")
            .move_y(4)

            .align("left")
            .left(3)
            .prints("2. ")
            .prints("---", "hs2.name")
            .align("right")
            .right(3)
            .println("0", "hs2.score")
            .end(3.0)

            .move_y(5)
            .align("left")
            .left(3)
            .prints("3. ")
            .prints("---", "hs3.name")
            .align("right")
            .right(3)
            .println("0", "hs3.score")
            .move_y(4)

            .align("left")
            .left(3)
            .prints("4. ")
            .prints("---", "hs4.name")
            .align("right")
            .right(3)
            .println("0", "hs4.score")
            .end(3.0)

            .empty(10.0)
            .script()
        )

    def start(self):
        self.update()
