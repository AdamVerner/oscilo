#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
"""
import os

import gi

gi.require_version('Gtk', '3.0')

from MainWindow import MainWindow

if __name__ == '__main__':
    os.environ['NO_AT_BRIDGE'] = '1'
    MainWindow()
