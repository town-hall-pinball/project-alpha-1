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

from pinlib import p, log

class Base(object):

    defaults = None

    def __init__(self, options, priority=None):
        self.options = {}
        if self.defaults:
            self.options.update(self.defaults)
        self.options.update(options);

        self.priority = priority if priority else self.options.get("priority", 0)
        self.settings = p.data
        self.data = p.data
        self.machine = p.machine
        self.sound = p.sounds
        self.events = p.events
        self.active = False
        self.root = None
        self._layer = None

        self.ident = self.options.get("id", self.__class__.__name__)
        self.label = self.options.get("label", self.ident)
        self.start_events = self.options.get("start", [])
        self.start_events += ["request_" + self.ident]
        self.events = []
        self.stop_events = self.options.get("stop", [])
        self.stop_events += ["cancel_" + self.ident]
        self.toggle_events = ["toggle_" + self.ident]

        p.events.all(self.start_events, self.activate)
        p.events.all(self.toggle_events, self.toggle)

    def setup(self):
        pass

    def set_layer(self, layer):
        self._layer = layer

    def get_layer(self):
        return self._layer

    def _activate(self):
        pass

    def start(self):
        pass

    def activate(self):
        p.events.none(self.start_events, self.activate)
        p.events.all(self.stop_events, self.deactivate)
        for event in self.events:
            if event[0] not in ("active", "inactive", "open", "closed"):
                p.events.on(event[0], event[1])
        self.active = True
        self._activate()
        self.start()
        p.events.trigger(self.ident + "_started")
        p.modes += [self]
        p.events.trigger("mode", self.ident, "activate", self)

    def _deactivate(self):
        pass

    def stop(self):
        pass

    def deactivate(self):
        p.events.none(self.stop_events, self.deactivate)
        p.events.all(self.start_events, self.activate)
        for event in self.events:
            if event[0] not in ("active", "inactive", "open", "closed"):
                p.events.off(event[0], event[1])
        self.active = False
        self._deactivate()
        self.stop()
        p.events.trigger(self.ident + "_stopped")
        if self in p.modes:
            p.modes.remove(self)
        p.events.trigger("mode", self.ident, "deactivate", self)

    def toggle(self):
        if self.active:
            self.deactivate()
        else:
            self.activate()

    def delay(self, *args, **kwags):
        pass

    def cancel_delayed(self, *args, **kwargs):
        pass

    def serialize(self):
        return {
            "id": self.ident,
            "label": self.label,
            "priority": self.priority
        }
