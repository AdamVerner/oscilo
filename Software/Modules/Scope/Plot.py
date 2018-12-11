#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
|----------------------------------------------------------|
|             ,--|--.                                      |
|          ,-'       `-.                                   |
|        ,'      |      `.                                 |
|      ,'                 `.                               |
|     /          |          \                              |
|    /                       \                           / |
|- - - - - - - - + - - - - - -\- - - - - - - - - - - - -/- |
|                              \                       /   |
|                |              \                     /    |
|                                `.                 ,'     |
|                |                 `.             ,'       |
|                                    `-.       ,-'         |
|                |                      `--,--'            |
|----------------------------------------------------------|
"""


from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Plot(Gtk.Box):

    graph_properties = {
        'linestyle': '-',
        'marker': 'o',
    }

    def __init__(self, size=(400, 400)):
        self.size = size
        Gtk.Box.__init__(self)

        fig = Figure()

        self.ax = fig.add_subplot(111, fc='black')

        self.ax.grid(True, 'both', 'both')

        y = [0, 1, 2, 3, 2.57]

        self.ax.plot(range(len(y)), y, **self.graph_properties)

        canvas = FigureCanvas(fig)
        canvas.set_size_request(*size)
        self.add(canvas)

    # TODO z plotu odebrat popisky (asi)
    # TODO zmenit pozadi plotu
    # TODO pridat divisions
    # TODO zmensit velikost bodu

    def update(self, values):

        self.ax.clear()
        self.ax.grid(True, 'both', 'both')
        self.ax.plot(*values, **self.graph_properties)
        self.queue_draw()


if __name__ == '__main__':
    from TestUtil import test_util

    p = Plot()

    def t1(*_, **__):
        print('t1')
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        p.update([x, y])

    def t2(*_, **__):
        print('t2')
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        p.update([x, y])

    test_util(p, t1, t2)
