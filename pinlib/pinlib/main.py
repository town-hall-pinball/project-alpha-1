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

# This section deals with setup that pyprocgame requires as a side-effect
# of importing modules
from procgame import config
config.values = {
    "font_path": ["resources/fonts"],
    "pinproc_class": "procgame.fakepinproc.FakePinPROC",
    "config_path": ["config"],
    "desktop_dmd_scale": 4,
    "dmd_cache_path": "tmp/cache",
    "display": False
}

import argparse
from copy import deepcopy
import json
import os
import re
import signal
import sys
import traceback

import pinproc
from pinlib import p, sound
from procgame import auxport, dmd
from procgame.game import Mode
from procgame.game.game import GameController
from pinlib import brand, log, machine, resources, util
from pinlib.dmd import displays

config_dir        = "config"
runtime_dir       = "var"
ext_dir           = "ext"
default_data_file = os.path.join(config_dir,  "default.json")
data_file         = os.path.join(runtime_dir, "data.json")
features_file     = os.path.join(config_dir,  "features.json")
machine_file      = os.path.join(config_dir,  "machine.json")

def init():
    parse_arguments()
    check_directories()
    log.init()
    load_config()
    install_extensions()
    bind()
    load_resources()
    load_data()
    if not p.options["proc"]:
        setup_fake_optos()
    load_features()
    install_signal_handlers()
    start_services()

def parse_arguments():
    parser = argparse.ArgumentParser(prog=brand.prog)
    parser.add_argument("-c", "--console", action="store_true", default=False,
        help="also print log file to console")
    parser.add_argument("-d", "--debug", action="store_true", default=False,
        help="enable all debugging options")
    parser.add_argument("--display", action="store_true", default=False,
        help="force debugging display when using the P-ROC")
    parser.add_argument("-e", "--events", action="store_true", default=False,
        help="show machine events to console")
    parser.add_argument("-p", "--proc", action="store_true", default=False,
        help="connect to the P-ROC")
    parser.add_argument("-q", "--quiet", action="store_true", default=False,
        help="do not use a log file")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
        help="print debugging information to the log")

    args = parser.parse_args()

    for key, value in vars(args).items():
        config.values[key] = value
    p.options = config.values

    if p.options["proc"]:
        del p.options["pinproc_class"]
    else:
        p.options["display"] = True

    if p.options["debug"]:
        p.options["console"] = True
        p.options["display"] = True
        p.options["verbose"] = True

def load_resources():
    resources.load("sounds")
    resources.load("images")
    resources.load("fonts")
    resources.load("music")
    resources.load("animations")

def load_config():
    with open(features_file) as fp:
        p.features = json.load(fp)

def install_extensions():
    if not os.path.isdir(ext_dir):
        return
    sys.path += [ext_dir]
    for ext in os.listdir(ext_dir):
        p.extensions += [ext]
        ext_features_file = os.path.join(ext_dir, ext, "config", "features.json")
        if os.path.exists(ext_features_file):
            with open(ext_features_file) as fp:
                ext_features = json.load(fp)
            if "modules" in ext_features:
                p.features["modules"] += ext_features["modules"]


def check_directories():
    if not os.path.isdir(config_dir):
        raise IOError("No configuration directory: {}".format(config_dir))
    if not os.path.isdir(runtime_dir):
        os.makedirs(runtime_dir)

def bind():
    p.sounds = sound.SoundController(None)
    p.save = save_data
    p.load_mode = load_mode
    p.activate = activate
    p.deactivate = deactivate
    p.device = displays.DMD128x32x16()

    with open(machine_file) as fp:
        machine_config = json.load(fp)
    map_keyboard(machine_config)
    p.procgame = Game(str(machine_config["PRGame"]["machineType"]))
    p.procgame.load_config(machine_file)
    p.machine = machine.Machine(machine_config, p.procgame)
    p.switches = p.procgame.switches

def load_features():
    p.load_module("pinlib.core")
    for module in p.features.get("modules", []):
        p.load_module(module)
    for mode_def in p.features.get("modes", []):
        p.load_mode(mode_def["name"], mode_def)
    p.load_module("pinlib.modules.simulator")

def setup_fake_optos():
    for switch in p.machine.switches():
        if switch.type == "NC":
            switch.driver.set_state(True)

def install_signal_handlers():
    signal.signal(signal.SIGABRT, signal_exit)
    signal.signal(signal.SIGBUS,  signal_exit)
    signal.signal(signal.SIGSEGV, signal_exit)
    signal.signal(signal.SIGTERM, signal_exit)
    signal.signal(signal.SIGQUIT, signal_exit)

def start_services():
    p.events.trigger("server-adjust")

def reset():
    p.events.trigger("reset")
    p.procgame.run_loop()

def run():
    exit_code = 0
    try:
        init()
        reset()
    except KeyboardInterrupt as ke:
        log.info("Exiting on console interrupt")
        pass
    except SystemExit as se:
        pass
    except Exception as e:
        log.exception("Exiting on unexpected error")
        exit_code = 1
    shutdown(exit_code)

def signal_exit(signal, frame):
    log.critical("Exiting on signal {} ({})".format(signal,
            util.signal_names.get(signal, "Unknown")))
    shutdown(1)

def shutdown(exit_code):
    if p.desktop:
        p.desktop.stop()
    #if p.threads.web:
    #    p.threads.web.stop()
    #    p.threads.web.join()
    log.info("Exited with return code {}".format(exit_code))
    os._exit(exit_code)

def load_data():
    with open(default_data_file) as fp:
        p.defaults = json.load(fp)
        p.data = deepcopy(p.defaults)
    if os.path.exists(data_file):
        with open(data_file) as fp:
            util.dict_merge(p.data, json.load(fp))

def save_data():
    directory = os.path.dirname(data_file)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    with open(data_file, "w") as fp:
        json.dump(p.data, fp)
    p.events.trigger("save")

def load_mode(klass, options=None):
    options = options if options else {}
    if isinstance(klass, basestring):
        klass = util.for_name(klass)
    instance = Adapter(p.procgame, klass(options))
    instance.init()
    p.using += [instance]

def activate(mode):
    adapter = Adapter(p.procgame, mode)
    adapter.target.activate()

def deactivate(mode):
    p.procgame.modes.remove(mode)

def map_keyboard(machine_config):
    keymap = {}
    for sw in machine_config["PRSwitches"]:
        swdef = machine_config["PRSwitches"][sw]
        if "keyboard" in swdef:
            keymap[swdef["keyboard"]] = swdef["id"]
    config.values["keyboard_switch_map"] = keymap


class Game(GameController):

    dmd = None
    alpha_display = None
    score_display = None
    aux_port = None
    desktop = None

    def __init__(self, machine_type):
        super(Game, self).__init__(machine_type)
        self.aux_port = auxport.AuxPort(self)
        if self.machine_type == pinproc.MachineTypeWPCAlphanumeric:
            self.alpha_display = alphanumeric.AlphanumericDisplay(self.aux_port)
        else:
            self.dmd = dmd.DisplayController(self, width=128, height=32)

        if p.options["display"]:
            from pinlib.debug import Desktop
            self.desktop = Desktop()
            p.desktop = self.desktop

        if self.dmd: self.dmd.frame_handlers.append(self.set_last_frame)

    def load_config(self, path):
        super(Game,self).load_config(path)

        # Setup the key mappings from the config.json.
        # We used to do this in __init__, but at that time the
        # configuration isn't loaded so we can't peek into self.switches.
        key_map_config = config.value_for_key_path(keypath='keyboard_switch_map', default={})
        if self.desktop:
            for k, v in key_map_config.items():
                switch_name = str(v)
                if self.switches.has_key(switch_name):
                    switch_number = self.switches[switch_name].number
                else:
                    switch_number = pinproc.decode(self.machine_type, switch_name)
                self.desktop.add_key_map(ord(str(k)), switch_number)

    def reset(self):
        """Calls super's reset and adds the :class:`ScoreDisplay` mode to the mode queue."""
        super(Game, self).reset()
        self.modes.add(self.score_display)

    def dmd_event(self):
        """Updates the DMD via :class:`DisplayController`."""
        if self.dmd: self.dmd.update()

    def tick(self):
        """Called once per run loop.
        Displays the last-received DMD frame on the desktop."""
        super(Game, self).tick()
        self.show_last_frame()

    def score(self, points):
        """Convenience method to add *points* to the current player."""
        p = self.current_player()
        p.score += points

    #
    # Support for showing the last DMD frame on the desktop.
    #
    #   Because showing each frame on the desktop can be pretty time-consuming,
    #   we show it only once per run loop cycle (via tick()), and only when there
    #   is a new frame (via last_frame).  By showing it this way (and not directly
    #   from DisplayController's frame_handlers), we allow the run loop to progress
    #   quickly without getting bogged down drawing the DMD on the desktop if a
    #   large number of DMD events arrive 'at once'.
    #

    last_frame = None

    def set_last_frame(self, frame):
        self.last_frame = frame

    def show_last_frame(self):
        if self.desktop and self.last_frame:
            self.desktop.draw(self.last_frame)
            self.last_frame = None

    def get_events(self):
        events = super(Game, self).get_events()
        if self.desktop:
            events.extend(self.desktop.get_events())
        if p.commands:
            c = []
            while not p.commands.empty():
                c += [p.commands.get_nowait()]
            events.extend(c)
        return events


class Adapter(Mode):

    def __init__(self, procgame, target):
        self.target = target
        self.game = procgame
        target.delay = self.delay
        target.cancel_delayed = self.cancel_delayed
        target.add_switch_handler = self.add_switch_handler
        target.adapter = True
        super(Adapter, self).__init__(procgame, target.priority)

        if hasattr(target, "mode_tick"):
            self.mode_tick = target.mode_tick

        def _set_layer(layer):
            self.layer = layer
        target.set_layer = _set_layer
        target.display = _set_layer
        if target._layer:
            self.layer = target._layer

        def _get_layer():
            return self.layer
        target.get_layer = _get_layer

        def _activate():
            self.game.modes.add(self)
        target._activate = _activate

        def _deactivate():
            self.game.modes.remove(self)
        target._deactivate = _deactivate

    def init(self):
        self.target.setup()
        for event in self.target.events:
            #print "EVENT", event
            if event[0] in ["active", "inactive", "open", "closed"]:
                event_type = event[0]
                name = event[1]
                handler = event[2]
                delay = event[3] if len(event) == 4 else None
                self.add_switch_handler(name, event_type, delay, handler)


    # Copied directly from pyprogame but changing self to target
    def _Mode__scan_switch_handlers(self):
        # Format: sw_popperL_open_for_200ms(self, sw):
        handler_func_re = re.compile('sw_(?P<name>[a-zA-Z0-9]+)_(?P<state>open|closed|active|inactive)(?P<after>_for_(?P<time>[0-9]+)(?P<units>ms|s))?')
        for item in dir(self.target):
            m = handler_func_re.match(item)
            if m == None:
                continue
            seconds = None
            if m.group('after') != None:
                seconds = float(m.group('time'))
                if m.group('units') == 'ms':
                    seconds /= 1000.0

            handler = getattr(self.target, item)

            switch_name = m.group('name')
            switch_state = m.group('state')

            if switch_name not in self.game.switches:
                raise ValueError, 'Unrecognized switch name %s in handler %s.%s().' % (switch_name, self.__class__.__name__, item)
            self.add_switch_handler(name=switch_name, event_type=switch_state, delay=seconds, handler=handler)

    def __unicode__(self):
        return self.target.__class__.__name__ + " " + str(self.target.priority)

    def __str__(self):
        return self.__unicode__()
