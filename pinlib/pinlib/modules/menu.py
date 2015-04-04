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

from collections import deque
from pinlib import p, mode, util
from pinlib.dmd import ui

def option_tuple(option):
    if isinstance(option, list):
        value = option[0]
        text = option[1]
    else:
        value = option
        text = option
    return (value, text)

def text_for_value(options, search):
    for option in options:
        value, text = option_tuple(option)
        if search == value:
            return text

def index_for_value(options, search):
    index = 0
    for option in options:
        value, text = option_tuple(option)
        if search == value:
            return index
        index += 1


class MenuNode(object):

    def __init__(self, key, node):
        self.key = key
        self.node = node
        self.type = None
        if "options" in node:
            self.type = "edit"
            self.items = node["options"]
        else:
            item = node["menu"][0]
            if "icon" in item:
                self.type = "icon"
                self.items = node["menu"]
            elif "options" in item:
                self.type = "option"
                self.items = node["menu"]
            elif "data" in item:
                self.type = "value"
                self.items = node["menu"]
            else:
                self.type = "text"
                self.items = node["menu"]
        self.iter = util.CycleIterator(self.items)


class Confirm(mode.Base):

    def __init__(self, callback):
        super(Confirm, self).__init__({}, priority=1001)
        self.callback = callback
        self.value = False

        self.panel = ui.RowPanel({
            "align": "center",
            "bottom": 3
        })
        self.panel.add(ui.Text({
            "margin_right": 6,
            "text": "Confirm"
        }))
        self.yes = ui.Text({
            "padding": [0, 2],
            "margin_right": 3,
            "text": "Yes"
        })
        self.panel.add(self.yes)
        self.no = ui.Text({
            "padding": [0, 4],
            "text": "No"
        })
        self.panel.add(self.no)
        self.set_layer(self.panel)

    def start(self):
        p.sounds.play("menu/enter")
        self.value = False
        self.update()

    def sw_serviceUp_active(self, sw=None):
        self.toggle()
        return True

    def sw_serviceDown_active(self, sw=None):
        self.toggle()
        return True

    def sw_serviceEnter_active(self, sw=None):
        self.deactivate()
        self.callback(self.value)
        return True

    def sw_serviceExit_active(self, sw=None):
        self.deactivate()
        self.callback(False)
        return True

    def toggle(self):
        p.sounds.play("menu/next")
        self.value = not self.value
        self.update()

    def update(self):
        on = self.yes if self.value else self.no
        off = self.no if self.value else self.yes
        on.update_style({"fill": 0x5})
        off.update_style({"fill": None})


class Tree(mode.Base):

    def __init__(self, options, root):
        super(Tree, self).__init__(options)
        self.root = root
        self.menu = None
        self.menus = {}
        self.menu_stack = deque()
        self.key_stack = deque()
        self.depth = 0
        self.confirm = Confirm(self.confirm_result)

        self.breadcrumbs = ui.Text({
            "left": 2,
            "top": 1,
            "font": "small_narrow"
        })
        self.name = ui.Text({
            "top": 1
        })
        self.value = ui.Text({
            "top": 12,
            "padding": [0, 5],
        })
        self.icons = ui.RowPanel({
            "top": 11,
            "x_align": "center"
        })
        self.default = ui.Text({
            "bottom": 2,
            "right": 2,
            "font": "small_narrow_full"
        })
        self.result = ui.Text({
            "bottom": 3,
            "fill": 0x8,
            "enabled": False,
            "padding": [0, 3]
        })

        self.panel = ui.Panel()
        self.panel.add(self.breadcrumbs)
        self.panel.add(self.name)
        self.panel.add(self.icons)
        self.panel.add(self.value)
        self.panel.add(self.default)
        self.panel.add(self.result)
        self.set_layer(self.panel)

    def start(self):
        p.sounds.play("menu/enter")
        self.push_menu(self.root)

    def next(self):
        p.sounds.play("menu/next")
        self.menu.iter.next()
        self.update()

    def select(self):
        item = self.menu.iter.get()
        if not isinstance(item, list) and item.get("confirm", False):
            p.activate(self.confirm)
        elif self.menu.type == "edit":
            self.save()
        elif "menu" in item or "options" in item:
            p.sounds.play("menu/enter")
            self.push_menu(item)
        elif "event" in item:
            p.sounds.play("menu/enter")
            p.events.trigger(item["event"])

    def exit(self):
        p.sounds.play("menu/exit")
        self.pop_menu()

    def previous(self):
        p.sounds.play("menu/previous")
        self.menu.iter.previous()
        self.update()

    def push_menu(self, node):
        self.depth += 1
        self.key_stack += [node.get("name", "/")]
        key = "/".join(self.key_stack)
        if key in self.menus:
            self.menu = self.menus[key]
        else:
            self.menu = MenuNode(key, node)
            self.menus[key] = self.menu
        self.menu_stack += [self.menu]
        self.new_menu()

    def pop_menu(self):
        self.depth -= 1
        self.key_stack.pop()
        self.menu_stack.pop()
        if self.depth == 0:
            self.deactivate()
        else:
            self.menu = self.menu_stack[-1]
            self.new_menu()

    def new_menu(self):
        self.breadcrumbs.show("<" * self.depth)
        self.name.disable()
        self.value.disable()
        self.icons.clear()
        if self.menu.type == "icon":
            for item in self.menu.items:
                icon = ui.Image({
                    "image": item["icon"],
                    "margin": [0, 1],
                    "padding": [0, 1],
                })
                self.icons.add(icon)
        elif self.menu.type == "edit":
            options = self.menu.node["options"]
            key = self.menu.node["data"]
            self.menu.iter.index = index_for_value(options, p.data[key])
        self.update()

    def update(self):
        menu = self.menu
        selected = menu.iter.get()
        self.default.disable()
        self.value.update_style({"fill": None})

        if menu.type == "text":
            self.name.show(self.menu.node.get("name", ""))
            self.value.show(selected["name"])
        elif menu.type == "icon":
            self.name.show(selected["name"])
            for i in xrange(len(menu.items)):
                fill = 0xf if i == menu.iter.index else 0
                reverse = i == menu.iter.index
                self.icons.components[i].update_style({
                    "fill": fill,
                    "reverse": reverse
                })
        elif menu.type == "option":
            self.name.show(selected["name"])
            value = p.data[selected["data"]]
            default_value = p.defaults[selected["data"]]
            text = text_for_value(selected["options"], value)
            self.value.show(text)
            if value != None and value == default_value:
                self.default.show("Default")
        elif menu.type == "edit":
            self.name.show(menu.node["name"])
            value = selected[0]
            default_value = p.defaults[menu.node["data"]]
            self.value.show(selected[1])
            self.value.update_style({"fill": 0x4})
            if value != None and value == default_value:
                self.default.show("Default")
        elif menu.type == "value":
            self.name.show(selected["name"])
            value = p.data[selected["data"]]
            if "format" in selected:
                value = selected["format"].format(value)
            self.value.show(str(value))

    def save(self):
        item = self.menu.iter.get()
        key = self.menu.node["data"]
        value, text = option_tuple(item)
        self.result.enabled = True
        if value != p.data[key]:
            p.data[key] = value
            p.save()
            self.result.show("Saved", duration=1)
            p.sounds.play("menu/save")
            if "event" in self.menu.node:
                p.events.trigger(self.menu.node["event"])
        else:
            self.result.show("No Change", duration=1)
            p.sounds.play("menu/exit")
        self.pop_menu()

    def confirm_result(self, result):
        item = self.menu.iter.get()
        if result:
            p.events.trigger(item["event"])
            self.result.show("Confirmed", duration=1)
            p.sounds.play("menu/save")
        else:
            self.result.show("Canceled", duration=1)
            p.sounds.play("menu/exit")
