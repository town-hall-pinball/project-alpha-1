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

import dpath

class Configuration(object):
    """
    TODO
    """

    def __init__(self, config=None):
        self.config = config if config else {}

    def get(self, path, default=None):
        """
        TODO
        """
        try:
            print "******* GET: ", path
            value = dpath.get(self.config, path)
            return Configuration(value) if isinstance(value, dict) else value
        except KeyError:
            if default is not None:
                return default
            raise ConfigurationError("Configuration requires a value for {}"
                    .format(path))

    def subset(self, path, default=None):
        """
        TODO
        """
        value = self.get(path, default)
        return Configuration(value) if isinstance(value, dict) else value

    def items(self):
        print "ITEMS"
        items = []
        for key in self.config:
            items += [[key, self.get(key)]]
        return items

    def __repr__(self):
        return repr(self.config)


class ConfigurationError(Exception):
    """
    Exception raised when a configuration value is missing or has an
    incorrect value.
    """

