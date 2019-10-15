# /bin/env python3
# -*- coding: utf-8 -*-
"""
|------------------------------------|
| |SearchBar| |---------------------||
| |---------| |                     ||
| ||-------|| | DESCRIPTION         ||
| ||Device || | OF                  ||
| ||-------|| | THE                 ||
| ||-------|| | DEVICE              ||
| ||Device || |                     ||
| ||-------|| |---------------------||
|------------------------------------|
"""

import os
import sys

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

if __name__ == '__main__':
    sys.path.extend([os.path.abspath('../../../')])  # for running without Controller
    print(sys.path)

from Software.Devices.Wrapper import get_available_devices


class Module(Gtk.HBox):
    """
    Top level module for Scope view
    """

    def device_selected(self, box, box_row):
        self.device.change_device(box_row.device)
        self.make_selection(self.device)

    def __init__(self, device):
        self.device = device
        super(Module, self).__init__()

        self.box_rows = []

        self.device_list = Gtk.ListBox()
        self.device_list.connect('row-activated', self.device_selected)
        for dev in get_available_devices():
            row = Gtk.ListBoxRow()
            row.device = dev

            row.text_buffer = Gtk.TextBuffer()
            row.text_buffer.set_text(dev.__doc__)

            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(dev.icon, 64, 64, True)
            icon = Gtk.Image.new_from_pixbuf(pixbuf)
            icon_wrap = Gtk.Box(spacing=50)
            icon_wrap.pack_start(icon, True, True, 0)

            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)

            vbox = Gtk.VBox(spacing=5)
            vbox.pack_start(hbox, True, True, 0)
            vbox.pack_start(Gtk.Separator(), True, True, 0)

            row.add(vbox)
            self.box_rows.append(row)

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            hbox.pack_start(vbox, True, True, 0)

            label1 = Gtk.Label('<span size=\'25000\'>' + dev.name + '</span>', xalign=0)
            label1.set_use_markup(True)
            label2 = Gtk.Label(dev.description, xalign=0)

            vbox.pack_start(label1, True, True, 0)
            vbox.pack_start(label2, True, True, 0)

            hbox.pack_start(icon_wrap, False, True, 0)
            self.device_list.add(row)

        self.pack_start(self.device_list, False, False, 0)
        self.pack_start(Gtk.Separator(), False, False, 0)
        self.text_view = Gtk.TextView(accepts_tab=True, editable=False, cursor_visible=False)
        self.pack_start(self.text_view, True, True, 0)

    def make_selection(self, device):
        """
        receives device, tries to find in in device list, then select the one tab containing the
        device
        this is usefull, when device selection fails, and DUMMY is used as default it gets selected
        """
        # range through all devices, select the one;
        self.device_list.unselect_all()
        for row in self.box_rows:
            print(device._dev, row.device, isinstance(device._dev, row.device))
            if isinstance(device._dev, row.device):

                buffer = self.text_view.get_buffer()
                start = buffer.get_start_iter()
                end = buffer.get_end_iter()
                buffer.delete(start, end)
                buffer.insert_markup(start, row.device.__doc__, len(row.device.__doc__))

                self.device_list.select_row(row)
                break
        else:
            raise Exception('failed to select device')

    def redraw(self):
        """This page should be static, so there is no need to redraw anything"""
        # self.__init__(self.device)
        # self.make_selection(self.device)



if __name__ == '__main__':
    from Software.TestUtil import test_util
    from Software.Devices import Device

    m = Module(device=Device())

    test_util(m)
