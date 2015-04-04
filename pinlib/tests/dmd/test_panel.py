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

from mock import MagicMock
import unittest
from pinlib import p, dmd
from tests import fixtures

@unittest.skip
class TestPanel(unittest.TestCase):

    def setUp(self):
        fixtures.init()
        self.panel = dmd.Panel()
        self.c1 = dmd.Component()
        self.c1.composite_next = MagicMock()
        self.c2 = dmd.Component()
        self.c2.composite_next = MagicMock()

    def test_add_single(self):
        result = self.panel.add(self.c1)
        self.assertEquals([self.c1], self.panel.components)
        self.assertEquals(result, self.panel)

    def test_add_multiple(self):
        self.panel.add(self.c1, self.c2)
        self.assertEquals([self.c1, self.c2], self.panel.components)

    def test_draw_none(self):
        self.assertFalse(self.c1.composite_next.called)
        self.assertEquals(None, self.panel.frame)

    def test_draw_two(self):
        self.panel.add(self.c1, self.c2)
        self.assertTrue(self.c1.composite_next.called)
        self.assertTrue(self.c2.composite_next.called)

    def test_draw_skip_disabled(self):
        self.c1.enabled = False
        self.panel.add(self.c1, self.c2)
        self.assertFalse(self.c1.composite_next.called)
        self.assertTrue(self.c2.composite_next.called)
