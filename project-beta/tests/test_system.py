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
from mock import Mock, mock_open, patch
import unittest

from pinlib import system

class TestLoadConfig(unittest.TestCase):

    @patch("os.walk")
    def test_load(self, os_walk):
        contents = '{"a": 1}'
        _open = mock_open(read_data=contents)
        with patch("pinlib.system.open", _open, create=True):
            path = ("foo", ["d1"], ["f1.json"])
            os_walk.return_value = iter([path])
            config = system.load_config()
            self.assertEquals(1, config.get("a"))

    @nose.tools.raises(system.ConfigurationError)
    @patch("os.walk")
    def test_load_error(self, os_walk):
        contents = '{xxxx}'
        _open = mock_open(read_data=contents)
        with patch("pinlib.system.open", _open, create=True):
            path = ("foo", ["d1"], ["f1.json"])
            os_walk.return_value = iter([path])
            config = system.load_config()



