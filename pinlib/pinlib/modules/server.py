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
import os
from threading import Thread

import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

from pinlib import p
from pinlib import log
import pinproc

def init():
    p.set_defaults({
        "server.enabled": True,
        "server.publish_events": True,
        "server.remote_control": True
    })
    p.events.on("server-adjust", server_adjust)
    server_adjust()

def server_adjust():
    running = p.threads.web
    if p.data["server.enabled"] and not running:
        p.threads.web = Web()
        p.threads.web.start()
    elif not p.data["server.enabled"] and running:
        p.threads.web.stop()
        p.threads.web = None

class Handler(WebSocket):

    def received_message(self, m):
        if not p.data["server.remote_control"]:
            return
        message = json.loads(str(m))
        command = message["command"]
        #print "command", str(message)
        if command == "status":
            self.status()
        if command == "switch":
            self.switch(message)
        if command == "lamp":
            self.lamp(message)
        if command == "coil":
            self.coil(message)
        if command == "flasher":
            self.flasher(message)
        if command == "trigger":
            self.trigger(message)
        if command == "ping":
            self.pong()

    def status(self):
        payload = p.machine.serialize()
        payload["modes"] = []
        for mode in p.modes:
            payload["modes"] += [mode.serialize()]
        payload["message"] = "status"
        self.send(json.dumps(payload))

    def pong(self):
        payload = { "message": "pong" }
        self.send(json.dumps(payload))

    def switch(self, message):
        switch = p.machine.switch(message["id"])
        if message["action"] == "toggle":
            if switch.is_closed():
                switch.open()
            else:
                switch.close()
        elif message["action"] == "activate":
            switch.activate()
        elif message["action"] == "deactivate":
            switch.deactivate()

    def lamp(self, message):
        lamp = p.machine.lamp(message["id"])
        if lamp.state["schedule"] == "disable":
            lamp.enable()
        else:
            lamp.disable()

    def coil(self, message):
        coil = p.machine.coil(message["id"])
        coil.pulse()

    def flasher(self, message):
        flasher = p.machine.flasher(message["id"])
        flasher.pulse()

    def trigger(self, message):
        p.events.trigger(message["event"])


class Root(object):

    @cherrypy.expose
    def ws(self):
        # you can access the class instance through
        handler = cherrypy.request.ws_handler

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def config(self):
        return p.machine.config


class Web(Thread):

    def __init__(self):
        super(Web, self).__init__()
        cherrypy.config.update({
            "server.socket_host": "0.0.0.0",
            "server.socket_port": 9000,
            "log.screen": False,
            "engine.autoreload.on": False
        })
        self.log = log.get("web")
        self.events = {
            "switch":   self.dispatch_device,
            "lamp":     self.dispatch_device,
            "coil":     self.dispatch_device,
            "flasher":  self.dispatch_device,
            "flippers": self.dispatch_device,
            "notify":   self.dispatch_notice,
            "mode":     self.dispatch_mode,
            "audio":    self.dispatch_audio,
            "simulate": self.dispatch_simulate,
        }

    def run(self):
        self.log.info("Starting web services")
        plugin = WebSocketPlugin(cherrypy.engine)
        plugin.subscribe()
        cherrypy.tools.websocket = WebSocketTool()

        for event, fn in self.events.items():
            p.events.on(event, fn)

        cherrypy.quickstart(Root(), "/", config={
            "/": {
                "tools.staticdir.on": True,
                "tools.staticdir.root": os.path.abspath(os.path.join(
                        os.path.dirname(__file__), "..", "web")),
                "tools.staticdir.index": "index.html",
                "tools.staticdir.dir": ""
            },
            "/console": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": "console"
            },
            "/ws": {
                "tools.websocket.on": True,
                "tools.websocket.handler_cls": Handler
            }
        })
        p.commands = None
        plugin.unsubscribe()

        for event, fn in self.events.items():
            p.events.off(event, fn)

        self.log.info("Web services stopped")

    def dispatch_device(self, item, *args, **kwargs):
        if not p.data["server.publish_events"]:
            return
        payload = item.serialize()
        payload["message"] = item.hardware
        cherrypy.engine.publish("websocket-broadcast", json.dumps(payload))

    def dispatch_notice(self, event):
        if not p.data["server.publish_events"]:
            return
        payload = {
            "message": "notice",
            "type":    event["type"],
            "text":    event["text"]
        }
        cherrypy.engine.publish("websocket-broadcast", json.dumps(payload))

    def dispatch_mode(self, ident, status, mode):
        if not p.data["server.publish_events"]:
            return
        payload = mode.serialize()
        payload["message"] = "mode"
        payload["active"] = status == "activate"
        cherrypy.engine.publish("websocket-broadcast", json.dumps(payload))

    def dispatch_audio(self, category, key, state):
        if not p.data["server.publish_events"]:
            return
        payload = {
            "message": "audio",
            "type": category,
            "text": key,
            "state": state
        }
        cherrypy.engine.publish("websocket-broadcast", json.dumps(payload))

    def dispatch_simulate(self, ball_from, ball_to):
        if not p.data["server.publish_events"]:
            return
        payload = {
            "message": "simulate",
            "text": "{} to {}".format(ball_from, ball_to)
        }
        cherrypy.engine.publish("websocket-broadcast", json.dumps(payload))

    def stop(self):
        p.commands = None
        cherrypy.engine.exit()
