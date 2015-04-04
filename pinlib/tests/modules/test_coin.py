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
from pinlib import p
from pinlib.modules import coin

@unittest.skip
class TestCoin(unittest.TestCase):

    def setUp(self):
        p.pinlib_reset()
        self.coin = p.use("pinlib.modes.coin.Coin")
        self.g = p.graphics()

    # Does the left coin chute add half a credit?
    def test_coin_left(self):
        self.coin.sw_coinLeft_active()
        self.assertEquals(0.5, p.data["coin.credits"])

    # Does the center coin chute add half a credit?
    def test_coin_center(self):
        self.coin.sw_coinCenter_active()
        self.assertEquals(0.5, p.data["coin.credits"])

    # Does the right coin chute add half a credit?
    def test_coin_right(self):
        self.coin.sw_coinRight_active()
        self.assertEquals(0.5, p.data["coin.credits"])

    # If it is $1.00 to play, does the coin chute add a quarter of a credit?
    def test_dollar_pricing(self):
        p.data["coin.pricing"] = 1
        self.coin.sw_coinLeft_active()
        self.assertEquals(0.25, p.data["coin.credits"])

    # Can the operator add a service credit?
    def test_service_credit(self):
        p.events.trigger("request_service_credit")
        self.assertEquals(1, p.data["coin.credits"])

    # Are coins recorded in earnings and credits paid?
    def test_audit_paid(self):
        self.coin.sw_coinLeft_active()
        self.assertEquals(0.25, p.data["coin.earnings"])
        self.assertEquals(0.5, p.data["coin.credits.paid"])

    # Are service credits recorded?
    def test_audit_service(self):
        p.events.trigger("request_service_credit")
        self.assertEquals(0, p.data["coin.earnings"])
        self.assertEquals(1, p.data["coin.credits.service"])

    # Will the machine refuse to add more than 99 credits?
    def test_max_credits(self):
        p.data["coin.credits"] = 99
        self.coin.sw_coinLeft_active()
        self.assertEquals(99, p.data["coin.credits"])

    # Is the credits display shown when a coin is inserted?
    def test_credits_display(self):
        p.data["coin.free_play"] = False
        self.coin.sw_coinLeft_active()
        self.assertTrue(self.coin.get_layer())

    # Is the display unchanged when a coin is inserted when in free play?
    def test_no_credits_display_for_free_play(self):
        p.data["coin.free_play"] = True
        self.g.clear()
        self.coin.sw_coinLeft_active()
        self.assertFalse(self.coin.get_layer())
