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
from pinlib import p, dmd
from tests import fixtures

@unittest.skip
class TestComponentSetup(unittest.TestCase):

    def setUp(self):
        fixtures.init()

    def test_at(self):
        c = dmd.Component({
            "at": [1, 2]
        })
        self.assertEquals(1, c.style["x"])
        self.assertEquals(2, c.style["y"])

    def test_margin_4(self):
        c = dmd.Component({
            "margin": [1, 2, 3, 4]
        })
        self.assertEquals(1, c.style["margin-top"])
        self.assertEquals(2, c.style["margin-right"])
        self.assertEquals(3, c.style["margin-bottom"])
        self.assertEquals(4, c.style["margin-left"])

    def test_margin_3(self):
        c = dmd.Component({
            "margin": [1, 2, 3]
        })
        self.assertEquals(1, c.style["margin-top"])
        self.assertEquals(2, c.style["margin-right"])
        self.assertEquals(3, c.style["margin-bottom"])
        self.assertEquals(2, c.style["margin-left"])

    def test_margin_2(self):
        c = dmd.Component({
            "margin": [1, 2]
        })
        self.assertEquals(1, c.style["margin-top"])
        self.assertEquals(2, c.style["margin-right"])
        self.assertEquals(1, c.style["margin-bottom"])
        self.assertEquals(2, c.style["margin-left"])

    def test_margin_1(self):
        c = dmd.Component({
            "margin": 1
        })
        self.assertEquals(1, c.style["margin-top"])
        self.assertEquals(1, c.style["margin-right"])
        self.assertEquals(1, c.style["margin-bottom"])
        self.assertEquals(1, c.style["margin-left"])

    def test_padding_4(self):
        c = dmd.Component({
            "padding": [1, 2, 3, 4]
        })
        self.assertEquals(1, c.style["padding-top"])
        self.assertEquals(2, c.style["padding-right"])
        self.assertEquals(3, c.style["padding-bottom"])
        self.assertEquals(4, c.style["padding-left"])

    def test_padding_3(self):
        c = dmd.Component({
            "padding": [1, 2, 3]
        })
        self.assertEquals(1, c.style["padding-top"])
        self.assertEquals(2, c.style["padding-right"])
        self.assertEquals(3, c.style["padding-bottom"])
        self.assertEquals(2, c.style["padding-left"])

    def test_padding_2(self):
        c = dmd.Component({
            "padding": [1, 2]
        })
        self.assertEquals(1, c.style["padding-top"])
        self.assertEquals(2, c.style["padding-right"])
        self.assertEquals(1, c.style["padding-bottom"])
        self.assertEquals(2, c.style["padding-left"])

    def test_padding_1(self):
        c = dmd.Component({
            "padding": 1
        })
        self.assertEquals(1, c.style["padding-top"])
        self.assertEquals(1, c.style["padding-right"])
        self.assertEquals(1, c.style["padding-bottom"])
        self.assertEquals(1, c.style["padding-left"])

    def test_size(self):
        c = dmd.Component({
            "size": [1, 2]
        })
        self.assertEquals(1, c.style["width"])
        self.assertEquals(2, c.style["height"])


@unittest.skip
class TestComponentSizes(unittest.TestCase):

    def setUp(self):
        fixtures.init()
        self.c = dmd.Component({
            "margin": [2, 1],
            "padding": [20, 10],
            "size": [100, 200]
        })

    def test_inner_width(self):
        self.assertEquals(120, self.c.inner_width())

    def test_inner_height(self):
        self.assertEquals(240, self.c.inner_height())

    def test_outer_width(self):
        self.assertEquals(122, self.c.outer_width())

    def test_outer_height(self):
        self.assertEquals(244, self.c.outer_height())


@unittest.skip
class TestComponentTopLeft(unittest.TestCase):

    def setUp(self):
        fixtures.init()
        self.c = dmd.Component({
            "padding": [2, 1],
        })

    def test_left(self):
        self.assertEquals(1, self.c.left())

    def test_top(self):
        self.assertEquals(2, self.c.top())


@unittest.skip
class TestComponentAlignment(unittest.TestCase):

    def setUp(self):
        fixtures.init()
        self.c = dmd.Component({
            "size": [10, 20],
            "at": [1, 1]
        })

    def test_center_x(self):
        self.c.update_style({ "align": "center" })
        self.assertEquals(dmd.CENTER_X - 5, self.c.style["x"])

    def test_left(self):
        self.c.update_style({ "align": "left" })
        self.assertEquals(0, self.c.style["x"])

    def test_right(self):
        self.c.update_style({ "align": "right" })
        self.assertEquals(dmd.WIDTH - 10, self.c.style["x"])

    def test_center_y(self):
        self.c.update_style({ "vertical-align": "middle" })
        self.assertEquals(dmd.CENTER_Y - 10, self.c.style["y"])

    def test_top(self):
        self.c.update_style({ "vertical-align": "top" })
        self.assertEquals(0, self.c.style["y"])

    def test_bottom(self):
        self.c.update_style({ "vertical-align": "bottom" })
        self.assertEquals(dmd.HEIGHT - 20, self.c.style["y"])


@unittest.skip
class TestComponentRender(unittest.TestCase):

    def setUp(self):
        fixtures.init()
        self.c = dmd.Component({
            "margin": 2,
            "padding": 4,
            "size": [10, 20]
        })
        fixtures.reset()

    def test_fill(self):
        self.c.update_style({ "fill": 8 })
        self.c.frame.fill_rect.assert_called_with(0, 0, 18, 28, 8)

    def test_no_fill(self):
        self.c.invalidate()
        self.assertFalse(self.c.frame.fill_rect.called)

    def test_composite_next(self):
        self.c.composite_next(target=None)
        p.copy_rect.assert_called_with(None, 2, 2, self.c.frame, 0, 0,
            22, 32, "copy")

    def test_composite_next_offsets(self):
        self.c.x_offset = 1
        self.c.y_offset = 2
        self.c.composite_next(target=None)
        p.copy_rect.assert_called_with(None, 3, 4, self.c.frame, 0, 0,
            22, 32, "copy")
