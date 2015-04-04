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

import json
from pinlib import p, mode, util
from pinlib.dmd import ui, effects
from pinlib.modules import menu

priority = 3210

def init():
    p.set_defaults({
        "debug.alignment_grid": False
    })

    p.load_mode(TriggerMode)
    p.load_mode(ServiceMode)
    p.load_mode(SwitchTestMode)
    p.load_mode(CoilTestMode)
    p.load_mode(LampTestAllMode)
    p.load_mode(FlasherTestAllMode)
    p.load_mode(MusicBrowserMode)
    p.load_mode(SoundBrowserMode)
    p.load_mode(FontBrowserMode)
    p.load_mode(AnimationBrowserMode)

    #p.load_mode("pinlib.modules.service.AlignmentGridMode", {
    #    "toggle": ["alignment-grid-toggle"]
    #})


class TriggerMode(mode.Base):

    defaults = {
        "id": "service_trigger",
        "label": "Service Mode Trigger",
        "priority": 3800,
        "start": ["reset", "service_stopped"],
        "stop": ["service_started"]
     }

    def setup(self):
        self.events = [
            ["active", "serviceEnter", self.service_mode]
        ]

    def service_mode(self, sw=None):
        p.events.trigger("request_service")
        return True


class ServiceMode(menu.Tree):

    defaults = {
        "id": "service",
        "label": "Service Mode",
        "priority": priority
    }

    def __init__(self, options):
        with open("config/service_menu.json") as fp:
            root = json.load(fp)
        super(ServiceMode, self).__init__(options, root=root)

    def start(self):
        super(ServiceMode, self).start()
        p.sounds.stop_music()

    def sw_serviceEnter_active(self, sw=None):
        self.select()
        return True

    def sw_serviceExit_active(self, sw=None):
        self.exit()
        return True

    def sw_serviceUp_active(self, sw=None):
        self.next()
        return True

    def sw_serviceDown_active(self, sw=None):
        self.previous()
        return True


class SwitchTestMode(mode.Base):

    defaults = {
        "id": "service_switch_test",
        "label": "Switch Test",
        "priority": priority + 1
    }

    def setup(self):
        self.panel = ui.Panel()
        self.canvas = ui.Canvas({
            "left": 0,
            "top": 0,
            "width": 40,
        })
        col_panel = ui.ColumnPanel({
            "left": 40,
            "width": p.device.WIDTH - 40,
        })
        col_panel.add(ui.Text({
            "text": "Switch Edges",
            "margin_bottom": 8,
        }))
        self.name = ui.Text({
            "text": "Hit switch to start",
            "font": "small_narrow_full"
        })
        col_panel.add(self.name)

        self.panel.add(self.canvas)
        self.panel.add(col_panel)
        self.set_layer(self.panel)

        for sw in p.switches:
            self.add_switch_handler(sw.name, "active", None,
                    handler=self.update_switch_change)
            self.add_switch_handler(sw.name, "inactive", None,
                    handler=self.update_switch_change)

    def start(self):
        self.update_switches()

    def dot_column(self, x, prefix):
        y = 5
        row = 1
        for y in xrange(5, 5 + (8 * 3), 3):
            ident = prefix + str(row)
            switch = p.machine.switch(ident, optional=True)
            if switch and switch.category != "unused":
                if switch.is_closed():
                    self.canvas.box(x - 1, y - 1, 3, 3)
                else:
                    self.canvas.dot(x, y)
            row += 1

    def update_switches(self, sw=None):
        if sw:
            self.name.show(sw.label, duration=5)
        self.canvas.clear()
        self.dot_column(2, "SD")
        self.canvas.vline(5, 2, p.device.HEIGHT - 4, color=4)
        col = 1
        for x in xrange(8, 8 + (8 * 3), 3):
            self.dot_column(x, "S" + str(col))
            col += 1
        x += 3
        self.canvas.vline(x, 2, p.device.HEIGHT - 3, color=4)
        x += 3
        self.dot_column(x, "SF")
        self.canvas.draw()
        return True

    def update_switch_change(self, sw=None):
        if sw.name != "serviceExit":
            p.sounds.play("service/switch_edge")
        self.update_switches(sw)
        return True

    def sw_serviceExit_active(self, sw=None):
        p.sounds.play("menu/exit")
        self.deactivate()


class CoilTestMode(mode.Base):

    defaults = {
        "id": "service_coil_test",
        "label": "Coil Test",
        "priority": priority + 1
    }

    def setup(self):
        self.root = ui.Panel()
        self.test_name = ui.Text({
            "top": 1,
            "font": "small_wide",
            "text": "Coils"
        })
        self.coil_name = ui.Text({
            "font": "medium_bold"
        })
        self.status = ui.Text({
            "bottom": 1,
            "padding": [1, 2],
            "fill": 4
        })
        self.root.add(self.test_name)
        self.root.add(self.coil_name)
        self.root.add(self.status)
        self.set_layer(self.root)

        all_coils = p.machine.coils()
        testing_coils = []
        for coil in all_coils:
            if coil.category != "unused" and "flipper" not in coil.tags:
                testing_coils += [coil]
        self.coils = util.CycleIterator(testing_coils)

    def start(self):
        self.machine.lamp("buttonStart").enable()
        self.update()

    def stop(self):
        self.machine.lamp("buttonStart").disable()

    def sw_serviceUp_active(self, sw=None):
        self.coils.next()
        self.update()
        return True

    def sw_serviceDown_active(self, sw=None):
        self.coils.previous()
        self.update()
        return True

    def sw_serviceEnter_active(self, sw=None):
        self.pulse()
        return True

    def sw_startButton_active(self, sw=None):
        self.pulse()
        return True

    def pulse(self):
        self.coils.get().pulse(100)
        self.status.show("Pulse", 0.5)

    def update(self):
        coil = self.coils.get()
        self.coil_name.show(coil.label)

    def sw_serviceExit_active(self, sw=None):
        p.sounds.play("menu/exit")
        self.deactivate()
        return True


class LampTestAllMode(mode.Base):

    defaults = {
        "id": "service_lamp_test_all",
        "label": "Lamp Test: All",
        "priority": priority + 1
    }

    def setup(self):
        self.root = ui.Panel()
        self.test_name = ui.Text({
            "top": 1,
            "font": "small_wide",
            "text": "Lamps"
        })
        self.mode_name = ui.Text({
            "font": "medium_bold"
        })
        self.status = ui.Text({
            "bottom": 1,
            "padding": [1, 2],
            "fill": 4
        })
        self.root.add(self.test_name)
        self.root.add(self.mode_name)
        self.root.add(self.status)
        self.set_layer(self.root)

        all_lamps = p.machine.lamps()
        self.lamps = []
        for lamp in all_lamps:
            if "gi" not in lamp.tags:
                self.lamps += [lamp]
        #self.lamps = self.lamps[:10]
        #0print "***** LAMPS ", str(len(self.lamps))
        self.modes = util.CycleIterator(["On", "Blink", "Off"])

    def start(self):
        self.update()

    def stop(self):
        self.off()

    def sw_serviceUp_active(self, sw=None):
        self.modes.next()
        self.update()
        return True

    def sw_serviceDown_active(self, sw=None):
        self.modes.previous()
        self.update()
        return True

    def sw_serviceExit_active(self, sw=None):
        p.sounds.play("menu/exit")
        self.deactivate()
        return True

    def update(self):
        mode = self.modes.get()
        self.mode_name.show(mode)
        if mode == "On":
            self.on()
        if mode == "Off":
            self.off()
        if mode == "Blink":
            self.blink()

    def on(self):
        map(lambda lamp: lamp.enable(), self.lamps)

    def off(self):
        map(lambda lamp: lamp.disable(), self.lamps)

    def blink(self):
        map(lambda lamp: lamp.patter(), self.lamps)


class FlasherTestAllMode(mode.Base):

    defaults = {
        "id": "service_flasher_test_all",
        "label": "Flasher Test: All",
        "priority": priority + 1
    }

    def setup(self):
        self.root = ui.Panel()
        self.test_name = ui.Text({
            "top": 1,
            "font": "small_wide",
            "text": "Flashers"
        })
        self.mode_name = ui.Text({
            "font": "medium_bold"
        })
        self.status = ui.Text({
            "bottom": 1,
            "padding": [1, 2],
            "fill": 4
        })
        self.root.add(self.test_name)
        self.root.add(self.mode_name)
        self.root.add(self.status)
        self.set_layer(self.root)

        all_flashers = p.machine.flashers()
        self.flashers = []
        for flasher in all_flashers:
            # Nothing to filter yet?
            self.flashers += [flasher]
        self.modes = util.CycleIterator(["Blink", "Off"])

    def start(self):
        self.update()

    def stop(self):
        self.off()

    def sw_serviceUp_active(self, sw=None):
        self.modes.next()
        self.update()
        return True

    def sw_serviceDown_active(self, sw=None):
        self.modes.previous()
        self.update()
        return True

    def sw_serviceExit_active(self, sw=None):
        p.sounds.play("menu/exit")
        self.deactivate()
        return True

    def update(self):
        mode = self.modes.get()
        self.mode_name.show(mode)
        if mode == "Off":
            self.off()
        if mode == "Blink":
            self.blink()

    def off(self):
        map(lambda flasher: flasher.disable(), self.flashers)

    """
    def blink(self):
        map(lambda flasher: flasher.schedule(0x10000000), self.flashers)
    """


class MusicBrowserMode(mode.Base):

    defaults = {
        "id": "service_music_browser",
        "label": "Music Browser",
        "priority": priority + 1
    }

    def setup(self):
        self.music = util.CycleIterator(sorted(p.sounds.music.keys()))
        panel = ui.Panel({"opqaue": False})
        self.name = ui.Text({
            "top": 0,
            "font": "small_narrow_full"
        })
        panel.add(self.name)
        self.set_layer(panel)

    def start(self):
        self.update_music()

    def stop(self):
        p.sounds.stop_music()

    def update_music(self):
        music_name = self.music.get()
        self.name.show(music_name)
        p.sounds.play_music(music_name)

    def sw_serviceEnter_active(self, sw=None):
        self.update_music()
        return True

    def sw_serviceUp_active(self, sw=None):
        p.sounds.play("menu/next")
        self.music.next()
        self.update_music()
        return True

    def sw_serviceDown_active(self, sw=None):
        p.sounds.play("menu/previous")
        self.music.previous()
        self.update_music()
        return True

    def sw_serviceExit_active(self, sw=None):
        p.sounds.play("menu/exit")
        self.deactivate()
        return True


class SoundBrowserMode(mode.Base):

    defaults = {
        "id": "service_sound_browser",
        "label": "Sound Browser",
        "priority": priority + 1
    }

    def setup(self):
        self.sounds = util.CycleIterator(sorted(p.sounds.sounds.keys()))
        panel = ui.Panel({"opqaue": False})
        self.name = ui.Text({
            "top": 0,
            "font": "small_narrow_full"
        })
        panel.add(self.name)
        self.last_sound = None
        self.set_layer(panel)

    def start(self):
        self.update_sound()

    def stop(self):
        if self.last_sound:
            p.sounds.stop(self.last_sound)

    def update_sound(self):
        sound_name = self.sounds.get()
        self.name.show(sound_name)
        if self.last_sound:
            p.sounds.stop(self.last_sound)
        self.last_sound = sound_name
        p.sounds.play(sound_name)

    def sw_serviceEnter_active(self, sw=None):
        self.update_sound()
        return True

    def sw_serviceUp_active(self, sw=None):
        self.sounds.next()
        self.update_sound()
        return True

    def sw_serviceDown_active(self, sw=None):
        self.sounds.previous()
        self.update_sound()
        return True

    def sw_serviceExit_active(self, sw=None):
        p.sounds.play("menu/exit")
        self.deactivate()
        return True


class FontBrowserMode(mode.Base):

    defaults = {
        "id": "service_font_browser",
        "label": "Font Browser",
        "priority": priority + 1
    }

    def setup(self):
        self.fonts = util.CycleIterator(sorted(p.fonts.keys()))
        self.sample = ""
        panel = ui.Panel()
        self.name = ui.Text({
            "top": 0,
            "font": "small_narrow_full",
        })
        self.text = ui.Text({
            "bottom": 2,
            "fill": 4
        })
        panel.add(self.name)
        panel.add(self.text)
        self.set_layer(panel)

        self.scroll = effects.Animation({
            "interval": 0.05,
            "delay": 0.2,
            "update": self.update_chars
        })
        self.direction = None

    def start(self):
        self.update_font()

    def update_font(self):
        font_name = self.fonts.get()
        font = p.fonts[font_name]
        self.sample = "".join(font.chars())
        self.name.show(font_name)
        self.text.update_style({
            "text": self.sample,
            "font": self.fonts.get()
        })

    def update_chars(self):
        if self.direction == "right":
            self.sample = self.sample[1:] + self.sample[0]
        else:
            self.sample = self.sample[-1:] + self.sample[:-1]
        self.text.show(self.sample)

    def sw_serviceEnter_active(self, sw=None):
        return True

    def sw_serviceUp_active(self, sw=None):
        p.sounds.play("menu/next")
        self.fonts.next()
        self.update_font()
        return True

    def sw_serviceDown_active(self, sw=None):
        p.sounds.play("menu/previous")
        self.fonts.previous()
        self.update_font()
        return True

    def sw_flipperRight_active(self, sw=None):
        self.direction = "right"
        self.update_chars()
        self.scroll.start()
        return True

    def sw_flipperRight_inactive(self, sw=None):
        self.scroll.stop()
        return True

    def sw_flipperLeft_active(self, sw=None):
        self.direction = "left"
        self.update_chars()
        self.scroll.start()
        return True

    def sw_flipperLeft_inactive(self, sw=None):
        self.scroll.stop()
        return True

    def sw_serviceExit_active(self, sw=None):
        p.sounds.play("menu/exit")
        self.deactivate()
        self.scroll.stop()
        return True


class AnimationBrowserMode(mode.Base):

    defaults = {
        "id": "service_animation_browser",
        "label": "Animation Browser",
        "priority": priority + 1
    }

    def setup(self):
        self.animations = util.CycleIterator(sorted(p.animations.keys()))
        self.animation = ui.Animation()
        panel = ui.Panel()
        self.name = ui.Text({
            "top": 0,
            "font": "small_narrow_full",
        })
        panel.add(self.animation)
        panel.add(self.name)
        self.set_layer(panel)

    def start(self):
        self.update_animation()

    def update_animation(self):
        animation_name = self.animations.get()
        self.name.show(animation_name, 2.0)
        self.animation.set_animation(animation_name)
        self.animation.start()

    def sw_serviceEnter_active(self, sw=None):
        return True

    def sw_serviceUp_active(self, sw=None):
        p.sounds.play("menu/next")
        self.animations.next()
        self.update_animation()
        return True

    def sw_serviceDown_active(self, sw=None):
        p.sounds.play("menu/previous")
        self.animations.previous()
        self.update_animation()
        return True

    def sw_serviceEnter_active(self, sw=None):
        self.update_animation()
        return True

    def sw_serviceExit_active(self, sw=None):
        p.sounds.play("menu/exit")
        self.deactivate()
        return True


class AlignmentGridMode(mode.Base):

    def __init__(self, options):
        super(AlignmentGridMode, self).__init__(options, priority + 10)

    def setup(self):
        self.canvas = ui.Canvas({
            "fill": 2,
            "composite": "add"
        })
        width = p.device.WIDTH
        height = p.device.HEIGHT
        for x in xrange(0, width, 8):
            self.canvas.vline(x, 0, height, color=6)
        for y in xrange(0, height, 8):
            self.canvas.hline(0, y, width, color=6)
        self.canvas.vline(0, 0, height)
        self.canvas.vline(width - 1, 0, height)
        self.canvas.hline(0, 0, width)
        self.canvas.hline(0, height - 1, width)
        self.canvas.draw()
        self.set_layer(self.canvas)

        p.events.on("reset", self.reset)

    def reset(self):
        if p.data["debug.alignment_grid"]:
            self.activate()
