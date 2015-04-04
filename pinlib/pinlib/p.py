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
import time
from importlib import import_module
from Queue import Queue
from pinlib import mock, util

locale.setlocale(locale.LC_ALL, '')

class Balls(object):

    free = 0
    held = 0
    trough = 0
    total = 0

animations = {}
balls = Balls()
commands = Queue()
data = {}
defaults = {}
desktop = None
display = mock.DMD128x32x16()
events = util.Events()
extensions = []
fonts = {}
features = {}
game = None
images = {}
machine = None
modes = []
options = {}
player = None
procgame = None
state = None
switches = {}
threads = mock.Threads()
now = time.time()
sounds = mock.Sound()
timers = util.Timers(time.time())
using = []

def set_defaults(kv):
    for key, value in kv.items():
        defaults[key] = defaults.get(key, value)
        data[key] = data.get(key, value)

def save():
    events.trigger("save")

def activate(mode):
    pass

def deactivate(mode):
    pass

def load_module(name):
    module = import_module(name)
    if hasattr(module, "init"):
        module.init()

def load_mode(class_name, options=None):
    pass
