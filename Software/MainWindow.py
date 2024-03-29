#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
"""
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Software.Modules.ModuleSelector import ModuleSelector
from Software.Devices import Device

# constant to scale the default window size to
SIZE_CONST = 0.66


class MainWindow(Gtk.Window):
    """

    """

    def __init__(self):
        Gtk.Window.__init__(self)

        self.set_title('Oscilo')
        self.set_border_width(6)

        s = self.get_screen()

        # get the monitor which the windows is on
        try:
                active_window = s.get_active_window()
                monitor_at_window = s.get_monitor_at_window(active_window)
                monitor = s.get_monitor_geometry(monitor_at_window)
                self.set_default_size(monitor.width * SIZE_CONST, monitor.height * SIZE_CONST)
        except TypeError:
            pass

        self.set_border_width(0)
        self.connect('destroy', Gtk.main_quit)

        self.device = Device()

        self.add(ModuleSelector(self.device))

        self.show_all()


if __name__ == '__main__':
    main = MainWindow()
    Gtk.main()
