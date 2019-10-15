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

from Software.Modules.Scope.Module import Module as ScopeModule
from Software.Modules.Selector.Module import Module as DeviceSelector
from Software.Modules.Overview.Module import Module as Overview


class ModuleSelector(Gtk.Notebook):
    """
    selects Modules to run
    """

    def __init__(self, device):
        super(ModuleSelector, self).__init__()
        self.device = device

        self.pages = list()
        self.pages.append(['DeviceSelector', DeviceSelector(self.device)])
        self.pages.append(['Scope', ScopeModule(self.device)])
        self.pages.append(['Overview', Overview()])

        for page in self.pages:
            # label = Gtk.Label()
            self.append_page(page[1], Gtk.Label(page[0]))

        self.show_all()
        self.connect('switch-page', self.change_page)

    def change_page(self, selector, module, page_num):
        # assume that page order didn't diviate from page list
        self.pages[page_num][1].redraw()


if __name__ == '__main__':
    from Software.TestUtil import test_util
    from Software.Devices import Device

    test_util(ModuleSelector(Device()))
