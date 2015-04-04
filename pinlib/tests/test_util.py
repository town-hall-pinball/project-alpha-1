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

import locale
import unittest

from mock import DEFAULT, patch, MagicMock

from pinlib import p, util

class TestEvents(unittest.TestCase):

    def setUp(self):
        self.events = util.Events()

    def test_on(self):
        listener = MagicMock()
        self.events.on("foo", listener)
        self.events.trigger("foo")
        self.assertTrue(listener.called)

    def test_all(self):
        listener = MagicMock()
        self.events.all(["foo", "bar"], listener)
        self.events.trigger("foo")
        self.events.trigger("bar")
        self.assertEquals(2, listener.call_count)

    def test_off(self):
        listener = MagicMock()
        self.events.on("foo", listener)
        self.events.off("foo", listener)
        self.events.trigger("foo")
        self.assertFalse(listener.called)

    def test_none(self):
        listener = MagicMock()
        self.events.all(["foo", "bar"], listener)
        self.events.none(["foo", "bar"], listener)
        self.events.trigger("foo")
        self.events.trigger("bar")
        self.assertFalse(listener.called)        

    def test_trigger_with_arguments(self):
        listener = MagicMock()
        self.events.on("foo", listener)
        self.events.trigger("foo", 1, foo="bar")
        listener.assert_called_with(1, foo="bar")

    def test_trigger_separate(self):
        foo_listener = MagicMock()
        bar_listener = MagicMock()
        self.events.on("foo", foo_listener)
        self.events.on("bar", bar_listener)
        self.events.trigger("foo", it="foo")
        self.events.trigger("bar", it="bar")
        foo_listener.assert_called_with(it="foo")
        bar_listener.assert_called_with(it="bar")

    def test_clear(self):
        foo_listener = MagicMock()
        bar_listener = MagicMock()
        self.events.on("foo", foo_listener)
        self.events.on("bar", bar_listener)
        self.events.clear()
        self.events.trigger("foo", it="foo")
        self.events.trigger("bar", it="bar")
        self.assertFalse(foo_listener.called)
        self.assertFalse(bar_listener.called)


class TestCycleIterator(unittest.TestCase):

    def setUp(self):
        self.items = [0, 1, 2]
        self.iter = util.CycleIterator(self.items)

    def test_starts_at_zero(self):
        self.assertEquals(0, self.iter.get())

    def test_next(self):
        self.assertEquals(1, self.iter.next())
        self.assertEquals(1, self.iter.get())

    def test_previous(self):
        self.iter.index = 2
        self.assertEquals(1, self.iter.previous())
        self.assertEquals(1, self.iter.get())

    def test_next_cycle(self):
        self.iter.index = 2
        self.assertEquals(0, self.iter.next())
        self.assertEquals(0, self.iter.get())

    def test_previous_cycle(self):
        self.iter.index = 0
        self.assertEquals(2, self.iter.previous())
        self.assertEquals(2, self.iter.get())


class TestTimers(unittest.TestCase):

    def setUp(self):
        self.timers = util.Timers(0)

    def test_set_called(self):
        callback = MagicMock()
        self.timers.set(1.0, callback)
        self.timers.service(2.0)
        self.assertTrue(callback.called)

    def test_set_not_called(self):
        callback = MagicMock()
        self.timers.set(1.0, callback)
        self.timers.service(0.5)
        self.assertFalse(callback.called)

    def test_set_not_called_twice(self):
        callback = MagicMock()
        self.timers.set(1.0, callback)
        self.timers.service(2.0)
        self.assertEquals(1, callback.call_count)
        self.timers.service(3.0)
        self.assertEquals(1, callback.call_count)

    def test_clear(self):
        callback = MagicMock()
        ident = self.timers.set(1.0, callback)
        self.timers.clear(ident)
        self.timers.service(2.0)
        self.assertFalse(callback.called)

    def test_tick(self):
        callback = MagicMock()
        self.timers.tick(callback)
        self.timers.service(0.1)
        self.timers.service(0.2)
        self.assertEquals(2, callback.call_count)


class TestStopwatch(unittest.TestCase):

    @patch("pinlib.util.now")
    def test_elapsed(self, now):
        now.return_value = 10
        sw = util.Stopwatch()
        now.return_value = 15
        self.assertEquals(5, sw.elapsed())
        now.return_value = 25
        self.assertEquals(10, sw.elapsed())


class TestDictMerge(unittest.TestCase):

    def test_simple(self):
        a = { "x": 1 }
        b = { "y": 2 }
        expected = { "x": 1, "y": 2 }
        self.assertEquals(expected, util.dict_merge(a, b))

    def test_deep(self):
        a = { "x": { "one": 1 } }
        b = { "x": { "two": 2 } }
        expected = { "x": { "one": 1, "two": 2 } }
        self.assertEquals(expected, util.dict_merge(a, b))


class TestUtilFunctions(unittest.TestCase):

    def tearDown(self):
        locale.setlocale(locale.LC_ALL, "")

    def test_fraction_0(self):
        self.assertEquals("0", util.fraction(0))

    def test_fraction_025(self):
        self.assertEquals("1/4", util.fraction(0.25))

    def test_fraction_1_3(self):
        self.assertEquals("1/3", util.fraction(1.0/3.0))

    def test_fraction_050(self):
        self.assertEquals("1/2", util.fraction(0.5))

    def test_fraction_075(self):
        self.assertEquals("3/4", util.fraction(0.75))

    def test_fraction_575(self):
        self.assertEquals("5 3/4", util.fraction(5.75))

    def test_to_list_single(self):
        self.assertEquals([1], util.to_list(1))

    def test_to_list_multiple(self):
        self.assertEquals([1, 2], util.to_list([1, 2]))
