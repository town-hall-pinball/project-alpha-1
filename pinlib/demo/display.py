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
from pinlib.modules import highscore, script
from demo.base import Base

def init():
    p.load_mode("demo.display.HighScoreTableClassic", {
        "start": ["high-score-table-classic"]
    })
    p.load_mode("demo.display.HighScoreTableModern", {
        "start": ["high-score-table-modern"]
    })

class HighScoreTableClassic(script.Script, Base):

    def __init__(self, options):
        super(HighScoreTableClassic, self).__init__(options, priority=1001)
        self.script = highscore.ClassicTable()
        self.set_layer(self.script)

    def start(self):
        p.data["highscores"] = [
            ("PL1", 10000000),
            ("PL2",  9000000),
            ("PL3",  8000000),
            ("PL4",  7000000),
            ("PL5",  6000000)
        ]
        p.events.trigger("save")
        super(HighScoreTableClassic, self).start()


class HighScoreTableModern(script.Script, Base):

    def __init__(self, options):
        super(HighScoreTableModern, self).__init__(options, priority=1001)
        self.script = highscore.ModernTable()
        self.set_layer(self.script)

    def start(self):
        p.data["highscores"] = [
            ("PLAYER 1", 10000000),
            ("PLAYER 2",  9000000),
            ("PLAYER 3",  8000000),
            ("PLAYER 4",  7000000),
            ("PLAYER 5",  6000000)
        ]
        p.events.trigger("save")
        super(HighScoreTableModern, self).start()
