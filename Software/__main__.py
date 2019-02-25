#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
"""
import logging
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

logger = logging.getLogger(__name__)
from Software.MainWindow import MainWindow

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    os.environ['NO_AT_BRIDGE'] = '1'
    MainWindow()
    Gtk.main()
