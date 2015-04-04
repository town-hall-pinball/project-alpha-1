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

import os
import sys

import paver.doctools
import paver.virtual
from paver.easy import *
from paver.setuputils import setup

options(
    setup=dict(
        name="project-beta",
        version="0.0",
        url="http://townhallpinball.org",
        author="Town Hall Pinball Studios",
        author_email="admin@townhallpinball.org",
        package_data=paver.setuputils.find_package_data("pinlib",
            package="pinlib", only_in_packages=False)
    ),
    virtualenv=Bunch(
        packages_to_install=[
            "coverage",
            "docutils",
            "dpath",
            "nose",
            "Sphinx",
        ],
        install_paver=True,
        dest_dir="virtualenv",
        script_name="virtualenv-setup",
    ),
)

paver.setuputils.install_distutils_tasks()

@task
@paver.virtual.virtualenv("virtualenv")
def test():
    import nose
    sys.path.insert(0, os.path.abspath("."))
    nose.run(argv=["",
        "-w", "tests",
        "--with-coverage",
        "--cover-package=pinlib"
    ])


@task
@paver.virtual.virtualenv("virtualenv")
def doc():
    from sphinx import main as sphinx
    sphinx(["", "-b", "html", "doc", "build/doc"])


@task
@paver.virtual.virtualenv("virtualenv")
def console():
    sh("python")


@task
def clean():
    removes = (
        ("pinlib", "*.pyc"),
        ("pinlib", "*.pyo"),
        ("tests", "*.pyc"),
        ("tests", "*.pyo")
    )
    for directory, match in removes:
        for f in path(directory).walkfiles(match):
            f.remove()

@task
@paver.virtual.virtualenv("virtualenv")
def run():
    sys.argv = sys.argv[2:]
    print sys.argv



