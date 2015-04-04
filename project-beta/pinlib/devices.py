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

class Device(object):
    """
    TODO: Base class for devices
    """

    def __init__(self, controller, type_, types, name, config):
        self.controller = controller
        self.type = type_
        self.types = types

        print self.types, config
        map_key = "map/{}/{}".format(self.types, config.get("device"))
        self.number = self.controller.config.get(map_key)

        self.name = name
        self.id = self.type + ":" + self.name
        self.label = config.get("label", self.name)

    def __unicode__(self):
        return self.name


class Driver(Device):
    """
    TODO: Base class for drivers
    """
    def __init__(self, controller, type_, types, name, config):
        super(Driver, self).__init__(controller, type_, types, name, config)


class Coil(Driver):
    """
    TODO: Coil
    """
    def __init__(self, controller, name, config):
        super(Coil, self).__init__(controller, "coil", "coils", name, config)


class Lamp(Driver):
    """
    TODO: Lamp
    """
    def __init__(self, controller, name, config):
        super(Lamp, self).__init__(controller, "lamp", "lamps", name, config)


class Flasher(Driver):
    """
    TODO: Flasher
    """
    def __init__(self, controller, name, config):
        super(Flasher, self).__init__(controller, "flasher", "flashers", name,
                config)


class Switch(Device):
    """
    TODO: Switch
    """
    def __init__(self, controller, name, config):
        super(Switch, self).__init__(controller, "switch", "switches", name,
                config)
        self.debounce = controller.requires_debouncing(self.number)

    def enable(self, value=True):
        """
        Registers this switch to send events when opened or closed. Disables
        events if `value` is `False`
        """
        self.controller.enable_switch(self, value)

    def disable(self):
        """
        Unregisters this switch to no longer send events when opened or closed.
        """
        self.enable(False)







