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

import time
from pinlib import p, mode, util
from pinlib.dmd import ui

def init():
    p.load_mode(SystemMode,         { "start": ["reset"] })
    #p.load_mode("pinlib.core.DefaultMode",     { "start": ["reset"] })
    p.load_mode(CatchAllMode, { "start": ["reset"] })


class CatchAllMode(mode.Base):

    defaults = {
        "id": "catch_all",
        "label": "Catch All",
        "priority": 1000
    }

    def __init__(self, options):
        super(CatchAllMode, self).__init__(options)

    def setup(self):
        self.root = (ui.Message()
            .add("This page intentionally", font="small_narrow_full")
            .add("left blank", font="small_narrow_full"))
        self.display(self.root)


class DefaultMode(mode.Base):

    def __init__(self, options):
        options["id"] = "Default"
        super(DefaultMode, self).__init__(options, priority=9)

    def sw_serviceEnter_active(self, sw=None):
        p.events.trigger("request-service-menu")

    def sw_serviceExit_active(self, sw=None):
        p.events.trigger("request_service_credit")


class SystemMode(mode.Base):

    defaults = {
        "id": "system",
        "label": "System",
        "priority": 3990
    }

    def __init__(self, options):
        super(SystemMode, self).__init__(options)

    def start(self):
        p.machine.lamps("gi", lambda lamp: lamp.enable())
        for sw in p.switches:
            self.add_switch_handler(sw.name, "active", None,
                    handler=self.trigger_switch_active)
            self.add_switch_handler(sw.name, "inactive", None,
                    handler=self.trigger_switch_inactive)

    def trigger_switch_active(self, sw):
        p.events.trigger("switch", p.machine.switch(sw.name), {
            "state": "active",
            "schedule": "enable"
        })

    def trigger_switch_inactive(self, sw):
        p.events.trigger("switch", p.machine.switch(sw.name), {
            "state": "inactive",
            "schedule": "disable"
        })

    def mode_tick(self):
        p.now = time.time()
        p.timers.service(p.now)
