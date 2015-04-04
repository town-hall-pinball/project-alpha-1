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

import logging
from logging import handlers
import sys
import traceback
from pinlib import p
from pinlib import brand

__level = logging.INFO
__root = None

__device_map = {
    "switch":   "switch",
    "lamp":     "lamp",
    "flasher":  "flash",
    "coil":     "coil",
    "flippers": "rule"
}

def init():
    global __level, __root
    if p.options["verbose"]:
        __level = logging.DEBUG

    log_file = "var/{}.log".format(brand.prog)
    date_format = "%Y-%m-%d %H:%M:%S"
    log_format = "%(asctime)s [%(levelname)s]: %(message)s"
    logger = get()
    logger.setLevel(__level)

    formatter = logging.Formatter(log_format, date_format)
    file_handler = handlers.WatchedFileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if p.options["console"]:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.info("{}, Version {}, {}".format(brand.name, brand.version,
            brand.release))
    if p.options["verbose"]:
        logger.info("Debug logging enabled")
    __root = logger

    if p.options["events"]:
        p.events.on("switch", log_machine_event)
        p.events.on("lamp", log_machine_event)
        p.events.on("flasher", log_machine_event)
        p.events.on("coil", log_machine_event)
        p.events.on("flippers", log_machine_event)

def log_machine_event(device, options=None):
    hardware = device.hardware
    state = options["schedule"] if "schedule" in options else options["state"]
    marker = "-" if state == "disable" else "+"
    suffix = ""
    if state not in ("enable", "disable"):
        str_options = str(options) if options else ""
        suffix = str_options
    debug("{:6} {} {} {}".format(__device_map[hardware], marker, device.name,
            suffix))

def get(subname=None):
    name = brand.prog
    if subname:
        name = name + "." + subname
    logger = logging.getLogger(name)
    return logger

def exception(*args, **kwargs):
    if __root:
        __root.exception(*args, **kwargs)
    else:
        sys.stderr.write("Unexpected error\n")
        sys.stderr.write(traceback.format_exc())

def critical(*args, **kwargs):
    __root.critical(*args, **kwargs)

def error(*args, **kwargs):
    __root.error(*args, **kwargs)

def warning(*args, **kwargs):
    __root.warning(*args, **kwargs)

def info(*args, **kwargs):
    if __root:
        __root.info(*args, **kwargs)

def debug(*args, **kwargs):
    if __root:
        __root.debug(*args, **kwargs)

def notify(message, category="game"):
    debug(message)
    p.events.trigger("notify", {
        "text": message,
        "type": category
    })
