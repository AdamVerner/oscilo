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

from typing import Union
import logging

logger = logging.getLogger(__name__)

from matplotlib.figure import Figure

try:
    from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
except ImportError:
    try:
        from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
    except ImportError:
        raise Exception('Unable to start application as none of the matplotlib backends could be '
                        'imported')

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from multiprocessing import Pipe


class Plot(Gtk.Alignment):
    graph_properties = {
        'linestyle': '-',
        'marker': '',
    }

    def __init__(self, device):
        Gtk.Box.__init__(self)
        self.device = device
        self.set_hexpand(True)
        self.set_vexpand(True)

        fig = Figure()

        self.ax = fig.add_subplot(111, fc='black')

        self.ax.grid(True, 'both', 'both')

        self.ax.set_xlabel('Time [S]')
        self.ax.set_ylabel('Amplitude [V]')

        canvas = FigureCanvas(fig)
        canvas.set_size_request(600, 600)
        self.add(canvas)

        parent_conn, self.child_conn = Pipe(duplex=False)  # Pipe to pump the label data through

        def update_self(source, condition):
            """
            watches pipe and when data changes, changes the label
            """
            print(source, condition)
            assert parent_conn.poll()
            data = parent_conn.recv()

            logging.debug(data.keys(), data['trig_low'], data['trig_up'],  len(data['values']))

            self.ax.clear()
            self.ax.grid(True, 'both', 'both')
            self.ax.plot(data['values'], **self.graph_properties)

            if data['trig_low'] is not None:
                trig_low = [data['trig_low'] for _ in range(len(data['values']))]
                self.ax.plot(trig_low)
            if data['trig_up'] is not None:
                trig_up = [data['trig_up'] for _ in range(len(data['values']))]
                self.ax.plot(trig_up)

            self.queue_draw()
            return True

        GObject.io_add_watch(parent_conn.fileno(), GObject.IO_IN, update_self)

    def update(self) -> None:
        """renews plotted values from device"""

        data = {
            'values': self.device.get_samples(),
            'trig_low': self.device.get_trig_lvl(),
            'trig_up': self.device.get_trig_lvl()
        }
        self.child_conn.send(data)


if __name__ == '__main__':
    from Software.TestUtil import test_util
    from Software.Devices import Device
    p = Plot(Device())
    p.update()

    test_util(p)
