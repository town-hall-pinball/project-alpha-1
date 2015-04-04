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

from mock import Mock
import nose
import unittest

from pinlib import util

class TestEvents(unittest.TestCase):

    def setUp(self):
        self.events = util.Events()

    def test_on(self):
        listener = Mock()
        self.events.on("foo", listener)
        self.events.trigger("foo")
        self.assertTrue(listener.called)

    def test_all(self):
        listener = Mock()
        self.events.all(["foo", "bar"], listener)
        self.events.trigger("foo")
        self.events.trigger("bar")
        self.assertEquals(2, listener.call_count)

    def test_off(self):
        listener = Mock()
        self.events.on("foo", listener)
        self.events.off("foo", listener)
        self.events.trigger("foo")
        self.assertFalse(listener.called)

    def test_none(self):
        listener = Mock()
        self.events.all(["foo", "bar"], listener)
        self.events.none(["foo", "bar"], listener)
        self.events.trigger("foo")
        self.events.trigger("bar")
        self.assertFalse(listener.called)

    def test_trigger_with_arguments(self):
        listener = Mock()
        self.events.on("foo", listener)
        self.events.trigger("foo", 1, foo="bar")
        listener.assert_called_with(1, foo="bar")

    def test_trigger_separate(self):
        foo_listener = Mock()
        bar_listener = Mock()
        self.events.on("foo", foo_listener)
        self.events.on("bar", bar_listener)
        self.events.trigger("foo", it="foo")
        self.events.trigger("bar", it="bar")
        foo_listener.assert_called_with(it="foo")
        bar_listener.assert_called_with(it="bar")

    def test_clear(self):
        foo_listener = Mock()
        bar_listener = Mock()
        self.events.on("foo", foo_listener)
        self.events.on("bar", bar_listener)
        self.events.clear()
        self.events.trigger("foo", it="foo")
        self.events.trigger("bar", it="bar")
        self.assertFalse(foo_listener.called)
        self.assertFalse(bar_listener.called)

    @nose.tools.raises(util.ListenerError)
    def test_exception(self):
        listener = Mock(side_effect=Exception("error"))
        self.events.on("foo", listener)
        self.events.trigger("foo")

    @nose.tools.raises(util.ListenerError)
    def test_exception_no_reraise(self):
        listener = Mock(side_effect=util.ListenerError("error"))
        self.events.on("foo", listener)
        self.events.trigger("foo")


if __name__ == "__main__":
    unittest.main()

