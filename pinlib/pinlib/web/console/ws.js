/*
* Copyright (c) 2014 - 2015 townhallpinball.org
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
* FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
* DEALINGS IN THE SOFTWARE.
*/

var p = p || {};

p.ws = p.ws || (function() {

    var ws = null;
    var timer = null;
    var self = {};

    self.events = p.events();
    self.connected = false;

    self.connect = function() {
        heartbeat();
        timer = setInterval(heartbeat, 1000);
    };

    self.send = function(message) {
        ws.send(JSON.stringify(message));
    };

    self.command = function(command, id, action) {
        self.send({
            command: command,
            action: action,
            id: id
        });
    };

    var heartbeat = function() {
        if ( !ws ) {
            ws = new WebSocket('ws://localhost:9000/ws');
            ws.onopen = onopen;
            ws.onerror = onerror;
            ws.onmessage = onmessage;
        } else if ( ws && ws.readyState === WebSocket.OPEN ) {
            self.send({command: "ping"});
        } else if ( ws && ws.readyState === WebSocket.CLOSED ) {
            disconnected();
        }
    };

    var onopen = function () {
        console.log("connected");
        self.connected = true;
        self.events.trigger("connect");
    };

    var onmessage = function(message) {
        var data = JSON.parse(message.data);
        if ( data.message === "pong" ) {
            return;
        }
        console.log("event", data);
        self.events.trigger("message", data);
    };

    var onerror = function(error) {
        disconnected();
    };

    var disconnected = function() {
        ws = null;
        if ( !self.connected ) {
            return;
        }
        self.connected = false;
        self.events.trigger("disconnect");
    };

    return self;

})();
