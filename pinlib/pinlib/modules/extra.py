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

import sys
from pinlib import p, mode

class SwitchSequenceWatcher(mode.Base):
    """
    Mode that monitors for a certain switch sequence which is useful for easter
    eggs. If the specified sequence is received without a timeout, an event
    is fired.

    The `options` argument contains a dictionary with the following:

    sequence
        Required. The sequence of switch names to watch
    event_name
        The name of the event fired when the sequence is detected. Defaults
        to "sequence"
    priority
        The priority of this mode. Defaults to `sys.maxint`
    timeout
        Cancel the current sequence if this many milliseconds elapses
        between switch hits. Defaults to 10 seconds.
    """

    def __init__(self, options):
        priority = options.get("priority", sys.maxint)
        super(SwitchSequenceWatcher, self).__init__(options)
        self.sequence = self.options["sequence"]
        self.event_name = self.options.get("event_name", "sequence")
        self.index = 0
        self.timeout = self.options.get("timeout", 10000)
        self.timer = None

    def start(self):
        p.events.on("switch", self.update)
        self.index = 0

    def stop(self):
        p.events.off("switch", self.update)

    def update(self, sw, options):
        if options["state"] != "active":
            return
        p.timers.clear(self.timer)
        if sw.name != self.sequence[self.index]:
            self.index = 0
            return
        self.index += 1
        if self.index == len(self.sequence):
            self.deactivate()
            p.events.trigger(self.event_name)
            return
        p.timers.set(self.timeout, self.cancel)

    def cancel(self):
        p.timers.clear(self.timer)
        self.index = 0
