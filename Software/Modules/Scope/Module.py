# /bin/env python3
# -*- coding: utf-8 -*-
"""
|-----------------------------|
|                       |  S  |
|         PLOT          |  I  |
|                       |  G  |
|-----------------------|  N  |
|                       |  A  |
|       SETTINGS        |  L  |
|                       |  S  |
|-----------------------------|
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Software.Modules.Scope.Plot import Plot
from Software.Modules.Scope.Settings import Settings
from Software.Modules.Scope.Signals import Signals


class Module(Gtk.Grid):
    """
    Toplevel module for Scope view
    """

    def __init__(self, device):
        self.device = device
        super(Module, self).__init__()

        self.plot = Plot(self.device)
        self.settings = Settings(self.device)
        self.signals = Signals()

        self.settings.control.push_func = self.plot.update

        self.attach(self.plot, 0, 0, 1, 1)
        # self.attach(self.signals, 1, 0, 1, 1)
        self.attach(self.settings, 0, 1, 1, 1)

    def redraw(self):
        self.plot.redraw()
        self.settings.redraw()
        self.signals.redraw()


if __name__ == '__main__':
    from Software.TestUtil import test_util
    from Software.Devices import Device
    m = Module(device=Device())

    test_util(m)
