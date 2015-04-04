import threading
#from Tkinter import *
#from pinlib import switchboard
from procgame import desktop

class Desktop(desktop.Desktop):

    def __init__(self):
        self.events = []
        super(Desktop, self).__init__()
        #debug_gui = Thread(kwargs={"desktop": self})
        #debug_gui.desktop = self
        #debug_gui.start()

    def trigger(self, event):
        self.events += [event]

    def get_events(self):
        events = super(Desktop, self).get_keyboard_events()
        gui_events = self.events
        self.events = []
        gui_events.extend(events)
        #if len(gui_events) > 0:
        #    import sys
        #    sys.exit(0)
        return gui_events


#class Thread(threading.Thread):
#
#    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
#        super(Thread, self).__init__(group, target, name, args, kwargs)
#        self.desktop = kwargs["desktop"]
#
#    def run(self):
#        root = Tk()
#        app = switchboard.Window(self.desktop, master=root)
#        root.geometry("+550+0")
#        #root.geometry()
#        app.mainloop()
#        root.destroy()
