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

import os
import re
from pinlib import p
from pinlib import log
from procgame import dmd, sound
from procgame.dmd import animation

logger = log.get("resources")

def font_loader(filename, key):
    logger.debug("Loading font: " + filename)
    p.fonts[key] = dmd.Font().load(filename)

def sound_loader(filename, key):
    logger.debug("Loading sound: " + filename)
    p.sounds.register_sound(key, filename)

def music_loader(filename, key):
    logger.debug("Registering music: " + filename)
    p.sounds.register_music(key, filename)

def image_loader(filename, key):
    logger.debug("Loading image: " + filename)
    p.images[key] = dmd.Animation().load(filename).frames[0]

def animation_loader(filename, key):
    logger.debug("Loading animation: " + filename)
    p.animations[key] = animation.Animation().load(filename)

type_map = {
    "fonts":      { "handler": font_loader,  "extensions": [".dmd"] },
    "sounds":     { "handler": sound_loader, "extensions": [".wav", ".ogg"] },
    "music":      { "handler": music_loader, "extensions": [".ogg", ".mp3"] },
    "images":     { "handler": image_loader, "extensions": [".dmd"] },
    "animations": { "handler": animation_loader, "extensions": [".dmd"] }
}

def load(resource_type):
    r = resource_type
    this_dir = os.path.dirname(__file__)
    load_directory(os.path.join(this_dir, "resources", r), r)
    load_directory(os.path.join("resources", r), r)
    for ext in p.extensions:
        load_directory(os.path.join("ext", ext, "resources", r), r)

def load_directory(directory, resource_type):
    for root, dirs, files in os.walk(directory):
        for file in files:
            base, ext = os.path.splitext(file)
            if ext not in type_map[resource_type]["extensions"]:
                continue
            key = re.sub(r".*/" + resource_type + "/", "",
                    os.path.join(root, file))
            key = re.sub(ext + "$", "", key)
            handler = type_map[resource_type]["handler"]
            handler(os.path.join(root, file), key)
