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

$(function() {

    var famap = {
        "coil":     "fa-database",
        "flasher":  "fa-bolt",
        "lamp":     "fa-lightbulb-o",
        "switch":   "fa-minus-square-o",
        "flippers": "fa-arrows-h",
        "mode":     "fa-flag",

        "game":     "fa-info-circle",
        "music":    "fa-music",
        "sound":    "fa-volume-up",
        "local":    "fa-info-circle",
        "error":    "fa-exclamation-triangle",
        "simulate": "fa-play"
    }

    var config;
    var ready = false;
    var holdStart;
    var id = 0;
    var animations = {};
    var timer = null;
    var keyhold = {};
    var listAction = "mark";
    var modes = [];

    var load = function() {
        $.getJSON("/config", init);
    };

    var init = function(data) {
        config = data;
        p.config = config;
        config.devices = {};
        config.keys = {};
        $("#title").html(config["game.name"]);
        _.each(["PRSwitches", "PRLamps", "PRCoils"], function(type) {
            _.each(config[type], function(device, name) {
                if ( device.category === "unused" || device.id[0] === "F" ) {
                    return;
                }
                device.name = name;
                if ( config.devices[device.id] ) {
                    logError("Duplicate device " + device.id + " for " +
                        config.devices[device.id].label + " and " +
                        device.label);
                }
                config.devices[device.id] = device;
                if ( type == "PRSwitches" ) {
                    device.hardware = "switch";
                    device.indicator = "switch";
                    if ( device.type === "NC" ) {
                        device.opto = true;
                    }
                } else if ( type == "PRLamps" ) {
                    device.hardware = "lamp";
                    device.indicator = "light";
                } else if ( type == "PRCoils" ) {
                    if ( device.tags && _.contains(device.tags, "flasher") ) {
                        device.hardware = "flasher";
                        device.indicator = "light";
                    } else {
                        device.hardware = "coil";
                        device.indicator = "coil";
                    }
                }
                if ( device.keyboard ) {
                    var char = device.keyboard.toUpperCase();
                    if ( config.keys[char] ) {
                        logError("Duplicate keymap " + char + " for " +
                            config.keys[char].label + " and " + device.label);
                    }
                    config.keys[char] = device;
                }
            });
        });
        config.devices.flippers = {
            "hardware": "flippers",
            "id": "flippers",
            "label": "Enable Flippers"
        }
        switchMatrix();
        lampMatrix();
        coilFlasherMatrix();
        deviceList();
        keyboardReference();

        $("#search input").keyup(filter);
        $("#device-filter input").change(filter);
        $("input [data-action='filter']").change(filter);
        $('[data-toggle="tooltip"]').tooltip({
            "container": "body",
        });
        $("#action-button .dropdown-menu a").click(function() {
            listAction = $(this).attr("id");
            $("#action-button button i").attr("class",
                    $(this).find("i").attr("class"));

            if ( listAction === "info" ) {
                $("#log").hide();
                $("#info-panel").show();
            } else {
                $("#log").show();
                $("#info-panel").hide();
            }
        });
        $("#ball-search").click(function() {
            p.ws.send({ command: "trigger", event: "request_ball_search" });
        });
        $(document).keydown(keydown);
        $(document).keyup(keyup);

        console.log("config", config);
        requestAnimationFrame(tick);
        ready = true;

        if ( config.simulator ) {
            p.sim.start();
        }

        p.ws.events
            .on("connect", onConnect)
            .on("disconnect", onDisconnect)
            .on("message", onMessage);
        p.ws.connect();
    };

    var deviceList = function() {
        var sorted = _.sortBy(config.devices, "label");
        _.each(sorted, function(device) {
            if ( device.category === "unused" ) {
                return;
            }
            // No flippers that are controlled by rules
            if ( device.id[0] === "F" ) {
                return;
            }
            // Don't include pseudo-device to enable/disable the flippers
            if ( device.hardware === "flippers" ) {
                return;
            }
            var $device = $("<li></li>")
                .attr("data-device", device.id)
                .attr("data-name", device.name);
            var $favorite = $("<i></i>")
                .addClass("favorite")
                .addClass("fa")
                .addClass("fa-fw")
                .addClass("fa-star");
            var $icon = $("<i></i>")
                .addClass("hardware")
                .addClass("fa")
                .addClass("fa-fw")
                .addClass(famap[device.hardware]);
            var $label = $("<span></span>")
                .attr("data-hardware", device.hardware)
                .html(device.label);
            $device.append($favorite);
            $device.append($icon);
            $device.append($label);
            $("#device-list ul").append($device);
            device.$listItem = $device;
        });

        $("#device-list li").hover(function() {
            var id = $(this).attr("data-device");
            $("#" + id).parent().addClass("hover-link");
        }, function() {
            var id = $(this).attr("data-device");
            $("#" + id).parent().removeClass("hover-link");
        });

        $("#device-list li").mousedown(function() {
            listCommand(config.devices[$(this).attr("data-device")], "down");
        }).mouseup(function() {
            listCommand(config.devices[$(this).attr("data-device")], "up");
        });
    };

    var listCommand = function(device, mouse) {
        if ( listAction === "mark" && mouse === "down" ) {
            device.$listItem.toggleClass("selected");
            device.$listItem.find(".favorite").toggleClass("selected");
        } else if ( listAction === "send" ) {
            if ( mouse === "down" ) {
                holdStart = Date.now();
            }
            if ( mouse === "up" ) {
                if ( Date.now() - holdStart > 500 ) {
                    return;
                }
            }
            deviceCommand(device, mouse);
        } else if ( listAction === "info" ) {
            var hardware = device.hardware;
            if ( device.opto ) {
                hardware = "opto";
            }

            $("#info-label").html(device.label);
            $("#info-hardware").html(hardware);
            $("#info-name").html(device.name);
            $("#info-id").html(device.id);
            $("#info-notes").html(device.notes || device.note);
        }
    };

    var deviceCommand = function(device, mouse) {
        if ( device.hardware === "switch" ) {
            p.ws.send({
                command: "switch",
                action: "toggle",
                id: device.id
            });
        } else if ( device.hardware === "lamp" ) {
            p.ws.send({
                command: "lamp",
                action: "toggle",
                id: device.id
            });
        } else if ( device.hardware === "coil" && mouse === "up" ) {
            p.ws.send({
                command: "coil",
                action: "pulse",
                id: device.id
            });
        } else if ( device.hardware === "flasher" && mouse === "up")  {
            p.ws.send({
                command: "flasher",
                action: "pulse",
                id: device.id
            });
        }
    };

    var switchMatrix = function() {
        var $table = $("#switches table");
        for ( var row = 1; row <= 8; row++ ) {
            $row = $("<tr></tr>");
            cell($row, "SD" + row, "left-column");
            for ( var col = 1; col <= 8; col++ ) {
                cell($row, "S" + col + row);
            }
            cell($row, "SF" + row, "right-column")
            $table.append($row);
        }
        $("#switches").append($table);
    };

    var lampMatrix = function() {
        var $table = $("#lamps table");
        for ( var row = 1; row <= 8; row++ ) {
            $row = $("<tr></tr>");
            for ( var col = 1; col <= 8; col++ ) {
                cell($row, "L" + col + row);
            }
            cell($row, "G0" + row, "right-column")
            $table.append($row);
        }
        $("#lamps").append($table);
    };

    var coilFlasherMatrix = function() {
        var $table = $("#coils table");
        var $row = $("<tr></tr>");
        for ( var num = 1; num <= 40; num++ ) {
            var strNum = ( num < 10 ) ? "0" + num : num;
            cell($row, "C" + strNum);
            if ( num % 5 === 0 ) {
                $table.append($row);
                $row = $("<tr></tr>");
            }
        }
        $("#coils").append($table);
    };

    var cell = function($row, id, type) {
        type = type || "normal";
        var device = config.devices[id];
        var $cell = $("<td></td>").addClass(type);
        var $indicator = $("<div></div>");
        if ( device && device.category !== "unused" ) {
            $cell.attr("title", device.label)
                .attr("data-toggle", "tooltip");
            $indicator.addClass(device.indicator)
                .attr("id", device.id)
                .attr("data-name", device.name)
                .addClass("off");
            device.$indicator = $indicator;
        } else {
            $indicator.addClass("unused");
        }
        $cell.append($indicator);
        $row.append($cell);
    };

    var filter = function() {
        var text = $("#search input").val();
        var hardware = {};
        $("#device-filter input:checked").each(function() {
            hardware[$(this).attr("data-hardware")] = true;
        });
        if ( /^ *$/.test(text) ) {
            text = ".*";
        }
        var regexp = new RegExp(text, "i");
        $("#device-list li").each(function() {
            var device = config.devices[$(this).attr("data-device")]
            var content = device.label + " " + device.search;
            var show = hardware[device.hardware] && regexp.test(content);
            if ( hardware.favorites && !$(this).hasClass("selected") ) {
                show = false;
            }
            if ( show ) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    };

    var keyboardEntry = function($row, device) {
        var $key = $("<td>&nbsp;</td>");
        var $label = $("<td>&nbsp;</td>");
        if ( device ) {
            $key.html(device.keyboard);
            $label.html(device.label);
        }
        $row.append($key);
        $row.append($label);
    };

    var keyboardReference = function() {
        var $table = $("#keyboard-table");
        $table.empty();
        var devices = _.sortBy(config.keys, "keyboard");
        var rows = Math.ceil(devices.length / 2);
        for ( var row = 0; row < rows; row ++ ) {
            var $row = $("<tr></tr>");
            keyboardEntry($row, devices[row]);
            keyboardEntry($row, devices[row + rows]);
            $table.append($row);
        };
    };

    var onDisconnect = function() {
        $("#connection").removeClass("on");
        _.each(config.devices, function(device) {
            disable(device.id);
        });
        $("#modes table").empty();
        logNotice({
            type: "error",
            text: "Connection closed by remote host"
        });
    };

    var onConnect = function () {
        p.ws.send({command: "status"});
        $("#connection").addClass("on");
        logNotice({type: "local", text: "Connection established"});
    };

    var onMessage = function(data) {
        $("#activity")
            .finish()
            .css("background-color", "#fff")
            .animate({ backgroundColor: "#000" }, 250);

        if ( data.message === "status" ) {
            delete data.message;
            updateStatus(data);
            return;
        }

        if ( !ready ) {
            return;
        }
        if ( data.message === "notice" ) {
            logNotice(data);
        } else if ( data.message === "mode" ) {
            updateModes(data);
        } else if ( data.message === "audio" ) {
            logAudio(data);
        } else if ( data.message === "simulate" ) {
            logSimulate(data);
        } else {
            logDevice(data);
            updateDevice(data);
        }
    };

    var updateStatus = function(data) {
        console.log("status", data);
        _.each(data, function(group) {
            _.each(group, function(device) {
                if ( config.devices[device.id] && device.schedule !== "pulse" ) {
                    updateDevice(device);
                }
            });
        });
        modes = data.modes;
        updateModes();
    };

    var updateDevice = function(device) {
        if ( !device || !config.devices[device.id] ) {
            return;
        }
        var $element = $("#" + device.id);
        if ( device.active === true || device.schedule === "enable" ) {
            enable(device.id);
        } else if ( device.active === false || device.schedule === "disable" ) {
            disable(device.id);
        } else {
            animations[device.id] = device;
        }
    };

    var updateModes = function(message) {
        if ( message ) {
            if ( message.active ) {
                modes.push(message);
                log("mode", "enable", message.label);
            } else {
                _.remove(modes, { id: message.id });
                log("mode", "disable", message.label);
            }
        }
        modes = _.sortBy(modes, "priority").reverse();
        var $table = $("#modes table").empty();
        _.each(modes, function(mode) {
            var $row = $("<tr></tr>");
            var $priority = $("<td></td>")
                .addClass("priority")
                .html(mode.priority);
            var $id = $("<td></td>").html(mode.label);
            $row.append($priority);
            $row.append($id);
            $table.append($row);
        });
    };

    var log = function(type, style, message) {
        var $icon = $("<i></i>")
            .addClass("fa")
            .addClass("fa-fw")
            .addClass(famap[type]);
        var $message = $("<span></span>")
            .html(message);
        var $item = $("<li></li>")
            .addClass(style)
            .attr("data-type", type);
        $item.append($icon);
        $item.append($message);
        $("#log ul").prepend($item);
    };

    var logError = function(message) {
        log("error", "error", message);
    };

    var logDevice = function(device) {
        var style = "enable";
        if ( device.schedule === "disable" ) {
            style = "disable";
        }
        log(device.hardware, style, device.label);
    };

    var logNotice = function(entry) {
        log(entry.type, entry.type, entry.text);
    };

    var logAudio = function(entry) {
        log(entry.type, entry.state, entry.text);
    };

    var logSimulate = function(entry) {
        log("simulate", "simulate", entry.text);
    };

    var key = function(event) {
        if ( event.target.nodeName === "INPUT" ) {
            return;
        }
        var char = String.fromCharCode(event.which);
        var device = config.keys[char];
        if ( device ) {
            deviceCommand(device);
        }
    };

    var keydown = function(event) {
        if ( keyhold[event.which] ) {
            return;
        }
        keyhold[event.which] = true;
        key(event);
    };

    var keyup = function(event) {
        keyhold[event.which] = false;
        key(event);
    };

    var send = function(payload) {
        throw Error("NO SEND");
    };

    var on = function(id) {
        device = config.devices[id];
        if ( device.id === "flippers" ) {
            $("#flippers-enable").removeClass("off").addClass("on");
            return;
        }
        if ( !device.opto ) {
            device.$indicator.removeClass("off").addClass("on");
        } else {
            device.$indicator.removeClass("on").addClass("off");
        }
        device.$listItem.removeClass("off").addClass("on");

    };

    var off = function(id) {
        device = config.devices[id];
        if ( device.id === "flippers" ) {
            $("#flippers-enable").removeClass("on").addClass("off");
            return;
        }
        if ( !device.opto ) {
            device.$indicator.removeClass("on").addClass("off");
        } else {
            device.$indicator.removeClass("off").addClass("on");
        }
        device.$listItem.removeClass("on").addClass("off");
    }

    var enable = function(id) {
        delete animations[id];
        on(id);
    };

    var disable = function(id) {
        delete animations[id];
        off(id);
    };

    var pulse = function(id) {
        device = config.devices[id];
        device.$indicator
            .css("background-color", "#fff")
            .delay(device.duration)
            .animate({ backgroundColor: "#000" }, 1000);
        device.$listItem
            .css("background-color", "#888")
            .delay(device.duration)
            .animate({
                backgroundColor: "#000"
            }, 1000)
    };

    var tick = function(timestamp) {
        var completed = [];
        _.each(animations, function(device) {
            if ( device.schedule === "patter" ) {
                var total = device.on + device.off;
                var slice = timestamp % total;
                if ( slice < device.on ) {
                    on(device.id);
                } else {
                    off(device.id);
                }
            } else if ( device.schedule === "pulse" ) {
                pulse(device.id);
                completed.push(device);
            } else if ( device.schedule === "pulsed_patter" ) {
                pulse(device.id);
                completed.push(device);
            }
        });
        _.each(completed, function(device) {
            delete animations[device.id];
        });
        requestAnimationFrame(tick);
    };

    load();
});
