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

from pinlib import p, log, util

def init():
    p.set_defaults({
        "game.balls": 3,
        "game.max_players": 4,
    })
    p.game = Game()


class Player(object):

    def __init__(self, index):
        self.index = index
        self.number = index + 1
        self.score = 0
        self.state = {
            "bonus": {}
        }

    def award(self, points):
        self.score += points
        p.events.trigger("score")

    def adjust(self, points):
        self.score = points
        p.events.trigger("score")



class Game(object):

    active = False
    ball = 0
    order = None
    players = [Player(0)]
    handler = None

    def start(self):
        self.players = []
        self.order = util.CycleIterator()
        self.active = True
        self.ball = 1
        p.events.trigger("game_reset")

        start_name = "game_start"
        if self.handler:
            start_name += "_" + self.handler
        p.events.trigger(start_name)
        self.handler = None
        log.notify("Game Start")

        p.events.trigger("activate_playfield")
        self.add_player()
        p.player = self.order.get()
        p.state = p.player.state
        p.events.trigger("next_player")

    def add_player(self):
        if not self.active:
            p.events.trigger("request_check_game_start")
        elif self.ball == 1 and len(self.players) < p.data["game.max_players"]:
            self.new_player()

    def new_player(self):
        index = len(self.players)
        player = Player(index)
        self.players += [player]
        self.order.add(player)
        p.events.trigger("add_player", player)
        if index != 0:
            log.notify("Add Player")

    def next_player(self):
        p.player = self.order.next()
        p.state = p.player.state
        if p.player.index == 0:
            self.ball += 1
            if self.ball > p.data["game.balls"]:
                self.over()
        if self.active:
            p.events.trigger("activate_playfield")
            p.events.trigger("next_player")
            log.notify("Next Player")
            if p.player.index == 0:
                p.events.trigger("next_ball")
            log.notify("Ball {}, Player {}".format(
                    self.ball, p.player.number))

    def end_of_turn(self):
        p.events.trigger("end_of_turn")

    def over(self):
        self.active = False
        self.ball = 0
        p.events.trigger("game_over")
        log.notify("Game over")
