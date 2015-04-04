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

from collections import deque
from pinlib import p, util
from pinlib.dmd import ui
from demo.base import Base

def init():
    p.load_mode("demo.dmd.Gradient",    { "start": ["gradient"] })
    p.load_mode("demo.dmd.Text",        { "start": ["text"] })
    p.load_mode("demo.dmd.Image",       { "start": ["image"] })
    p.load_mode("demo.dmd.Alignment",   { "start": ["alignment"] })
    p.load_mode("demo.dmd.RowPanel",    { "start": ["row-panel"] })
    p.load_mode("demo.dmd.ColumnPanel", { "start": ["column-panel"] })


class Text(Base):

    content = ["aaaa", "bbbb", "cccc"]
    styles = [
        { "fill": None, "reverse": False },
        { "fill": 8, "reverse": False },
        { "fill": 8, "reverse": True },
    ]

    def __init__(self, options):
        super(Text, self).__init__(options)

        self.panel = ui.RowPanel({"opaque": True})
        self.text = []
        for content in self.content:
            text = ui.Text({
                "margin": [0, 5],
                "padding": [0, 1],
                "text": content
            })
            self.panel.add(text)
            self.text += [text]
        self.iter = util.CycleIterator(range(len(self.content)))
        self.set_layer(self.panel)
        self.update()

    def update(self):
        offset = self.iter.get()
        for i in xrange(len(self.text)):
            index = (i + offset) % len(self.text)
            self.text[index].update_style(self.styles[i])

    def sw_flipperRight_active(self, sw=None):
        self.iter.next()
        self.update()

    def sw_flipperLeft_active(self, sw=None):
        self.iter.previous()
        self.update()


class Image(Base):

    def __init__(self, options):
        super(Image, self).__init__(options)

        normal = ui.Image({
            "image": "image",
        })
        reverse = ui.Image({
            "image": "image",
            "fill": 0xf,
            "reverse": True
        })

        panel = ui.RowPanel()
        panel.add(normal)
        panel.add(reverse)
        self.set_layer(panel)


class Alignment(Base):

    specs = [
        { "text": "top left",      "top": 0, "left": 0 },
        { "text": "left center",   "left": 0, },
        { "text": "bottom left",   "bottom": 0, "left": 0 },
        { "text": "top center",    "top": 0 },
        { "text": "center" },
        { "text": "bottom center", "bottom": 0 },
        { "text": "top right",     "top": 0, "right": 0 },
        { "text": "center right",  "right": 0 },
        { "text": "bottom right",  "bottom": 0, "right": 0 }
    ]

    def __init__(self, options):
        super(Alignment, self).__init__(options)

        self.iter = util.CycleIterator(self.specs)
        self.iter.index = 4
        self.panel = ui.Panel({ "opaque": True })
        self.text = ui.Text()
        self.panel.add(self.text)
        self.set_layer(self.panel)
        self.update()

    def update(self):
        item = self.iter.get()
        self.text.set_style(item)

    def sw_flipperRight_active(self, sw=None):
        self.iter.next()
        self.update()

    def sw_flipperLeft_active(self, sw=None):
        self.iter.previous()
        self.update()


class RowPanel(Base):

    chars = "ABCDEFG"
    style = {
        "margin": [0, 2],
        "padding": [3, 5],
        "font": "medium_bold",
        "fill": 0x8
    }

    def __init__(self, options):
        super(RowPanel, self).__init__(options)

        self.panel = ui.RowPanel({
            "opaque": True,
            "vertical-align": "middle",
            "align": "center"
        })
        self.boxes = deque()
        self.set_layer(self.panel)
        self.add_box()

    def add_box(self):
        index = len(self.panel.components)
        if index >= len(self.chars):
            return
        text = ui.Text(self.style).set_text(self.chars[index])
        self.panel.add(text)
        self.boxes += [text]

    def remove_box(self):
        if len(self.panel.components) == 0:
            return
        self.panel.remove(self.boxes.pop())

    def sw_flipperRight_active(self, sw=None):
        self.add_box()

    def sw_flipperLeft_active(self, sw=None):
        self.remove_box()


class ColumnPanel(Base):

    chars = "ABCDE"
    style = {
        "margin": [1, 0],
        "padding": [0, 15],
        "fill": 0x8
    }

    def __init__(self, options):
        super(ColumnPanel, self).__init__(options)

        self.panel = ui.ColumnPanel({
            "vertical-align": "middle",
            "align": "center",
            "opaque": True
        })
        self.boxes = deque()
        self.set_layer(self.panel)
        self.add_box()

    def add_box(self):
        index = len(self.panel.components)
        if index >= len(self.chars):
            return
        text = ui.Text(self.style).set_text(self.chars[index])
        self.panel.add(text)
        self.boxes += [text]

    def remove_box(self):
        if len(self.panel.components) == 0:
            return
        self.panel.remove(self.boxes.pop())

    def sw_flipperRight_active(self, sw=None):
        self.add_box()

    def sw_flipperLeft_active(self, sw=None):
        self.remove_box()


class Gradient(Base):

    speeds = [0.5, 0.25, 0.1, 0.05, 0.025]
    modes = ["forward", "stop", "reverse"]
    each_width = p.device.WIDTH / 16

    def __init__(self, options):
        super(Gradient, self).__init__(options)
        self.rectangles = ui.RowPanel();
        self.offset = 0
        self.direction = -1
        self.speed_iter = util.CycleIterator(self.speeds)
        self.speed_iter.index = 2
        self.mode_iter = util.CycleIterator(self.modes)
        self.anim = ui.Animator({
            "update": self.update,
            "interval": self.speed_iter.get()
        })
        self.set_layer(self.anim)

    def update(self):
        self.offset = (self.offset + self.direction) % 16
        self.rectangles.clear()
        for i in xrange(self.offset, self.offset + 16):
            rect = ui.Rectangle({
                "fill": i % 16,
                "width": self.each_width
            })
            self.rectangles.add(rect)
        return self.rectangles

    def update_speed(self):
        speed = self.speed_iter.get()
        self.anim.update_style({"interval": speed})

    def sw_flipperRight_active(self, sw=None):
        self.speed_iter.next()
        self.update_speed()

    def sw_flipperLeft_active(self, sw=None):
        self.speed_iter.previous()
        self.update_speed()

    def sw_startButton_active(self, sw=None):
        self.mode_iter.next()
        mode = self.mode_iter.get()
        if mode == "reverse":
            self.anim.active = True
            self.direction = 1
        elif mode == "forward":
            self.anim.active = True
            self.direction = -1
        elif mode == "stop":
            self.anim.active = False
