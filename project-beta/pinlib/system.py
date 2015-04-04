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

import os
import json

import dpath

from .machine import Machine
from . import util


def start():
    config = load_config()
    machine = Machine(config, virtual=True)
    machine.start()

def load_config(directory="config"):
    """
    Returns a dictionary with the contents of all JSON files found
    in the specified `directory`. Raises a configuration error if the
    directory is not found, a file is not readable, or a file cannot be
    parsed.
    """
    config = {}
    for root, directories, files in os.walk(directory):
        for file in files:
            base, ext = os.path.splitext(file)
            if ext == ".json":
                fragment = _load_config_file(os.path.join(root, file))
                dpath.merge(config, fragment)
    return util.Configuration(config)


def _load_config_file(file):
    try:
        with open(file) as fp:
            return json.load(fp)
    except Exception as e:
        raise ConfigurationError("Unable to load {}: {}".format(file, str(e)))


class ConfigurationError(Exception):
    """
    Exception raised when there is an error loading the configuration.
    """


