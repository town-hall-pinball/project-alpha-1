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

from pinlib import devices, util

class Machine(object):
    """
    TODO
    """

    def __init__(self, config, **options):
        self.config = config
        virtual = options.get("virtual", False)
        controller_class_name = config.get("controller/class_name")
        controller_class = util.load_class(controller_class_name)
        self.controller = controller_class(config, virtual)
        self.numbers = {}
        self.devices = {}
        self.switches = []
        self.coils = []
        self.service = self.default_service

    def _create_devices(self, key, factory):
        for name, spec in self.config.get(key).items():
            device = factory(self.controller, name, spec)
            if device.number in self.numbers:
                raise ValueError("Device {} already exists when adding {}"
                        .format(numbers[device.number].id, device.id))
            self.devices[device.id] = device
            types = getattr(self, key)
            types += [device]

    def start(self):
        """
        TODO
        """
        self.controller.reset()

        device_types = (
            ("coils", devices.Coil),
            ("switches", devices.Switch)
        )
        for device_type, factory in device_types:
            self._create_devices(device_type, factory)

        for switch in self.switches:
            switch.enable()

        self.controller.start()
        self.run()

    def device(self, ident):
        """
        TODO
        """
        try:
            return self.devices[ident]
        except KeyError as ke:
            raise KeyError("No such device: {}".format(name))

    def default_service(self):
        """
        TODO
        """
        self.controller.service()

    def run(self):
        """
        TODO
        """
        done = False
        while not done:
            done = self.service()

