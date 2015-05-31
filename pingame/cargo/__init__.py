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

systems = [
    "Colony A",
    "Colony B",
    "Colony C",
    "Colony D",
    "Colony E",
]

elements = {
    "A": "Cargo A",
    "B": "Cargo B",
    "C": "Cargo C",
    "D": "Cargo D",
    "E": "Cargo E"
}

hi = 3.0
av = 1.0
lo = 0.25

prices = {
    "Colony A": {
        "A": hi,
        "B": av,
        "C": av,
        "D": lo,
        "E": lo
    },
    "Colony B": {
        "A": lo,
        "B": hi,
        "C": av,
        "D": av,
        "E": lo
    },
    "Colony C": {
        "A": lo,
        "B": lo,
        "C": hi,
        "D": av,
        "E": av
    },
    "Colony D": {
        "A": av,
        "B": lo,
        "C": lo,
        "D": hi,
        "E": av
    },
    "Colony E": {
        "A": av,
        "B": av,
        "C": lo,
        "D": lo,
        "E": hi
    }
}
