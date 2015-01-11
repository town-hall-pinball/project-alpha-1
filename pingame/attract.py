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

    unit = 5.55 / 2.0

    def __init__(self, options):
        options["id"] = "attract"
        options["label"] = "Attract"
        super(AttractMode, self).__init__(options, priority=22)
        self.script = ui.ScriptPanel()

        background = ui.Background("attract/p-roc")
        presents = ui.Message("Town Hall Pinball", "small_wide").add("Presents")
        no_fear = ui.Message(p.machine.config["game.name"])
        game_over = ui.Message("Game Over")

        #self.script.add(background, self.unit)
        self.script.add(presents, self.unit)
        self.script.add(no_fear, self.unit)
        self.script.add(game_over, self.unit * 2)
        self.script.add(coin.credits(), self.unit * 2)
        #self.script.add(highscore.ClassicTable())
        self.script.add(None, self.unit * 2)
        self.set_layer(self.script)

    def start(self):
        super(AttractMode, self).start()
        p.sounds.play_music("intro", start_time=0.5)
        self.script.reset()
