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

from pinlib import p, mode, util
from pinlib.modules import extra
from pinlib.dmd import ui

def init():
    p.load_mode(SequenceWatchMode, {
        "start": ["attract_started"],
        "stop":  ["attract_stopped"]
    })
    p.load_mode("mm3.ee.StageSelectMode",   { "start": ["stage-select"] })
    p.load_mode("mm3.ee.GameStartMode", {})

class SequenceWatchMode(extra.SwitchSequenceWatcher):

    defaults = {
        "id": "mm3_trigger",
        "label": "MM3 Trigger",
        "priority": 1810,
        "event_name": "request_mm3_stage_select",
        "sequence": [
            "flipperLeft",
            "flipperLeft",
            "flipperLeft",
            "flipperRight",
            "flipperRight",
            "flipperRight",
            "flipperLeft",
            "flipperRight"
        ]
    }

    def __init__(self, options):
        super(SequenceWatchMode, self).__init__(options)


class StageSelectMode(mode.Base):

    defaults = {
        "id": "mm3_stage_select",
        "label": "MM3 Stage Select",
        "priority": 1300
    }

    bosses = [
        ( "mm3/spark_man",  "Spark Man" ),
        ( "mm3/snake_man",  "Snake Man" ),
        ( "mm3/needle_man", "Needle Man" ),
        ( "mm3/hard_man",   "Hard Man" ),
        ( "mm3/top_man",    "Top Man" ),
        ( "mm3/gemini_man", "Gemini Man" ),
        ( "mm3/magnet_man", "Magnet Man" ),
        ( "mm3/shadow_man", "Shadow Man" )
    ]

    def __init__(self, options):
        super(StageSelectMode, self).__init__(options)

    def setup(self):
        self.iter = util.CycleIterator(self.bosses)
        self.root = ui.Panel()
        self.image = ui.Image({
            "left": 0
        })
        self.info = ui.ColumnPanel({
            "left": 32,
            "right": 0
        })
        select = ui.Text({
            "text": "Flippers to Select",
            "font": "small_narrow_full",
            "margin_bottom": 5
        })
        self.push_start = ui.Text({
            "text": "Push Start",
            "font": "medium_bold"
        })
        self.info.add(select).add(self.push_start)

        self.root.add(self.image)
        self.root.add(self.info)
        self.update_boss()
        self.update_boss()
        self.set_layer(self.root)

    def start(self):
        p.events.trigger("cancel_attract")
        p.sounds.play_music("mm3/stage_select")
        self.push_start.update_style({"color": 0xf})
        anim = TearAnimator(self.root).complete(self.animation_end).start()
        self.set_layer(anim)

    def stop(self):
        self.push_start.stop_effects()

    def animation_end(self):
        self.set_layer(self.root)
        self.push_start.effect("pulse")

    def update_boss(self):
        boss = self.iter.get()
        self.image.update_style({"image": boss[0]})

    def sw_flipperRight_active(self, sw=None):
        self.iter.next()
        p.sounds.play("mm3/select")
        self.update_boss()

    def sw_flipperLeft_active(self, sw=None):
        self.iter.previous()
        p.sounds.play("mm3/select")
        self.update_boss()

    def sw_startButton_active(self, sw=None):
        p.sounds.stop_music()
        p.events.trigger("mm3-game-start", self.iter.get(), self.root)
        self.deactivate()
        return True


class GameStartMode(mode.Base):

    defaults = {
        "id": "mm3_game_start",
        "label": "MM3 Game Start",
        "priority": 1300
    }

    boss = None
    previous = None

    def __init__(self, options):
        super(GameStartMode, self).__init__(options)

    def setup(self):
        self.root = ui.Panel()
        self.background = ui.Image({
            "left": 0,
            "image": "mm3/background"
        })
        self.text_container = ui.Rectangle({
            "left": 0,
            "height": 14,
            "fill": 0,
            "composite": "sub",
            "enabled": False
        })
        self.image = ui.Image({
            "left": 10,
            "padding": [0, 2],
            "fill": 0,
            "enabled": False
        })
        self.name = ui.Text({
            "font": "medium_bold",
            "text_align": "center",
            "margin_top": 1,
            "left": 10 + 38,
            "right": 0
        })
        self.root.add(self.background)
        self.root.add(self.text_container)
        self.root.add(self.image)
        self.root.add(self.name)
        p.events.on("mm3-game-start", self.request_start)

    def request_start(self, boss, previous):
        self.boss = boss
        self.previous = previous
        self.activate()

    def start(self):
        self.image.enabled = False
        self.text_container.enabled = False
        self.text_container.update_style({"fill": 0})
        self.name.disable()
        p.sounds.play_music("mm3/game_start")
        anim = TearAnimator(self.root, self.previous)
        anim.start()
        self.set_layer(anim)
        p.timers.set(1.75, self.tear_end)
        p.timers.set(8.0, self.deactivate)

    def stop(self):
        p.sounds.play_music(self.boss[0])
        p.events.trigger("request_attract")

    def tear_end(self):
        self.set_layer(self.root)
        self.image.update_style({"image": self.boss[0]})
        self.image.enabled = True
        p.timers.set(1.5, self.blend_out)
        p.timers.set(3.25, self.set_name)

    def blend_out(self):
        self.text_container.enabled = True
        blend_out = BlendAnimator(self.text_container, "out")
        blend_out.start()

    def set_name(self):
        TextAnimator(self.name, self.boss[1]).start()

    def sw_startButton_active(self, sw=None):
        return True


class TearAnimator(ui.Animator):

    def __init__(self, target, source=None):
        target.invalidate()
        target.revalidate()
        super(TearAnimator, self).__init__(target.style, interval=1/30.0)
        self.progress = 0
        self.target = target
        self.source = source

    def update(self):
        self.invalidate()
        self.progress += 6
        if self.progress >= self.target.width:
            self.progress = self.target.width
            self.stop()

    def draw(self):
        super(TearAnimator, self).draw()
        width = self.target.width
        height = self.target.height
        mid = height / 2
        p.device.copy_rect(self.frame, width - self.progress, 0,
                self.target.frame, 0, 0, width, mid)
        p.device.copy_rect(self.frame, -width + self.progress, mid,
                self.target.frame, 0, mid, width, mid)
        if self.source:
            p.device.copy_rect(self.frame, -self.progress, 0,
                    self.source.frame, 0, 0, width, mid)
            p.device.copy_rect(self.frame, self.progress, mid,
                    self.source.frame, 0, mid, width, mid)


class BlendAnimator(ui.Animator):

    def __init__(self, target, direction="out"):
        target.invalidate()
        target.revalidate()
        super(BlendAnimator, self).__init__(target.style, interval=1/10.0)
        self.progress = 0 if direction == "out" else 0xf
        self.direction = direction
        self.target = target

    def update(self):
        self.progress += 1 if self.direction == "out" else -1
        if self.progress >= 0xf:
            self.progress = 0xf
            self.stop()
        if self.progress <= 0:
            self.progress = 0
            self.stop()
        self.target.update_style({"fill": self.progress})
        self.invalidate()

    def draw(self):
        self.target.draw()
        self.frame = self.target.frame


class TextAnimator(ui.Animator):

    def __init__(self, target, name):
        super(TextAnimator, self).__init__({}, interval=1/10.0)
        self.progress = 0
        self.name = name
        self.target = target

    def update(self):
        self.progress += 1
        if self.progress >= len(self.name):
            self.progress = len(self.name)
            self.stop()
        self.target.show(self.name[:self.progress])

    def draw(self):
        self.target.draw()
        self.frame = self.target.frame
