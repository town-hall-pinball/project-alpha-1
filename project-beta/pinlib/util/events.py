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

import traceback

__all__ = ["Events", "ListenerError"]

class Events(object):
    """
    Handler that registers listeners and triggers events. A system-wide handler
    for `pinlib` can be found in TODO.

    Example::

        def hello():
            print "Hello world"

        events = util.Events()
        events.on("hello", hello)
        events.trigger("hello")
    """

    def __init__(self):
        self.listeners = {}

    def on(self, event, listener):
        """
        Register the function `listener` to be called when an `event` is
        triggered. Any additional `*args` and `**kwargs` passed when triggering
        the event are passed to the `listener`
        """
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event] += [listener]

    def all(self, events, listener):
        """
        Register the function `listener` to be called when any event in the
        `events` list is triggered. Any additional `*args` and `**kwargs`
        passed when triggering the event are passed to the `listener`
        """
        for event in events:
            self.on(event, listener)

    def off(self, event, listener):
        """
        Unregisters `listener` from being called when an `event` is triggered.
        If the `listener` has not been registered, this method does nothing.
        """
        if event in self.listeners:
            if listener in self.listeners[event]:
                self.listeners[event].remove(listener)

    def none(self, events, listener):
        """
        Unregisteres `listener` from being called when any event in the
        `events` list is triggered. If the `listener` has not been registered,
        this method does nothing.
        """
        for event in events:
            self.off(event, listener)

    def trigger(self, event, *args, **kwargs):
        """
        Triggers `event` to all registered listeners. Each listener is called
        with `*args` and `**kwargs`
        """
        # Copy list in case it is mutated during triggering
        listeners = list(self.listeners.get(event, []))
        for listener in listeners:
            try:
                listener(*args, **kwargs)
            except ListenerError as le:
                raise
            except Exception as e:
                message = "Error dispatching {} to {}: {}\n{}".format(
                    event, listener, e, traceback.format_exc())
                raise ListenerError(message)

    def clear(self):
        """
        Unregisters all listeners.
        """
        self.listeners.clear()


class ListenerError(Exception):
    "Exception raised when there is an error dispatching an event"


