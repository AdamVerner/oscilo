# /bin/env python3
# -*- coding: utf-8 -*-
"""
popup errors indicating what has gone wrong
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import serial.tools.list_ports


def task_fail(title="Task Failed", msg="Task Failed successfully"):
    """
    shows ERROR popup with some info about task that failed
    :param title: short string that shows as title
    :param msg: can be markup text  
    """
    dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.USE_HEADER_BAR, Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.OK,
                               title)
    dialog.format_secondary_markup(msg)
    ret = dialog.run()
    dialog.destroy()
    return ret


class PortSelector(Gtk.Dialog):
    selected = None

    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_hexpand(False)
        self.set_vexpand(True)
        self.set_modal(True)  # freeze the resto of the application
        self.set_deletable(False)
        # self.set_size_request(150, 300)
        self.set_geometry_hints(None, None, Gdk.WindowHints.MAX_SIZE)  # don't resize

        content = self.get_content_area()  # type: Gtk.Box

        content.set_orientation(Gtk.Orientation.VERTICAL)

        dev_list = Gtk.ListBox()
        self.entry = Gtk.Entry()

        self.entry.connect('activate', self.select_entry)
        dev_list.connect('row-activated', self.select_entry)  # double click or enter
        dev_list.connect('selected-rows-changed',
                         lambda a: self.entry.set_text(a.get_selected_row().value.device)
                         )

        dev_list.set_selection_mode(Gtk.SelectionMode.BROWSE)
        dev_list.set_activate_on_single_click(False)

        for comport in serial.tools.list_ports.comports():
            row = Gtk.ListBoxRow()
            row.value = comport

            box = Gtk.Box()
            box.set_homogeneous(True)

            lbl1 = Gtk.Label(comport.device)
            sep1 = Gtk.Separator()
            lbl2 = Gtk.Label(comport.name)
            sep2 = Gtk.Separator()
            lbl3 = Gtk.Label(comport.description)

            box.pack_start(lbl1, True, True, 2)
            box.pack_start(lbl2, True, True, 2)
            box.pack_start(lbl3, True, True, 2)

            row.add(box)
            dev_list.add(row)

        content.pack_start(self.entry, False, True, 0)
        content.pack_start(dev_list, False, True, 0)
        self.show_all()

    def select_entry(self, widget, *_):
        self.selected = self.entry.get_text()
        self.response(Gtk.ResponseType.OK)

    def get_selection(self) -> str:
        self.run()
        self.destroy()
        return self.selected


if __name__ == '__main__':
    dialog = PortSelector()
    print(dialog.get_selection())
    task_fail()
