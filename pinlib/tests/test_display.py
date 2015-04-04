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

import unittest
import pinlib as p
#from pinlib import display

@unittest.skip
class TestCreditsDisplay(unittest.TestCase):

    def setUp(self):
        p.pinlib_reset()
        p.data = {
            "coin.free_play": True,
            "coin.credits": 0
        }
        self.credits = display.credits()
        self.g = p.graphics()

    # Does the display initialize with the correct text?
    def test_initial(self):
        self.assertTrue(self.g.called("println", "FREE PLAY", "credits"))
        self.assertTrue(self.g.called("println", "PRESS START", "credits_message"))

    # Is the display updated when settings are changed to free play?
    def test_free_play(self):
        self.g.clear()
        p.data["coin.free_play"] = True
        p.events.trigger("save")
        self.assertTrue(self.g.called("set_text", "FREE PLAY"))
        self.assertTrue(self.g.called("set_text", "PRESS START"))

    # Is the display updated when settings are changed to paid play?
    def test_paid_play(self):
        self.g.clear()
        p.data["coin.free_play"] = False
        p.events.trigger("save")
        self.assertTrue(self.g.called("set_text", "CREDITS 0"))
        self.assertTrue(self.g.called("set_text", "INSERT COINS"))

    # Is the display updated when a full credit is inserted? Does it now
    # show "Press Start"?
    def test_add_credit(self):
        p.data["coin.free_play"] = False
        p.events.trigger("save")
        p.data["coin.credits"] = 1
        self.g.clear()
        p.events.trigger("add_credits")
        self.assertTrue(self.g.called("set_text", "CREDITS 1"))
        self.assertTrue(self.g.called("set_text", "PRESS START"))

    # Is "Insert Coins" shown when less than a full credit is available?
    def test_partial_credit(self):
        self.g.clear()
        p.data["coin.free_play"] = False
        p.data["coin.credits"] = 0.75
        p.events.trigger("save")
        self.assertTrue(self.g.called("set_text", "CREDITS 3/4"))
        self.assertTrue(self.g.called("set_text", "INSERT COINS"))

    # Can the display be changed from "Insert Coins" to "Insert Money"?
    def test_insert_money(self):
        self.g.clear()
        p.data["coin.free_play"] = False
        p.data["coin.units"] = "money"
        p.events.trigger("save")
        self.assertTrue(self.g.called("set_text", "CREDITS 0"))
        self.assertTrue(self.g.called("set_text", "INSERT MONEY"))
