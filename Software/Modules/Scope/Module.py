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

from Modules.Scope.Plot import Plot
from Modules.Scope.Settings import Settings
from Modules.Scope.Signals import Signals


class Module(Gtk.Grid):
    """
    Toplevel module for Scope view
    """

    def __init__(self, device):
        self.device = device

        Gtk.Grid.__init__(self)

        self.plot = Plot()
        self.settings = Settings()
        self.signals = Signals()

        self.attach(self.plot, 0, 0, 1, 1)
        self.attach(self.settings, 0, 1, 1, 1)
        self.attach(self.signals, 1, 0, 1, 2)


if __name__ == '__main__':

    from TestUtil import test_util
    from Devices.Dummy import Device

    m = Module(device=Device())

    test_util(m)
