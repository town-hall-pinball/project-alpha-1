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

def init():
    p.load_mode(GameMode)


class GameMode(mode.Base):

    defaults = {
        "id": "main_game",
        "label": "Project Alpha",
        "priority": 2300,
        "start": ["game_start"],
        "stop": ["game_over"]
    }

    state = "over"

    def setup(self):
        self.events = [
            ["drain_all", self.balls_secured],
            ["end_of_turn", self.end_of_turn],
            ["inactive", "shooterLane",    self.check_launch],
        ]

    def start(self):
        p.events.on("next_player", self.next_player)

    def stop(self):
        p.events.off("next_player", self.next_player)
        p.sounds.stop_music()
        self.machine.flippers().disable()

    def next_player(self):
        self.machine.flippers().enable()
        self.state = "launch"
        p.sounds.play_music("Introduction", start_time=0.5, loops=-1)
        p.machine.coil("trough").pulse()

    def check_launch(self, sw=None):
        if self.state == "launch":
            self.state = "play"
            p.sounds.play_music("Credits", start_time=2.25, loops=-1)

    def end_of_turn(self):
        self.state = "end_of_turn"
        p.sounds.stop_music()
        self.machine.flippers().disable()

    def balls_secured(self):
        if not p.state.get("tilt", False):
            p.game.end_of_turn()
            p.events.trigger("request_bonus")

    def sw_kickback_active(self, sw=None):
        p.machine.coil("kickback").pulse()
