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

from pinlib import p

class Animation(object):

    def __init__(self, options):
        super(Animation, self).__init__()
        self.options = options if options else {}
        self.interval = self.options.get("interval", 1/30.0)
        self.start_delay = self.options.get("delay", 0)
        self.delay = 0
        self.update_function = self.options.get("update", None)
        self.timer = None
        self.active = False

    def start(self):
        if not self.active:
            self.active = True
            self.last_time = p.now
            self.elapsed = 0
            self.delay = self.start_delay
            self.timer = p.timers.tick(self.tick)

    def stop(self):
        if self.active:
            self.active = False
            p.timers.clear(self.timer)
            self.timer = None

    def tick(self):
        self.elapsed += p.now - self.last_time
        while self.elapsed > self.interval + self.delay:
            self.update()
            self.elapsed -= self.interval
            self.delay = 0
        self.last_time = p.now

    def update(self):
        if self.update_function:
            self.update_function()


class Effect(Animation):

    def __init__(self, target, options=None):
        super(Effect, self).__init__(options)
        self.target = target


class Pulse(Effect):

    def __init__(self, target, options=None):
        super(Pulse, self).__init__(target, options)
        self.min_color = self.options.get("min_color", 0x4)
        self.max_color = self.options.get("max_color", 0xf)
        self.color = self.max_color
        self.fade = "out"

    def update(self):
        if self.color == self.max_color:
            self.fade = "out"
        if self.color == self.min_color:
            self.fade = "in"
        if self.fade == "in":
            self.color += 1
        if self.fade == "out":
            self.color -= 1
        self.target.update_style({"color": self.color})


class Show(Effect):

    def __init__(self, target, options=None):
        options["interval"] = options.get("duration", 3.0)
        super(Show, self).__init__(target, options)
        self.target.enable()

    def update(self):
        self.stop()

    def stop(self):
        super(Show, self).stop()
        self.target.disable()


factory = {
    "pulse": Pulse,
    "show": Show
}
