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

import math
from pinlib import p, mode, util
from pinlib.dmd import ui
from pinlib.modules import coin

def init():
    p.load_mode(ScoreDisplayMode, { "start": ["reset"] })

class ScoreDisplayMode(mode.Base):

    defaults = {
        "id": "score",
        "label": "Cargo Score Display",
        "priority": 1200
    }

    players = None

    def __init__(self, options):
        super(ScoreDisplayMode, self).__init__(options)

    def setup(self):
        root = ui.Panel()
        self.player = ui.Text({
        })
        self.cargo = ui.Text({
            "top": 0,
        })
        self.ball = ui.Text({
            "bottom": 0,
            "font": "small",
        })
        root.add(self.player)
        root.add(self.cargo)
        root.add(self.ball)
        self.display(root)

        self.events = [
            ["credits_changed", self.update],
            ["add_player", self.update],
            ["next_player", self.update],
            ["game_reset", self.update],
            ["game_over", self.update],
            ["score", self.update],
        ]

    def start(self):
        self.update()

    def update(self, *args, **kwargs):
        self.update_score(self.player, 0, single=True)
        if p.game.active and p.state:
            bins = p.state.get("cargo_bins", 3)
            cargo = p.state.get("cargo", [])
            binstr = ""
            for i in xrange(0, bins):
                if i > len(cargo) - 1:
                    binstr += "-"
                else:
                    binstr += cargo[i]
            self.cargo.show(binstr)
            self.ball.show("Ball {}".format(p.game.ball))
        else:
            self.cargo.hide()
            self.ball.hide()

    def update_score(self, text, index, single):
        show = True
        if single and len(p.game.players) > 1:
            show = False
        if not single and len(p.game.players) == 1:
            show = False
        if index >= len(p.game.players):
            show = False
        if show:
            score = p.game.players[index].score
            self.update_score_size(text, single, index)
            text.show(util.format_score(score))
        else:
            text.hide()

    def update_score_size(self, text, single, index):
        score = p.game.players[index].score
        if single:
            if score < 1e9:
                text.apply_style({ "font": "huge_wide" })
            elif score < 1e10:
                text.apply_style({ "font": "huge" })
            else:
                text.apply_style({ "font": "huge_narrow"})
        elif not single and p.game.active and p.player.index == index:
            if score < 1e6:
                text.apply_style({ "font": "large_wide" })
            elif score < 1e7:
                text.apply_style({ "font": "large" })
            else:
                text.apply_style({ "font": "large_narrow"})
        else:
            if score < 1e6:
                text.apply_style({ "font": "medium_wide" })
            elif score < 1e7:
                text.apply_style({ "font": "medium" })
            else:
                text.apply_style({ "font": "medium_narrow"})

