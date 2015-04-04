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

import nose
import unittest

from pinlib import util

class TestConfig(unittest.TestCase):

    config = None

    def setUp(self):
        self.config = util.Configuration({
            "one": 1,
            "second": {
                "two": 2,
                "third": {
                    "three": 3
                }
            }
        })

    def test_get(self):
        self.assertEquals(3, self.config.get("second/third/three"))

    def test_get_default(self):
        self.assertEquals(10, self.config.get("second/ten", 10))

    @nose.tools.raises(util.ConfigurationError)
    def test_get_required(self):
        self.config.get("second/ten")

    def test_subset(self):
        sub = self.config.subset("second")
        self.assertEquals(3, sub.get("third/three"))




