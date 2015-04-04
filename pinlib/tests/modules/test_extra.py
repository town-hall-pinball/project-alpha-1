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

import unittest
from tests import fixtures
from mock import MagicMock
from pinlib import p, mock
from pinlib.modules import extra

class TestSwichSequence(unittest.TestCase):

    def setUp(self):
        fixtures.init()
        self.success = MagicMock()
        self.switches = {
            "up":       mock.Switch("up"),
            "down":     mock.Switch("down"),
            "left":     mock.Switch("left"),
            "right":    mock.Switch("right"),
            "a":        mock.Switch("a"),
            "b":        mock.Switch("b"),
            "start":    mock.Switch("start")
        }
        self.watcher = extra.SwitchSequenceWatcher({
            "sequence": [
                "up",
                "up",
                "down",
                "down",
                "left",
                "right",
                "left",
                "right",
                "b",
                "a"
            ],
            "event_name": "success",
            "timeout": 5000
        })
        p.events.on("success", self.success)
        self.watcher.activate()

    def tearDown(self):
        self.watcher.deactivate()

    def test_success(self):
        """
        Does the easter egg sequence trigger?
        """
        for name in self.watcher.sequence:
            p.events.trigger("switch", self.switches[name], "active")
        self.assertTrue(self.success.called)
        self.assertFalse(self.watcher.active)

    def test_failure(self):
        """
        Is the sequence not triggered when it is incorrect?
        """
        sequence = list(self.watcher.sequence)
        sequence.insert(len(sequence) - 2, "start")
        for name in sequence:
            p.events.trigger("switch", self.switches[name], "active")
        self.assertFalse(self.success.called)
        self.assertTrue(self.watcher.active)

    def test_restart(self):
        """
        Does the easter egg sequence trigger after a false start?
        """
        sequence = ["up", "up", "down", "up"] + self.watcher.sequence
        for name in sequence:
            p.events.trigger("switch", self.switches[name], "active")
        self.assertTrue(self.success.called)

    def test_timeout(self):
        """
        Does the sequence timeout if enough time elapses between switches?
        """
        sequence1 = self.watcher.sequence[:4]
        sequence2 = self.watcher.sequence[4:]
        for name in sequence1:
            p.events.trigger("switch", self.switches[name], "active")
        p.timers.service(6000)
        for name in sequence2:
            p.events.trigger("switch", self.switches[name], "active")
        self.assertFalse(self.success.called)
        self.assertTrue(self.watcher.active)

    def test_not_timeout(self):
        """
        Does the sequence still work after a pause that didn't timeout?
        """
        sequence1 = self.watcher.sequence[:4]
        sequence2 = self.watcher.sequence[4:]
        for name in sequence1:
            p.events.trigger("switch", self.switches[name], "active")
        p.timers.service(4000)
        for name in sequence2:
            p.events.trigger("switch", self.switches[name], "active")
        self.assertTrue(self.success.called)
        self.assertFalse(self.watcher.active)
