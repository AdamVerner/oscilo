# /bin/env python3
# -*- coding: utf-8 -*-
"""

  |----------------------------------------------------------------------------------|
  |  TRIGGER SETTINS    #     Horizontal      #      VERTICAL      #    FILTERING    |
  | |------| |------|   #   |------------|    #   |------------|   #   |---------|   |
  | | Rise | | Tval |   #   |   SPEED    |    #   |  todo      |   #   |         |   |
  | |------| |------|   #   |------------|    #   |     T      |   #   |         |   |
  | | Fall | |------|   #   |            |    #   |     O      |   #   |         |   |
  | |------| |  T   |   #   |     S      |    #   |     D      |   #   |         |   |
  | | Both | |  L   |   #   |     P      |    #   |     O      |   #   |         |   |
  | |------| |  V   |   #   |     S      |    #   |            |   #   |         |   |
  | | Other| |  l   |   #   |            |    #   |            |   #   |         |   |
  | |------| |------|   #   |------------|    #   |------------|   #   |---------|   |
  |----------------------------------------------------------------------------------|
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


LABEL_START = '<big>'
LABEL_END   = '</big>'
LABEL_PROPS = {'xpad': 12,
               'use_markup': True
               }


class Settings(Gtk.Grid):
    """
    wrapper for the underlying classes
    """

    def __init__(self):
        super(Settings, self).__init__()

        self.trigger    = Trigger()
        self.vertical   = Vertical()
        self.horizontal = Horizontal()
        self.filtering  = Filters()

        self.attach(self.trigger,    0, 0, 1, 1)
        self.attach(self.vertical,   1, 0, 1, 1)
        self.attach(self.horizontal, 2, 0, 1, 1)
        self.attach(self.filtering,  3, 0, 1, 1)


class Trigger(Gtk.Grid):
    """
    source
    Rising/falling/both edges
    level
    """

    def __init__(self):
        super(Trigger, self).__init__()
        label = Gtk.Label(LABEL_START + 'TRIGGER MENU' + LABEL_END, **LABEL_PROPS)
        self.attach(label, 0, 0, 1, 1)


class Vertical(Gtk.Grid):
    """
    AC/DC
    Offset
    volts/div
    """

    def __init__(self):
        super(Vertical, self).__init__()
        label = Gtk.Label(LABEL_START + 'VERTICAL MENU' + LABEL_END, **LABEL_PROPS)
        self.attach(label, 0, 0, 1, 1)


class Horizontal(Gtk.Grid):
    """
    position
    sec/div
    """

    def __init__(self):
        super(Horizontal, self).__init__()
        label = Gtk.Label(LABEL_START + 'HORIZONTAL MENU' + LABEL_END, **LABEL_PROPS)
        self.attach(label, 0, 0, 1, 1)


class Filters(Gtk.Grid):
    """
    LowPass
    HighPass
    BandPass
    Derivation
    """
    def __init__(self):
        super(Filters, self).__init__()
        label = Gtk.Label(LABEL_START + 'FILTERS' + LABEL_END, **LABEL_PROPS)
        self.attach(label, 0, 0, 1, 1)


if __name__ == '__main__':
    from TestUtil import test_util
    test_util(Settings())
