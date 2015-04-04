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
from pinlib.dmd import ui

class Table(ui.ScriptPanel):

    def __init__(self):
        super(Table, self).__init__({ "opaque": True })
        self.entries = []

    def update_table(self):
        for i in xrange(len(self.entries)):
            name = p.data["highscores"][i][0]
            score = p.data["highscores"][i][1]
            self.entries[i]["name"].show(name)
            self.entries[i]["score"].show("${:,d}".format(score))


class ClassicTable(Table):

    def __init__(self):
        super(ClassicTable, self).__init__()
        lines = []
        for i in xrange(5):
            name = ui.Text({"font": "medium_bold"})
            score = ui.Text({"font": "medium_bold", "x_align": "right"})
            self.entries += [{
                "name": name,
                "score": score
            }]
            lines += [self.line(i, name, score)]

        panel_gc = ui.ColumnPanel()
        panel_gc.add(ui.Text({
            "font": "medium_bold",
            "text": "Grand Champion",
            "margin": [2, 0]
        }))
        panel_gc.add(lines[0])

        panel_hs = ui.Message("Highest Scores")
        panel_hs1 = ui.ColumnPanel().add(lines[1]).add(lines[2])
        panel_hs2 = ui.ColumnPanel().add(lines[3]).add(lines[4])

        self.add(panel_gc, 3.0)
        self.add(panel_hs, 3.0)
        self.add(panel_hs1, 3.0)
        self.add(panel_hs2, 3.0)

        p.events.on("save", self.update_table)
        self.update_table()

    def line(self, place, name, score):
        panel = ui.RowPanel({
            "name": "line:",
            "left": 2,
            "right": 2,
            "margin": [2, 0]
        })
        if place > 0:
            panel.add(ui.Text({
                "font": "medium_bold",
                "text": str(place) + ". "
            }))
        panel.add(name)
        panel.add(score)
        return panel


class ModernTable(Table):

    places = [
        "Grand Champion",
        "First Place",
        "Second Place",
        "Third Place",
        "Fourth Place"
    ]

    def __init__(self):
        super(ModernTable, self).__init__()
        for i in xrange(5):
            name = ui.Text({"font": "medium_bold" })
            score = ui.Text({"margin_top": 1, "font": "medium" })
            self.entries += [{
                "name": name,
                "score": score
            }]
            panel = ui.ColumnPanel().add(
                ui.Text({
                    "margin_bottom": 2,
                    "text": self.places[i]
                })
            ).add(name).add(score)
            self.add(panel, 3.0)

        p.events.on("save", self.update_table)
        self.update_table()
