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

import pinlib as p
from pinlib import display, util
from pinlib.modules import coin, highscore, script

class Attract(script.Script):

    def __init__(self, options):
        super(Attract, self).__init__(options, priority=22)
        self.script = p.gfx.ScriptPanel()

        background = p.gfx.Background("Splash")
        presents = p.gfx.Message("TOWN HALL PINBALL", "plain").add("PRESENTS")
        no_fear = p.gfx.Message("NO FEAR")
        game_over = p.gfx.Message("GAME OVER")

        self.script.add(background, 3.0)
        self.script.add(presents, 3.0)
        self.script.add(no_fear, 3.0)
        self.script.add(game_over, 6.0)
        self.script.add(coin.credits(), 6.0)
        self.script.add(highscore.table_classic())
        self.script.add(None, 10.0)
        self.set_layer(self.script)
