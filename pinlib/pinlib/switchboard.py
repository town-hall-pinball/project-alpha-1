from Tkinter import *
import pinproc
import os, json
from pinlib import p

CONFIG_PATH = 'config/machine.json'
BUTTON_WIDTH = 15

class Window(Frame):

    def get_config(self):
        self.json_data = {}
        try:
            with open(CONFIG_PATH) as data_file:
                self.json_data = json.load(data_file)
        except Exception as e:
            print 'Error in get_config: ', str(e)

    def load_trigger(self, button, value):
        code = value.get('number')

        value = pinproc.decode("wpc", code)
        opto = p.switches[code].type == "NC"

        if button['bg'] == 'red':
            button['activebackground'] = 'green'
            button['bg'] = 'green'
            event = (pinproc.EventTypeSwitchOpenDebounced if not opto
                    else pinproc.EventTypeSwitchClosedDebounced)
            self.desktop.trigger({
                "type": event,
                "value": pinproc.decode('wpc', code)
            })
        else:
            button['activebackground'] = 'red'
            button['bg'] = 'red'
            event = (pinproc.EventTypeSwitchClosedDebounced if not opto
                    else pinproc.EventTypeSwitchOpenDebounced)
            self.desktop.trigger({
                "type": event,
                "value": pinproc.decode('wpc', code)
            })

    def create_button(self, value, position):
        new_button = Button(self, width = BUTTON_WIDTH)
        if 'type' in value:
            new_button ["text"] = value.get('name')
            new_button['activebackground'] = 'red'
            new_button['bg'] = 'red'
        else:
            new_button ["text"] = value.get('name')
            new_button['activebackground'] = 'green'
            new_button['bg'] = 'green'
        new_button ["command"] = lambda:self.load_trigger(new_button, value)
        new_button.grid(row = position[0], column = position[1])

    #auto generates all the PR switches in the machine.json file
    def all_prswitches(self):
        i, j = 0, 0

        switches = self.json_data.get('PRSwitches')
        for key in sorted(switches.iterkeys()):
            value = switches.get(key)
            if 'unused' not in value:
                if 'name' in value:
                    name = value.get("name")
                else:
                    name = key
                code = value.get("number")
                self.create_button(value, [i, j])
                i += 1
            if i % 18 == 0:
                i = 0
                j += 1

    def __init__(self, desktop, master=None):
        Frame.__init__(self, master)
        self.get_config()
        self.desktop = desktop
        self.grid()
        self.all_prswitches()
