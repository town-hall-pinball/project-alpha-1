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
from copy import deepcopy
from pinlib import p, util
from pinlib.dmd import effects

class Component(object):
    """
    A component is an item that can be rendered to a dot-matrix display.

    Each component has a :class:`procgame.dmd.Frame` object used for rendering.
    The `Frame` is created with the size of the component plus any padding.

    Components can aggregate other components to composite multiple frames
    to a single frame.

    The `style` is a dictionary that can contain the following:

    bottom
        Absolutely position the component this many dots from the bottom of
        the display.
    fill
        Fill in the background of this component, the content and the
        padding, with this color (0 - 15).
    height
        Set the height of the component to this many dots.
    left
        Absolutely position the component this many dots from the left of
        the display.
    margin
        Sets multiple margin values similar to CSS. If it is a single value,
        that value is applied to all margins. If it is a list, margins are
        set as follows:

            * [top/bottom, left/right]
            * [top, left/right, bottom]
            * [top, right, bottom, left]
    margin_bottom
        Add this many dots of spacing to the bottom of the component.
    margin_left
        Add this many dots of spacing to the left of the component.
    margin_right
        Add this many dots of spacing to the right of the component.
    margin_top
        Add this many dots of spacing to the top of the component.
    padding
        Sets multiple padding values similar to CSS. If it is a single
        value, that value is applied to all paddings. If it is a list,
        paddings are set as follows:

            * [top/bottom, left/right]
            * [top, left/right, bottom]
            * [top, right, bottom, left]
    padding_bottom
        Add this many dots of padding to the bottom of the component.
    padding_left
        Add this many dots of padding to the left of the component.
    padding_right
        Add this many dots of padding to the right of the component.
    padding_top
        Add this many dots of padding to the top of the component.
    right
        Absolutely position the component this many dots from the right of
        the display.
    top
        Absolutely position the component this many dots from the top of the
        display.
    width
        Set the width of the component to this many dots.

    If `width` and `height` are not specified, this base class defaults to
    using the dimensions of the dot-matrix display. Subclasses may
    override this behavior to automatically adjust based on the minimum size
    required to render this component.

    Paddings place inner space around a component and are useful for applying a
    background fill color. If a fill color is set, any blank space in the
    content of the component and the padding space is set to that color.

    Margins place outer space around a compoent and are useful for separating
    a component from other components. This base class simply adds the
    `margin_left` and `margin_top` to the `left` and `top` when compositing
    the frame but can be overridden by subclasses that perform layout.

    Subclasses can pass in other `defaults` for the style.
    """

    frame = None
    """
    The :class:`procgame.dmd.Frame` used to render this component.
    """

    parent = None
    """
    If this component is a member of another component, this is the reference
    to the component that contains it.
    """

    x = 0
    """
    The `x` location where this component's frame should be composited on the
    parent frame.
    """

    y = 0
    """
    The `y` location where this compoent's frame should be composited on the
    parent frame.
    """

    width = p.display.WIDTH
    """
    Width of the component's content.
    """

    height = p.display.HEIGHT
    """
    Height of the compoent's content.
    """

    opaque = False
    """
    If true, no other components will be rendered under this component.
    """

    enabled = True
    """
    If false, this component will be skipped during rendering.
    """

    def __init__(self, style=None, defaults=None):
        self.style = {}
        self.active_effects = {}
        self.defaults = {
            "top": None,
            "right": None,
            "bottom": None,
            "left": None,
            "width": None,
            "height": None,
            "fill": None,
            "margin_top": 0,
            "margin_right": 0,
            "margin_bottom": 0,
            "margin_left": 0,
            "opaque": False,
            "padding_top": 0,
            "padding_right": 0,
            "padding_bottom": 0,
            "padding_left": 0,
            "x_align": "center",
            "y_align": "center",
            "composite": "copy",
        }
        if defaults:
            self.defaults.update(defaults)
        self.set_style(style)
        self.components = []
        self.valid = False
        self.timer = None

    def apply_style(self, style=None):
        style = style if style else {}
        self.style.update(style)
        if "margin" in style:
            self.expand4("margin", util.to_list(style["margin"]))
        if "padding" in style:
            self.expand4("padding", util.to_list(style["padding"]))
        if "at" in style:
            self.style["left"] = style["at"][0]
            self.style["top"] = style["at"][1]
        if "size" in style:
            self.style["width"] = style["size"][0]
            self.style["height"] = style["size"][1]
        if "opaque" in style:
            self.opaque = style["opaque"]
        if "enabled" in style:
            self.enabled = style["enabled"]

    def update_style(self, style=None):
        self.apply_style(style)
        self.invalidate()

    def set_style(self, style=None):
        self.style.clear()
        self.apply_style(self.defaults)
        self.apply_style(style)
        self.invalidate()

    def invalidate(self):
        self.valid = False
        if self.parent:
            self.parent.invalidate()

    def revalidate(self):
        for component in self.components:
            if not component.valid:
                component.revalidate()
        self.layout()
        self.draw()
        self.valid = True

    def layout(self):
        style = self.style
        self.width = None
        self.height = None

        if style["width"] != None:
            self.width = style["width"]
        if style["height"] != None:
            self.height = style["height"]

        if self.width == None:
            if style["left"] != None and style["right"] != None:
                self.width = p.device.WIDTH - style["left"] - style["right"]
        if self.height == None:
            if style["top"] != None and style["bottom"] != None:
                self.height = p.device.HEIGHT - style["top"] - style["bottom"]

        if self.width == None or self.height == None:
            self.auto_size()

        self.x = None
        self.y = None

        # See if can be anchored to top left
        if style["left"] != None:
            self.x = style["left"]
        if style["top"] != None:
            self.y = style["top"]

        # See if can be anchored to bottom right
        if self.x == None and style["right"] != None:
            self.x = p.device.WIDTH - self.outer_width() - style["right"]
        if self.y == None and style["bottom"] != None:
            self.y = p.device.HEIGHT - self.outer_height() - style["bottom"]

        if self.x == None:
            self.x = math.floor((p.device.WIDTH - self.outer_width()) / 2.0)
        if self.y == None:
            self.y = math.floor((p.device.HEIGHT - self.outer_height()) / 2.0)

        self.x = self.x + style["margin_left"]
        self.y = self.y + style["margin_top"]


    def auto_size(self):
        if self.width == None:
            self.width = p.device.WIDTH
        if self.height == None:
            self.height = p.device.HEIGHT

    def draw(self):
        if ( self.frame == None or self.inner_width() > self.frame.width or
                self.inner_height() > self.frame.height ):
            self.frame = p.device.create_frame(self.inner_width(),
                    self.inner_height())
        self.frame.clear()
        fill = self.style["fill"]
        if fill != None:
            self.frame.fill_rect(0, 0, self.inner_width(),
                    self.inner_height(), fill)

    def next_frame(self):
        if self.enabled:
            return self.frame

    def composite_next(self, target):
        if not self.valid:
            self.revalidate()
        src = self.next_frame()
        if src != None:
            p.device.copy_rect(target,
                self.x,
                self.y,
                src, 0, 0,
                self.inner_width(),
                self.inner_height(),
                self.style["composite"])

    def inner_width(self):
        return (self.width +
                self.style["padding_left"] +
                self.style["padding_right"])

    def inner_height(self):
        return (self.height +
                self.style["padding_top"] +
                self.style["padding_bottom"])

    def outer_width(self):
        return (self.inner_width() +
                self.style["margin_left"] +
                self.style["margin_right"])

    def outer_height(self):
        return (self.inner_height() +
                self.style["margin_top"] +
                self.style["margin_bottom"])

    def left(self):
        return self.style["padding_left"]

    def top(self):
        return self.style["padding_top"]

    def enable(self, value=True):
        self.enabled = value
        self.invalidate()
        return self

    def disable(self):
        self.enabled = False
        self.invalidate()

    def hide(self):
        self.disable()

    def show(self, duration=None):
        self.enable()
        if duration:
            self.effect("show", { "duration": duration })
        else:
            self.stop_effect("show")

    def effect(self, name, options=None):
        if name in self.active_effects:
            self.active_effects[name].stop()
        self.active_effects[name] = effects.factory[name](self, options)
        self.active_effects[name].start()

    def stop_effects(self):
        for effect in self.active_effects.values():
            effect.stop()

    def stop_effect(self, name):
        if name in self.active_effects:
            self.active_effects[name].stop()
            del self.active_effects[name]

    def expand4(self, key, value):
        if len(value) == 1:
            value = [value[0], value[0], value[0], value[0]]
        elif len(value) == 2:
            value = [value[0], value[1], value[0], value[1]]
        elif len(value) == 3:
            value = [value[0], value[1], value[2], value[1]]
        self.style[key + "_top"] = value[0]
        self.style[key + "_right"] = value[1]
        self.style[key + "_bottom"] = value[2]
        self.style[key + "_left"] = value[3]



class Panel(Component):

    def __init__(self, style=None, defaults=None):
        defaults = defaults if defaults else {}
        defaults["width"] = defaults.get("width", p.device.WIDTH)
        defaults["height"] = defaults.get("height", p.device.HEIGHT)
        super(Panel, self).__init__(style, defaults)

    def add(self, component):
        component.parent = self
        self.components += [component]
        component.invalidate()
        return self

    def remove(self, component):
        self.components.remove(component)
        component.invalidate()
        return self

    def clear(self):
        self.components = []
        self.invalidate()
        return self

    def draw(self):
        super(Panel, self).draw()
        for item in self.components:
            frame = item.next_frame()
            if frame:
                p.device.copy_rect(self.frame,
                    item.x,
                    item.y,
                    frame, 0, 0,
                    item.inner_width(),
                    item.inner_height(),
                    item.style["composite"])


class ColumnPanel(Panel):

    def __init__(self, style=None):
        super(ColumnPanel, self).__init__(style, defaults={
            "width": None, "height": None
        })

    def auto_size(self):
        max_height = 0
        max_width = 0
        for item in self.components:
            max_height += item.outer_height()
            max_width = max(max_width, item.outer_width())
        if self.width == None:
            self.width = max_width
        if self.height == None:
            self.height = max_height

    def layout(self):
        super(ColumnPanel, self).layout()
        y = 0
        for item in self.components:
            item.y = y + item.style["margin_top"]
            y += item.outer_height()
            if self.style["x_align"] == "center":
                item.x = math.ceil((self.width - item.outer_width()) / 2.0)
            if self.style["x_align"] == "right":
                item.x = self.width - item.outer_width()
            item.x += item.style["margin_left"]

class RowPanel(Panel):

    def __init__(self, style=None):
        super(RowPanel, self).__init__(style, defaults={
            "width": None, "height": None
        })

    def auto_size(self):
        max_height = 0
        max_width = 0
        for item in self.components:
            max_width += item.outer_width()
            max_height = max(max_height, item.outer_height())
        if self.width == None:
            self.width = max_width
        if self.height == None:
            self.height = max_height

    def layout(self):
        super(RowPanel, self).layout()
        left_x = 0
        right_x = self.width
        for item in self.components:
            if item.style["x_align"] == "right":
                item.x = right_x - item.outer_width()
                right_x -= item.outer_width()
            else:
                item.x = left_x
                left_x += item.outer_width()
            if self.style["y_align"] == "center":
                item.y = math.ceil((self.height - item.outer_height()) / 2.0)
            if self.style["y_align"] == "bottom":
                item.y = self.height - item.outer_height()


class Text(Component):

    def __init__(self, style=None):
        super(Text, self).__init__(style, defaults={
            "font": "small_wide",
            "reverse": False,
            "text": "",
            "color": 0xf,
            "text_align": "left",
            "tracking": 1
        })

    def show(self, text, duration=None):
        self.style["text"] = text if text is not None else ""
        self.enable()
        if duration:
            self.effect("show", { "duration": duration })
        else:
            self.stop_effect("show")
        return self

    def auto_size(self):
        font = p.fonts[self.style["font"]]
        (text_width, text_height) = font.size(self.style["text"])
        if self.width == None:
            self.width = text_width
        if self.height == None:
            self.height = text_height

    def next_frame(self):
        if self.enabled and len(self.style["text"]) > 0:
            return self.frame

    def draw(self):
        super(Text, self).draw()
        font = p.fonts[self.style["font"]]
        composite_op = "sub" if self.style["reverse"] else "blacksrc"
        x = self.left()
        y = self.top()
        if self.style["text_align"] == "center":
            (text_width, text_height) = font.size(self.style["text"])
            x += round((self.width / 2.0) - (text_width / 2.0))
        font.draw(self.frame, self.style["text"], x, y,
                self.style["color"], composite_op, self.style["tracking"])


class ScriptPanel(Component):

    def __init__(self, style=None):
        super(ScriptPanel, self).__init__(style, defaults={
            "width": p.device.WIDTH, "height": p.device.HEIGHT
        })
        self.frames = []
        self.iter = util.CycleIterator(self.frames)
        self.timer = None
        self.active = False

    def add(self, item, duration=None):
        if hasattr(item, "frames"):
            for frame in item.frames:
                self.add(frame["component"], frame["duration"])
            return self
        if item:
            item.parent = self
            self.components += [item]
            item.invalidate()
        self.iter.add({
            "component": item,
            "duration": duration
        })
        return self

    def draw(self):
        super(ScriptPanel, self).draw()
        item = self.iter.get()["component"]
        if item:
            self.enable()
            frame = item.next_frame()
            if frame:
                p.device.copy_rect(self.frame,
                    item.x,
                    item.y,
                    frame, 0, 0,
                    item.inner_width(),
                    item.inner_height(),
                    "copy")
        else:
            self.disable()

    def update(self):
        if self.timer:
            p.timers.clear(self.timer)
            self.timer = None
        if len(self.iter.items) > 0:
            item = self.iter.get()
            if item["duration"] and self.active:
                self.timer = p.timers.set(item["duration"], self.next)
            self.draw()

    def next(self):
        self.iter.next()
        self.update()

    def previous(self):
        self.iter.previous()
        self.update()

    def reset(self):
        self.iter.index = 0
        self.update()

    def set_active(self, active):
        self.active = active
        self.update()


class Image(Component):

    def __init__(self, style=None):
        super(Image, self).__init__(style, defaults={
            "image": None,
            "reverse": False
        })

    def auto_size(self):
        if self.style["image"] != None:
            image =  p.images[self.style["image"]]
            width = image.width
            height = image.height
        else:
            width = 0
            height = 0
        if self.width == None:
            self.width = width
        if self.height == None:
            self.height = height

    def next_frame(self):
        if self.enabled and self.style["image"]:
            return self.frame

    def draw(self):
        super(Image, self).draw()
        if self.width == 0 or self.height == 9:
            return
        image = p.images[self.style["image"]]
        op  = "sub" if self.style["reverse"] else "copy"
        p.device.copy_rect(self.frame, self.left(), self.top(), image, 0, 0,
                image.width, image.height, op)


class Background(Image):

    def __init__(self, image):
        super(Background, self).__init__({ "image": image, "opaque": True })


class Rectangle(Component):

    def __init__(self, style=None):
        super(Rectangle, self).__init__(style)


class Message(ColumnPanel):

    def __init__(self, text=None, font="medium_bold", margin=1, opaque=True):
        super(Message, self).__init__({
            "opaque": opaque
        })
        if text:
            self.add(text, font, margin)

    def add(self, text, font="medium_bold", margin=0):
        super(Message, self).add(Text({
            "text": text,
            "font": font,
            "margin_bottom": margin
        }))
        return self


class Canvas(Component):

    def __init__(self, style=None):
        super(Canvas, self).__init__(style, defaults={
            "width": p.device.WIDTH, "height": p.device.HEIGHT
        })
        self.color = 0xf
        self.base = p.device.create_frame(p.device.WIDTH, p.device.HEIGHT)

    def clear(self):
        self.base.fill_rect(0, 0, self.base.width, self.base.height, 0)

    def dot(self, x, y):
        self.base.set_dot(x, y, self.color)

    def vline(self, x, top, length, color=None):
        color = color if color else self.color
        for y in xrange(top, top + length):
            self.base.set_dot(x, y, color)

    def hline(self, left, y, length, color=None):
        color = color if color else self.color
        for x in xrange(left, left + length):
            self.base.set_dot(x, y, color)

    def box(self, left, top, width, height, color=None):
        self.hline(left, top, width, color)
        self.hline(left, top + height - 1, width, color)
        self.vline(left, top, height, color)
        self.vline(left + width - 1, top, height, color)

    def draw(self):
        super(Canvas, self).draw()
        p.device.copy_rect(self.frame, self.left(), self.top(), self.base, 0, 0,
                self.base.width, self.base.height, "blacksrc")


class Animator(Component):

    def __init__(self, style=None, interval=1/30.0):
        super(Animator, self).__init__(style)
        self.interval = interval
        self.callback = None

    def start(self):
        self.active = True
        self.last_time = p.now
        self.elapsed = 0
        self.timer = p.timers.tick(self.handle)
        return self

    def stop(self):
        if self.active:
            self.active = False
            p.timers.clear(self.timer)
            self.timer = None
            if self.callback:
                self.callback()
        return self

    def handle(self):
        self.elapsed += p.now - self.last_time
        while self.elapsed > self.interval:
            self.update()
            self.elapsed -= self.interval
        self.last_time = p.now

    def complete(self, callback):
        self.callback = callback
        return self


class Animation(Animator):

    def __init__(self, style=None, interval=1/30.0):
        super(Animation, self).__init__(style, interval)
        animation_name = self.style.get("animation", None)
        if animation_name:
            self.animation = p.animations[animation_name]
        self.index = 0

    def set_animation(self, name):
        self.animation = p.animations.get(name)
        self.index = 0

    def update(self):
        if self.animation:
            self.index += 1
            if self.index >= len(self.animation.frames):
                self.stop()
            else:
                self.invalidate()

    def draw(self):
        if self.active and self.animation:
            self.frame = self.animation.frames[self.index]
