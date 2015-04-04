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

from pinlib import p
from procgame import sound

class SoundController(sound.SoundController):

    active_music = None

    def play_music(self, key, loops=0, start_time=0.0):
        if not self.enabled:
            return
        p.events.trigger("audio", "music", key, "enable")
        super(SoundController, self).play_music(key, loops, start_time)
        self.active_music = key

    def stop_music(self):
        if not self.enabled or not self.active_music:
            return
        p.events.trigger("audio", "music", self.active_music, "disable")
        super(SoundController, self).stop_music()
        self.active_music = None

    def play(self, key, loops=0, max_time=0, fade_ms=0):
        if not self.enabled:
            return
        p.events.trigger("audio", "sound", key, "enable")
        super(SoundController, self).play(key, loops, max_time, fade_ms)

    def stop(self, key, loops=0, max_time=0, fade_ms=0):
        if not self.enabled:
            return
        p.events.trigger("audio", "sound", key, "disable")
        super(SoundController, self).stop(key, loops, max_time, fade_ms)
