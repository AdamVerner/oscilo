# /bin/env python3
# -*- coding: utf-8 -*-
"""
|-----------------------------|
| |SearchBar| |--------------||
| |---------| |              ||
| ||-------|| | DESCRIPTION  ||
| ||Device || | OF           ||
| ||-------|| | THE          ||
| ||-------|| | DEVICE       ||
| ||Device || |              ||
| ||-------|| |--------------||
|-----------------------------|
"""

import os
import sys

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

if __name__ == '__main__':
    sys.path.extend([os.path.abspath('../../')])  # for running without Controller
    print(sys.path)

from Software.Devices import get_available_devices


class Module(Gtk.Grid):
    """
    Toplevel module for Scope view
    """

    def __init__(self, device):
        self.device = device
        super(Module, self).__init__()


git
add
self.device_list = Gtk.ListBox()

for dev in get_available_devices():
    row = Gtk.ListBoxRow()
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
    row.add(hbox)
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    hbox.pack_start(vbox, True, True, 0)

    label1 = Gtk.Label("Automatic Data & Time", xalign=0)
    label2 = Gtk.Label("Requires internet access", xalign=0)
    vbox.pack_start(label1, True, True, 0)
    vbox.pack_start(label2, True, True, 0)

    switch = Gtk.Switch()
    switch.props.valign = Gtk.Align.CENTER
    hbox.pack_start(switch, False, True, 0)
    self.device_list.add(row)

self.attach(self.device_list, 0, 0, 1, 1)

if __name__ == '__main__':
    from Software.TestUtil import test_util
    from Software.Devices import Device

    m = Module(device=Device())

    test_util(m)
