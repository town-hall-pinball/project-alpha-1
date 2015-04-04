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

import pinproc
from pinlib import p, util

class Device(object):

    def __init__(self, hardware, driver):
        self.hardware = hardware
        self.driver = driver
        self.id = driver.json_number
        self.name = driver.name
        self.number = driver.number
        self.label = driver.label
        self.category = driver.category
        self.tags = driver.tags

class Driver(Device):

    default_pulse = 30

    def __init__(self, hardware, driver):
        super(Driver, self).__init__(hardware, driver)
        self.state = { "schedule": "disable" }
        self.timer = None
        self.blink_on = None

    def disable(self):
        state = { "schedule": "disable" }
        if self.state != state:
            self.state = state
            p.events.trigger(self.hardware, self, state)
            self.driver.disable()

    def enable(self):
        state = { "schedule": "enable" }
        if self.state != state:
            self.state = state
            p.events.trigger(self.hardware, self, state)
            self.driver.enable()
            #self.driver.schedule(0xffffffff)
            #self.driver.schedule(0xffffffff, 0, True)

    def pulse(self, duration=None, delay=None):
        duration = duration if duration else self.default_pulse
        state = {
            "schedule": "pulse",
            "duration": duration
        }
        if delay:
            state["delay"] = delay
        self.state = state
        p.events.trigger(self.hardware, self, state)
        if delay:
            self.driver.future_pulse(duration, delay)
        else:
            self.driver.pulse(duration)

    def patter(self, on=127, off=None, initial=0, now=True):
        if not off:
            off = on
        state = {
            "schedule": "patter",
            "on": on,
            "off": off
        }
        if initial:
            state["initial"] = initial
        if now != True:
            state["now"] = now
        if self.state != state:
            self.state = state
            p.events.trigger(self.hardware, self, state)
            if on <= 127 and off <= 127:
                self.driver.patter(on, off, initial, now)
            else:
                self.blink_on = False
                self.update_blink()

    def update_blink(self):
        self.cancel_blink()
        if self.state["schedule"] != "patter":
            return
        elif self.state["on"] <= 127 and self.state["off"] < 127:
            return
        else:
            self.blink_on = not self.blink_on
            if self.blink_on:
                self.driver.enable()
                self.timer = p.timers.set(self.state["on"] / 1000,
                        self.update_blink)
            else:
                self.driver.disable()
                self.timer = p.timers.set(self.state["off"] / 1000,
                        self.update_blink)

    def cancel_blink(self):
        p.timers.clear(self.timer)
        self.timer = None

    def pulsed_patter(self, on=10, off=10, run=0, now=True):
        state = {
            "schedule": "pulsed_patter",
            "on": on,
            "off": off,
            "run": run
        }
        if now != True:
            state["now"] = now
        self.state = state
        p.events.trigger(self.hardware, self, state)
        self.driver.pulsed_patter(on, off, run, now)

    def schedule(self, schedule):
        state = {
            "schedule": schedule,
        }
        if self.state != state:
            self.state = state
            p.events.trigger(self.hardware, self, state)
            self.driver.schedule(schedule)

    def serialize(self):
        return util.dict_merge({
            "hardware": self.hardware,
            "name": self.name,
            "id": self.id,
            "label": self.label
        }, self.state)


class Switch(Device):

    def __init__(self, hardware, driver):
        super(Switch, self).__init__(hardware, driver)
        self.type = driver.type
        self.opto = driver.type == "NC"

    def is_active(self, seconds=None):
        return self.driver.is_active(seconds)

    def is_inactive(self, seconds=None):
        return self.driver.is_inactive(seconds)

    def is_open(self, seconds=None):
        return self.driver.is_open(seconds)

    def is_closed(self, seconds=None):
        return self.driver.is_closed(seconds)

    def activate(self, active=True):
        if not active:
            self.deactivate()
        elif self.opto:
            self.open()
        else:
            self.close()

    def deactivate(self):
        if self.opto:
            self.close()
        else:
            self.open()

    def close(self):
        #if self.is_closed():
        #    return
        value = pinproc.decode("wpc", self.id) # FIXME: Hard-coded to WPC
        p.commands.put({
            "command": "switch",
            "type": pinproc.EventTypeSwitchClosedDebounced,
            "value": value
        })

    def open(self):
        #if self.is_open():
        #    return
        value = pinproc.decode("wpc", self.id) # FIXME: Hard-coded to WPC
        p.commands.put({
            "command": "switch",
            "type": pinproc.EventTypeSwitchOpenDebounced,
            "value": value
        })

    def serialize(self):
        return {
            "hardware": self.hardware,
            "name": self.name,
            "id": self.id,
            "label": self.label,
            "active" :self.driver.is_active(),
            "open": self.driver.is_open(),
            "opto": self.opto,
            "schedule": "enable" if self.driver.is_active() else "disable"
        }

class DeviceCollection(object):

    def __init__(self, hardware):
        self.hardware = hardware
        self.names = {}
        self.ids = {}
        self.numbers = {}
        self.tags = {}

    def add(self, device):
        self.names[device.name] = device
        self.ids[device.id] = device
        self.numbers[device.number] = device
        for tag in device.tags:
            if tag not in self.tags:
                self.tags[tag] = []
            self.tags[tag] += [device]

    def get(self, it, optional=False):
        if it in self.names:
            return self.names[it]
        if it in self.ids:
            return self.ids[it]
        if it in self.numbers:
            return self.numbers[it]
        if not optional:
            raise LookupError("No such {}: {}".format(self.hardware, it))
        return None

    def serialize(self):
        items = {}
        for name, item in self.names.items():
            items[name] = item.serialize()
        return items


class Flippers(object):

    def __init__(self, proc):
        self.hardware = "flippers"
        self.id = "flippers"
        self.name = "flippers"
        self.label = "Enable Flippers"
        self.proc = proc
        self.enabled = False

    def enable(self, value=True):
        self.enabled = value
        state = "enable" if value else "disable"
        p.events.trigger("flippers", self, {
            "state": state
        })
        self.proc.enable_flippers(value)

    def disable(self):
        self.enabled = False
        p.events.trigger("flippers", self, {
            "state": "disable"
        })
        self.proc.enable_flippers(False)

    def serialize(self):
        return {
            "hardware": self.hardware,
            "id": self.id,
            "label": self.label,
            "active": self.enabled,
            "open": not self.enabled
        }


class Machine(object):

    def __init__(self, config, proc):
        self.config = config
        self.proc = proc
        self.devices = {}

        self.devices["lamps"] = DeviceCollection("lamp")
        for lamp in self.proc.lamps:
            self.devices["lamps"].add(Driver("lamp", lamp))

        self.devices["coils"] = DeviceCollection("coil")
        self.devices["flashers"] = DeviceCollection("flasher")
        for coil in self.proc.coils:
            if "flasher" in coil.tags:
                self.devices["flashers"].add(Driver("flasher", coil))
            else:
                self.devices["coils"].add(Driver("coil", coil))

        self.devices["switches"] = DeviceCollection("switch")
        for switch in self.proc.switches:
            self.devices["switches"].add(Switch("switch", switch))

        self.devices["flippers"] = Flippers(proc)

    def collection(self, hardware, name=None, fn=None):
        items = None
        if name:
            items = self.devices[hardware].tags.get(name, None)
            if not items:
                raise LookupError("No such tag: " + name)
        else:
            items = self.devices[hardware].names.values()
        if fn:
            map(fn, items)
        return items

    def lamp(self, name, optional=False):
        return self.devices["lamps"].get(name, optional)

    def lamps(self, name=None, fn=None):
        return self.collection("lamps", name, fn)

    def coil(self, name, optional=False):
        return self.devices["coils"].get(name, optional)

    def coils(self, name=None, fn=None):
        return self.collection("coils", name, fn)

    def flasher(self, name, optional=False):
        return self.devices["flashers"].get(name, optional)

    def flashers(self, name=None, fn=None):
        return self.collection("flashers", name, fn)

    def switch(self, name, optional=False):
        return self.devices["switches"].get(name, optional)

    def switches(self, name=None, fn=None):
        return self.collection("switches", name, fn)

    def flippers(self):
        return self.devices["flippers"]

    def serialize(self):
        return {
            "lamps": self.devices["lamps"].serialize(),
            "coils": self.devices["coils"].serialize(),
            "flashers": self.devices["flashers"].serialize(),
            "switches": self.devices["switches"].serialize(),
            "rules": {
                "flippers": self.devices["flippers"].serialize()
            }
        }
