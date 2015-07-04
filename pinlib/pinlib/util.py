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

"""
Utilities.
"""

from copy import deepcopy
import fractions
import locale
import signal
import time


class ListenerException(Exception):
    pass

class Events(object):
    """
    Handler that registers listeners and triggers events. A system-wide handler
    for `pinlib` can be found in p.events

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
        if not listener:
            raise ValueError("No listener specified")
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
            except ListenerException as le:
                raise
            except Exception as e:
                message = "Error dispatching {} to {}: {}".format(
                    event, listener, e)
                raise ListenerException(message)

    def clear(self):
        """
        Unregisters all listeners.
        """
        self.listeners.clear()


class CycleIterator(object):
    """
    Iterator that cycles through the list of `items`. When at the last element,
    calling :meth:`next` goes to the first element. When at the first element,
    calling :meth:`previous` goes to the last element.

    Example::

        >>> iter = util.CycleIterator([1,2,3])
        >>> print iter.get()
        1
        >>> iter.next()
        >>> iter.next()
        >>> print iter.get()
        3
        >>> iter.next()
        >>> print iter.get()
        1
    """

    def __init__(self, items=None):
        self.items = items if items else []
        self.index = 0

    def get(self):
        """
        Returns the item at the iterator's current position.
        """
        return self.items[self.index]

    def next(self):
        """
        Moves the position to the next element in the list. If at the end of
        the list, goes to the first element.
        """
        self.index += 1
        if self.index >= len(self.items):
            self.index = 0
        return self.items[self.index]

    def previous(self):
        """
        Moves the position to the previous element in the list. If at the
        beginning of the list, goes to the last element.
        """
        self.index -= 1
        if self.index < 0:
            self.index = len(self.items) - 1
        return self.items[self.index]

    def add(self, item):
        """
        Adds an additonal `item` to the list.
        """
        self.items += [item]


class Timers(object):
    """
    Handler that services timers.
    """

    def __init__(self, now):
        self.id = 1
        self.active = {}
        self.tickers = {}
        self.now = now

    def next_id(self):
        self.id += 1
        return self.id

    def set(self, duration, callback):
        """
        Register `callback` to be invoked one time after `duration` seconds
        have elapsed. Returns an identifier that can be used to cancel this
        registration using :meth:`clear`.
        """
        ident = self.next_id()
        self.active[ident] = {
            "duration": duration,
            "end": self.now + duration,
            "callback": callback
        }
        return ident

    def defer(self, callback):
        self.set(0, callback)

    def tick(self, callback):
        """
        Register `callback` to be invoked each time the main loop runs. Returns
        an identifier that can be used to cancel this registration using
        :meth:`clear`.
        """
        ident = self.next_id()
        self.tickers[ident] = callback
        return ident

    def clear(self, ident):
        """
        Unregister a callback that was assigned with the identifier, `ident`
        """
        if ident in self.active:
            del self.active[ident]
        if ident in self.tickers:
            del self.tickers[ident]

    def service(self, now):
        """
        Immediately service all active timers with the current time of `now`
        """
        self.now = now
        if len(self.active) > 0:
            for ident, timer in self.active.items():
                if self.now > timer["end"] and ident in self.active:
                    del self.active[ident]
                    timer["callback"]()
        for ticker in self.tickers.values():
            ticker()


class Stopwatch(object):
    """
    Utility class for recording elapsed time.
    """

    def __init__(self):
        self.start = now()

    def elapsed(self):
        """
        Returns elapsed time, in seconds, since :meth:`elapsed` was last
        called, or the object was created.
        """
        elapsed = now() - self.start
        self.start = now()
        return elapsed

    def show(self, message):
        """
        Prints the `message` along with result of :meth:`elapsed` as
        milliseconds to two decimal points.
        """
        print message, "{:.2f}".format(self.elapsed() * 1000.0)


class NullContext(object):
    """
    Context manager that does nothing.
    """

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def now():
    """
    Returns the current time. This is the same as calling `time.time()`, but
    can be easily mocked.
    """
    return time.time()

def write(*args):
    """
    Prints out `*args` to the console. This is the same as calling `print`, but
    can be easily mocked.
    """
    print " ".join(args)

# dict_merge from
# http://blog.impressiver.com/post/31434674390/deep-merge-multiple-python-dicts
def dict_merge(target, *args):
    """
    Merges two dictionaries. From:

    http://blog.impressiver.com/post/31434674390/deep-merge-multiple-python-dicts

    Example::

        >>> a = { "foo": 1 }
        >>> b = { "bar": 2 }
        >>> util.dict_merge(a, b)
        { "foo": 1, "bar": 2 }
    """

    # Merge multiple dicts
    if len(args) > 1:
        for obj in args:
            dict_merge(target, obj)
        return target

    # Recursively merge dicts and set non-dict values
    obj = args[0]
    if not isinstance(obj, dict):
        return obj
    for k, v in obj.iteritems():
        if k in target and isinstance(target[k], dict):
            dict_merge(target[k], v)
        else:
            target[k] = deepcopy(v)
    return target


def fraction(value):
    """
    Converts the floating point `value` into a human-readable fraction.

    Example::

        >>> util.fraction(2)
        "2"
        >>> util.fraction(2.5)
        "2 1/2"
    """
    fraction = fractions.Fraction(value).limit_denominator(4)
    if fraction.numerator == 0:
        return "0"
    if fraction.numerator < fraction.denominator:
        return str(fraction.numerator) + "/" + str(fraction.denominator)
    whole = fraction.numerator / fraction.denominator
    if fraction.denominator == 1:
        return str(whole)
    numerator = fraction.numerator - (whole * fraction.denominator)
    return str(whole) + " " + str(numerator) + "/" + str(fraction.denominator)

def format_score(score):
    if score == 0:
        return "00"
    return locale.format("%d", score, True)

def for_name(name):
    """
    Using the string `name`, returns a reference to the object while importing
    the necessary modules. Similar to `Class.forName` in Java.
    """
    parts = name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

def to_list(v):
    """
    Converts the value, `v`, to a list if it is not a list, otherwise returns
    the existing list.

    Example::
        >>> util.to_list(1)
        [1]
        >>> util.to_list([1, 2])
        [1, 2]
    """
    return v if isinstance(v, list) else [v]

signal_names = {
    signal.SIGABRT: "SIGABRT",
    signal.SIGBUS:  "SIGBUS",
    signal.SIGSEGV: "SIGSEGV",
    signal.SIGTERM: "SIGTERM",
    signal.SIGQUIT: "SIGQUIT",
}
"""
A dictionary of signal number keys that map to signal names.
"""
