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

class Display(object):

    def __init__(self):
        self.CENTER_X = self.WIDTH / 2;
        self.CENTER_Y = self.HEIGHT / 2;

    def create_frame(width, height):
        raise NotImplementedError()

    def copy_rect(self, dst, dst_x, dst_y, src, src_x, src_y,
            width, height, op="copy"):
        pass


class DMD128x32x16(Display):

    WIDTH = 128
    HEIGHT = 32


class Sound(object):

    def play(self, name):
        pass

    def stop(self, name):
        pass


class Threads(object):
    web = None


class Switch(object):

    def __init__(self, name):
        self.name = name
