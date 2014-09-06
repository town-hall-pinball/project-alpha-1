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

import locale
from procgame import game
from pinlib import attract, frame

class AttractMode(attract.AttractMode):

    def __init__(self, sys):
        super(AttractMode, self).__init__(sys)
        self.sys = sys

    def mode_started(self):
        gc = locale.format("%d",
            int(self.sys.settings["high_score.grand_champion.score"]), True)
        hs1 = locale.format("%d",
            int(self.sys.settings["high_score.place1.score"]), True)
        hs2 = locale.format("%d",
            int(self.sys.settings["high_score.place2.score"]), True)
        hs3 = locale.format("%d",
            int(self.sys.settings["high_score.place3.score"]), True)
        hs4 = locale.format("%d",
            int(self.sys.settings["high_score.place4.score"]), True)

        credits = "FREE PLAY"
        if self.sys.coin:
            credits = self.sys.coin.credits_text()
        if (self.sys.settings["coin.free_play"] == "YES" or
                self.sys.data["coin.credits"] > 0):
            credits_message = "PRESS START"
        else:
            credits_message = "INSERT MONEY"

        self.layer = (frame.Builder(self.sys.resources)
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
            .println(credits)
            .move_y(4)
            .println(credits_message)
            .end(6.0)

            .move_y(5)
            .font("bold")
            .println("GRAND CHAMPION")
            .move_y(4)
            .align("left")
            .left(3)
            .prints(self.sys.settings["high_score.grand_champion.player"])
            .align("right")
            .right(3)
            .println(gc)
            .end(3.0)

            .move_y(12)
            .println("HIGHEST SCORES")
            .end(3.0)

            .move_y(5)
            .align("left")
            .left(3)
            .prints("1. ")
            .prints(self.sys.settings["high_score.place1.player"])
            .align("right")
            .right(3)
            .println(hs1)
            .move_y(4)

            .align("left")
            .left(3)
            .prints("2. ")
            .prints(self.sys.settings["high_score.place2.player"])
            .align("right")
            .right(3)
            .println(hs2)
            .end(3.0)

            .move_y(5)
            .align("left")
            .left(3)
            .prints("3. ")
            .prints(self.sys.settings["high_score.place3.player"])
            .align("right")
            .right(3)
            .println(hs3)
            .move_y(4)

            .align("left")
            .left(3)
            .prints("4. ")
            .prints(self.sys.settings["high_score.place4.player"])
            .align("right")
            .right(3)
            .println(hs4)
            .end(3.0)

            .empty(10.0)
            .script()
        )
