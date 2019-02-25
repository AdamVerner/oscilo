# /bin/env python3
# -*- coding: utf-8 -*-
"""
|-------------------------------------------------------|
| |---------------------------------------------------| |
| |                 S E L E C T O R                   | |
| |---------------------------------------------------| |
| |---------------------------------------------------| |
| |                                                   | |
| |                                                   | |
| |                 S E L E C T E D                   | |
| |                                                   | |
| |                   M O D U L E                     | |
| |                                                   | |
| |                                                   | |
| |                                                   | |
| |---------------------------------------------------| |
|-------------------------------------------------------|
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Modules.Scope.Module import Module as ScopeModule


class ModuleSelector(Gtk.Notebook):
    """
    selects Modules to run
    """

    def __init__(self, device):
        super(ModuleSelector, self).__init__()
        self.device = device

        pages = list()
        pages.append(['Scope', ScopeModule(self.device)])

        for page in pages:
            # label = Gtk.Label()
            self.append_page(page[1], Gtk.Label(page[0]))

        self.show_all()


if __name__ == '__main__':
    from TestUtil import test_util
    from Devices.Dummy import Device

    test_util(ModuleSelector(Device()))
