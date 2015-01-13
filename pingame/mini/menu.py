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

from pinlib import p, log, mode, util
from pinlib.dmd import ui

class TriggerMode(mode.Base):

    defaults = {
        "id": "mini_trigger",
        "label": "Mini Game Menu Trigger",
        "priority": 1800,
        "button": "buyExtraBallButton",
        "lamp": "buyExtraBallButton",
        "start": ["attract_started"],
        "stop": ["attract_stopped"]
    }

    def __init__(self, options):
        super(TriggerMode, self).__init__(options)

    def setup(self):
        self.button = p.machine.switch(self.options["button"])
        self.lamp = p.machine.lamp(self.options["lamp"])
        self.events = [
            ["active", self.button.name, self.menu],
            ["credits_changed", self.update_button]
        ]

    def start(self):
        self.update_button()

    def stop(self):
        self.lamp.disable()

    def menu(self, sw=None):
        p.events.trigger("request_mini_menu")

    def update_button(self):
        free_play = p.data.get("coin.free_play", True)
        credits = p.data.get("coin.credits", 0)
        if free_play or credits >= 1:
            self.lamp.patter()
        else:
            self.lamp.disable()


class MenuMode(mode.Base):

    defaults = {
        "id": "mini_menu",
        "label": "Mini Game Menu",
        "priority": 1500,
        "stop": ["game_reset"]
    }

    games = [
        ["mini_12", "12 Shot Challege"],
        ["mini_multiball", "Multiball Madness"],
        ["cancel", "Cancel"]
    ]

    def __init__(self, options):
        super(MenuMode, self).__init__(options)

    def setup(self):
        self.root = ui.Panel({
            "opaque": True
        })
        self.title = ui.Text({
            "top": 2,
            "font": "small_narrow",
            "text": "Extra Mini Games"
        })
        self.name = ui.Text({
            "font": "medium_bold",
            "text": "12 Shot Challenge"
        })
        self.instructions = ui.Text({
            "bottom": 2,
            "font": "small_narrow_full",
            "text": "Use Flippers to Select"
        })
        self.root.add(self.title)
        self.root.add(self.name)
        self.root.add(self.instructions)
        self.display(self.root)

        self.iter = util.CycleIterator(self.games)
        self.events = [
            ["active", "flipperLeft", self.previous],
            ["active", "flipperRight", self.next],
            ["active", "startButton", self.check_cancel]
        ]

    def start(self):
        p.events.trigger("cancel_attract")
        self.iter.index = 0
        self.update()
        self.name.effect("pulse")

    def update(self):
        handler = self.iter.get()[0]
        name = self.iter.get()[1]
        if handler == "cancel":
            p.game.enabled = False
            p.game.handler = None
        else:
            p.game.enabled = True
            p.game.handler = handler
        self.name.update_style({ "text": name })

    def next(self, sw=None):
        self.iter.next()
        self.update()

    def previous(self, sw=None):
        self.iter.previous()
        self.update()

    def check_cancel(self, sw=None):
        handler = self.iter.get()[0]
        if handler == "cancel":
            self.deactivate()
            p.game.enabled = True
            p.events.trigger("request_attract")
            p.events.trigger("request_mini_trigger")
