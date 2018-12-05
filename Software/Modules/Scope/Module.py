# /bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Plot import Plot


class Module(Gtk.Box):

    def __init__(self, device):
        self.device = device
        Gtk.Box.__init__(self)
        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.plot = Plot()

        self.grid.attach(0, 0, self.plot)




if __name__ == '__main__':

    window = Gtk.Window()
    module = Module()
    window.add(module)
    window.show_all()
    
    Gtk.main()
