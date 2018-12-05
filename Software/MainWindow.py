#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    """

    """

    def __init__(self):
        Gtk.Window.__init__(self)

        self.set_title('Oscilo')
        self.set_default_size(1920, 600)
        self.set_border_width(50)
        self.connect('destroy', Gtk.main_quit)

        self.mainGrid = Gtk.Grid()
        self.add(self.mainGrid)

        self.show_all()


if __name__ == '__main__':
    main = MainWindow()
    Gtk.main()
