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

def init():
    p.set_defaults({
        "coin.free_play": True,
        "coin.pricing": 0.50,
        "coin.credits.max": 99,
        "coin.units": "coins",

        "coin.credits": 0,
        "coin.earnings": 0,
        "coin.credits.paid": 0,
        "coin.credits.service": 0,
    })
    p.events.on("request_clear_credits", credits_clear)
    p.events.on("request_clear_audits", audits_clear)
    p.events.on("pricing_changed", pricing_change)


# FIXME: Make this a class
def credits():
    panel = ui.ColumnPanel({
        "align": "center",
        "vertical-align": "middle",
        "opaque": True
    })
    amount = ui.Text({"font": "medium_bold", "margin": 1})
    message = ui.Text({"font": "medium_bold", "margin": 1})
    panel.add(amount).add(message)

    def update():
        free_play = p.data["coin.free_play"]
        credits = p.data["coin.credits"]
        unit = p.data["coin.units"].upper()
        if free_play:
            amount.show("Free Play")
            message.show("Press Start")
        else:
            amount.show("Credits " + util.fraction(credits))
            if credits >= 1:
                message.show("Press Start")
            else:
                message.show("Insert " + unit)

    update()
    p.events.on("credits_changed", update)
    p.events.on("save", update)
    return panel


class CoinMode(mode.Base):

    defaults = {
        "id": "coin",
        "label": "Coin",
        "priority": 1400
    }

    def __init__(self, options):
        super(CoinMode, self).__init__(options)

    def setup(self):
        self.events = [
            ["request_service_credit", self.service_credit],
            ["game_reset", self.update_button],
            ["game_over", self.update_button],
            ["add_player", self.add_player],
            ["active", "coinLeft", self.left_coin],
            ["active", "coinCenter", self.center_coin],
            ["active", "coinRight", self.right_coin],
            ["active", "startButton", self.start_button]
        ]
        self.root = credits()
        self.root.hide()
        self.display(self.root)

    def start(self):
        self.update_button()

    def _is_max(self):
        return p.data["coin.credits"] >= p.data["coin.credits.max"]

    def left_coin(self, sw=None):
        self.paid_credit(0)

    def center_coin(self, sw=None):
        self.paid_credit(1)

    def right_coin(self, sw=None):
        self.paid_credit(2)

    def start_button(self, sw=None):
        if p.data["coin.free_play"] or p.data["coin.credits"] >= 1:
            p.game.add_player()

    def add_player(self, player):
        self.use_credit()

    def service_enter(self, sw=None):
        p.events.trigger("request_service_credit")

    def paid_credit(self, slot):
        value = 0.25
        pricing = p.data["coin.pricing"]
        add = value / pricing
        p.data["coin.earnings"] += value
        p.data["coin.credits.paid"] += add
        self.add_credit(add)

    def service_credit(self):
        p.data["coin.credits.service"] += 1
        self.add_credit()

    def add_credit(self, add=1):
        if self._is_max():
            return
        p.data["coin.credits"] += add
        self.show()
        p.events.trigger("credits_changed")
        p.save()
        self.update_button()

    def use_credit(self):
        if p.data["coin.credits"] < 1:
            return
        p.data["coin.credits"] -= 1
        p.events.trigger("credits_changed")
        p.save()
        self.update_button()

    def show(self):
        p.sounds.play("coin/insert")
        if not p.game.active and not p.data["coin.free_play"]:
            self.root.show(2)

    def hide(self):
        self.root.hide()

    def update_button(self):
        button = p.machine.lamp("buttonStart")
        available = p.data["coin.free_play"] or p.data["coin.credits"] >= 1

        if not available:
            button.disable()
        elif not p.game.active and available:
            button.patter()
        else:
            button.enable()


def credits_string():
    if p.data.get("coin.free_play", True):
        return "Free Play"
    credits = p.data.get("coin.credits", 0)
    return "Credits " + util.fraction(credits)

def credits_clear():
    p.data["coin.credits"] = 0
    p.save()

def audits_clear():
    p.data["coin.earnings"] = 0
    p.data["coin.credits.paid"] = 0
    p.data["coin.credits.service"] = 0
    p.save()

def pricing_change():
    p.data["coin.credits"] = int(math.floor(p.data["coin.credits"]))
    p.save()
