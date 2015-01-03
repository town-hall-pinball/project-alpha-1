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
    p.load_mode(BackgroundMode, { "start": ["reset"] })
    p.load_mode(GameMode,       {
        "start": ["game_reset"],
        "stop":  ["game_over"]
    })

class BackgroundMode(mode.Base):

    def __init__(self, options):
        options["id"] = options.get("id", "background")
        super(BackgroundMode, self).__init__(options, priority=100)

    def start(self):
        map(lambda lamp: lamp.enable(), p.machine.lamps("gi"))


class GameMode(mode.Base):

    def __init__(self, options):
        options["id"] = options.get("id", "game")
        super(GameMode, self).__init__(options, priority=110)

    def start(self):
        p.sounds.play_music("credits", start_time=2.4)
        p.events.on("next_player", self.next_player)
        print "**** enable?"
        self.machine.flippers().enable()

    def stop(self):
        p.events.off("next_player", self.next_player)
        self.machine.flippers().disable()

    def next_player(self):
        p.machine.coil("trough").pulse()

    def sw_troughStack_active(self, sw=None):
        p.game.next_player()

    def sw_spinner_active(self, sw=None):
        p.game.player.award(10)

    def sw_eject_active_for_2s(self, sw=None):
        p.game.player.award(100)
        p.machine.coil("eject").pulse()
