# /bin/env python3
# -*- coding: utf-8 -*-
"""

|----------|
||--------||
||  CH1   ||
||--------||
||--------||
||  CH2   ||
||--------||
||--------||
||  MATH  ||
||--------||
|----------|

"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Signals(Gtk.Grid):
    """
    selects signal that will be highlighted
    posibilitiy to add more signals
        - reference signals from CSV files
        - Math with other signals


    """

    def __init__(self):
        super(Signals, self).__init__()


if __name__ == '__main__':
    from TestUtil import test_util
    s = Signals()
    test_util(s)


