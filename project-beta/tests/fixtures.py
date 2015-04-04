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

import pinlib
from pinlib import util

config_proc_wpc = util.Configuration({
    "map": {
        "switches": {
            "13": 34
        },
        "coils": {
            "2": 41
        }
    },
    "controller": {
        "class_name": "pinlib.controllers.PROC",
    },
    "platform": {
        "type": "wpc",
        "polarity": False
    },
    "switches": {
        "startButton": {
            "label": "Start Button",
            "device": "13"
        }
    },
    "coils": {
        "autoPlunger": {
            "label": "Auto Plunger",
            "device": "2",
        }
    }
})

def null_service(*args, **kwargs):
    return True

machine_proc_wpc = pinlib.Machine(config_proc_wpc, virtual=True)
machine_proc_wpc.service = null_service


