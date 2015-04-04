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

class Controller(object):
    """
    Base class for controlling pinball interfacing hardware.
    """

    artifical_events = None
    """
    List of artifical events to simulate switch activity.
    """

    displays = None
    """
    TODO.
    """

    def __init__(self):
        self.artifical_events = []
        self.displays = []

    def events(self):
        """
        Gets the list of events received from the controller. If events
        exist in :data:`artifical_events`, these are appended to the
        returned list and :data:`artifical_events` is cleared.
        """
        result = self.controller_events()
        if len(self.artifical_events) > 0:
            result += self.artifical_events
            del self.artifical_events[:]
        return self

    def refresh_displays(self):
        """
        TODO.
        Invoked by the main run loop when the display buffer is clear and
        is ready for another frame.
        """
        for display in self.displays:
            display.refresh()

    def reset(self):
        """
        TODO
        """

    def start(self):
        """
        TODO
        """

    def requires_debouncing(self, switch_number):
        """
        TODO
        """

    def enable_switch(self, switch, enable=True):
        """
        TODO
        """

    def disable_switch(self, switch):
        """
        TODO
        """

    def controller_events(self):
        """
        TODO
        """

    def keep_alive(self):
        """
        TODO
        """

    def flush(self):
        """
        TODO
        """

    def service(self):
        """
        TODO
        """



