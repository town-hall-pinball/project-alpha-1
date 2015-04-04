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

__all__ = ["PROC"]

from .base import Controller

_EVENT_DMD_READY = 5

class PROC(Controller):

    def __init__(self, config, virtual=False):
        super(PROC, self).__init__()
        self.config = config
        self.type = config.get("platform/type")
        self.polarity = config.get("platform/polarity")

        if virtual:
            self.api = _Virtual()
        else:
            self.api = __import__("pinproc").PinPROC(self.type)

    def reset(self):
        self.api.reset(1)

    def start(self):
        self.refresh_displays()

    def requires_debouncing(self, switch_number):
        return switch_number < 192

    def enable_switch(self, switch, enable=True):
        if switch.debounce:
            events = ["closed_debounced", "open_debounced"]
        else:
            events = ["closed_nondebounced", "open_nondebounced"]

        for event in events:
            self.api.switch_update_rule(switch.number, event, {
                "notifyHost": enable,
                "reloadActive": False
            }, [], False)

    def disable_switch(self, switch):
        self.enable_swich(self, switch, False)

    def controller_events(self):
        return self.api.get_events()

    def keep_alive(self):
        self.api.watchdog_tickle()

    def flush(self):
        self.api.flush()

    def service(self):
        for event in self.events():
            event_type = event["type"]
            if event_type == _EVENT_DMD_READY:
                self.refresh_displays()


class _Virtual(Controller):

    def __init__(self, *args, **kwargs):
        super(_Virtual, self).__init__()

    def reset(*args, **kwargs):
        pass

    def switch_update_rule(*args, **kwargs):
        pass

    def watchdog_tickle(self):
        pass

    def flush(self):
        pass




