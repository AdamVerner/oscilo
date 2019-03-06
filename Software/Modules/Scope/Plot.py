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
        'color': 'green'
    }

    def __init__(self, device):
        super(Plot, self).__init__()
        self.device = device
        self.set_hexpand(True)
        self.set_vexpand(True)

        fig = Figure()
        fig.subplots_adjust(top=1, bottom=0.09, right=1, left=0.065,
                            hspace=0.2, wspace=0.2)

        self.ax = fig.add_subplot(111, fc='black')
        self._def_axis(self.ax)

        canvas = FigureCanvas(fig)

        canvas.set_size_request(600, 600)
        self.add(canvas)

        parent_conn, self.child_conn = Pipe(duplex=False)  # Pipe to pump the label data through

        def update_self(source, condition):
            """
            watches pipe and when data changes, changes the label
            """
            print('source = ', source, 'condition = ', condition)
            assert parent_conn.poll()
            data = parent_conn.recv()

            samples = data['values']

            self._def_axis(self.ax)
            self.ax.plot(samples, **self.graph_properties)

            if data['trig_low'] is not None:
                self.ax.axhline(y=data['trig_low'], color='b', linestyle=':')
            if data['trig_up'] is not None:
                self.ax.axhline(y=data['trig_up'], color='b', linestyle=':')
            if data['trig_place'] is not None:
                self.ax.axvline(x=data['trig_place'], color='r', linestyle=':')

            self.queue_draw()
            return True

        GObject.io_add_watch(parent_conn.fileno(), GObject.IO_IN, update_self)

    def update(self) -> None:
        """renews plotted values from device"""

        data = {
            'values': self.device.get_samples(),
            'trig_low': self.device.get_trig_lvl(),
            'trig_up': self.device.get_trig_lvl(),
            'trig_place': self.device.get_trig_place() * self.device.sample_count
        }
        print('data trigplace', data['trig_place'])
        self.child_conn.send(data)

    @staticmethod
    def _def_axis(ax):

        ax.clear()
        ax.grid(True, 'both', 'both')
        ax.set_xlabel('Time [S]')
        ax.set_ylabel('Amplitude [V]')
        ax.margins(tight=True)

    def redraw(self):
        self.update()



if __name__ == '__main__':
    from Software.TestUtil import test_util
    from Software.Devices import Device
    p = Plot(Device())
    p.update()

    test_util(p)
