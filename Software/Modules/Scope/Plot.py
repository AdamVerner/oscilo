

#!/usr/bin/env python
# coding=utf-8
"""
Drawing Plot and plotting the right values
"""

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Plot(Gtk.Box):

    def __init__(self, size=(400, 400)):

        self.size = size
        Gtk.Box.__init__(self)

        fig = Figure()
        self.ax = fig.add_subplot(111, facecolor='black')
        
        self.ax.plot((1, 2, 3, 4), (1, 2, 3, 4))

        canvas = FigureCanvas(fig)
        canvas.set_size_request(*size)
        self.add(canvas)


    # pres celou rozlohu pridat plot
    # z plotu odebrat popisky (asi)
    # zmenit pozadi plotu
    # pridat divisions
    # udelat spojity graf

    def update(self, values):

        self.ax.clear()
        self.ax.scatter(*values)
        self.ax.plot()


if __name__ == '__main__':

    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    window.set_default_size(400, 400)

    p = Plot()

    window.add(p)
    window.show_all()
    Gtk.main()
