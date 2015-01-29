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

from pinlib import p, util
from pinlib.dmd import ui
from pinlib.modules import coin, highscore, script


class AttractMode(script.Script):

    defaults = {
        "id": "attract",
        "label": "Attract",
        "priority": 1300,
    }

    unit = 5.55 / 2.0

    def __init__(self, options):
        super(AttractMode, self).__init__(options)

    def setup(self):
        self.root = ui.ScriptPanel()

        background = ui.Background("attract/p-roc")
        town_hall = ui.Background("THP_Logo")
        presents = ui.Message("Presents")
        title = ui.Message(p.machine.config["game.name"])
        game_over = ui.Message("Game Over")
        #anim = ui.Animation({"animation": "tinatest"})

        #self.root.add(anim, self.unit)
        self.root.add(background, self.unit)
        self.root.add(town_hall, self.unit)
        self.root.add(presents, self.unit)
        self.root.add(title, self.unit)
        self.root.add(game_over, self.unit * 2)
        self.root.add(coin.credits(), self.unit * 2)
        #self.script.add(highscore.ClassicTable())
        self.root.add(None, self.unit * 2)

        self.display(self.root)

    def start(self):
        super(AttractMode, self).start()
        self.root.reset()
