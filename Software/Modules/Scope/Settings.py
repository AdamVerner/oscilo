# /bin/env python3
# -*- coding: utf-8 -*-
"""

  |----------------------------------------------------------------------------|
  |  TRIGGER  SETTING    #    Horizontal     #    VERTICAL    #    FILTERING   |
  | |------| |-------|   #   |----------|    #   |--------|   #   |---------|  |
  | | Rise | |  Tval |   #   |  SPEED   |    #   |  todo  |   #   |         |  |
  | |------| |-------|   #   |----------|    #   |   T    |   #   |         |  |
  | | Fall | |-------|   #   |          |    #   |   O    |   #   |         |  |
  | |------| |   T   |   #   |    S     |    #   |   D    |   #   |         |  |
  | | Both | |   L   |   #   |    P     |    #   |   O    |   #   |         |  |
  | |------| |   V   |   #   |    S     |    #   |        |   #   |         |  |
  | | Other| |   l   |   #   |          |    #   |        |   #   |         |  |
  | |------| |-------|   #   |----------|    #   |--------|   #   |---------|  |
  |----------------------------------------------------------------------------|
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Popups import task_fail


LABEL_START = '<big>'
LABEL_END   = '</big>'
LABEL_PROPS = {'xpad': 12,
               'use_markup': True
               }


class Settings(Gtk.Grid):
    """
    wrapper for the underlying classes
    """

    def __init__(self, device):
        super(Settings, self).__init__()
        self.device = device
        self.size = (800, 400)

        self.trigger    = Trigger(self.device)
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
    |------------------|
    | |-------------|  |
    | |     LABEL   |  |
    | |-------------|  |
    | |------||-----|  |
    | | RISE ||  L  |  |
    | |------||  V  |  |
    | | FALL ||  L  |  |
    | |------||-----|  |
    | | BOTH || SET |  |
    | |------||-----|  |
    |------------------|
    """

    def __init__(self, device):
        super(Trigger, self).__init__()
        self.device = device
        label = Gtk.Label(LABEL_START + 'TRIGGER MENU' + LABEL_END, **LABEL_PROPS)

        level_adjust = Gtk.Adjustment(self.device.trigger_level, 0, 255, 1, 100, 10)
        level_scale = Gtk.Scale.new(Gtk.Orientation.VERTICAL, level_adjust)
        level_scale.set_size_request(-1, 100)
        level_scale.set_inverted(True)
        level_scale.set_round_digits(0)

        def set_trigger_level(btn):
            self.device.trigger_level = level_scale.get_value()
            pass

        level_set = Gtk.Button('SET')
        level_set.connect('pressed', set_trigger_level)

        btn_rise = Gtk.ToggleButton('RISE')
        btn_fall = Gtk.ToggleButton('FALL')
        btn_both = Gtk.ToggleButton('BOTH')
        btn_othr = Gtk.ToggleButton('OTHER')  # that fucked-up name is intentional

        btn_rise.props.active = True  # TODO pull current one from device

        def btn_callback(btn_pressed):
            if btn_pressed.props.active:

                # remove other pressed options(so e.g. rising and falling isn't selected at once)
                if btn_pressed != btn_rise:
                    btn_rise.props.active = False
                if btn_pressed != btn_fall:
                    btn_fall.props.active = False
                if btn_pressed != btn_both:
                    btn_both.props.active = False
                if btn_pressed != btn_othr:
                    btn_othr.props.active = False

                # process each btn
                if btn_pressed == btn_othr:
                    task_fail()  # TODO add msg with apology
                elif btn_pressed == btn_rise:
                    self.device.trigger_mode = 'RISING'
                elif btn_pressed == btn_fall:
                    self.device.trigger_mode = 'FALLING'
                elif btn_pressed == btn_both:
                    self.device.trigger_mode = 'BOTH'

        btn_rise.connect('toggled', btn_callback)
        btn_fall.connect('toggled', btn_callback)
        btn_both.connect('toggled', btn_callback)
        btn_othr.connect('toggled', btn_callback)

        self.attach(label, 0, 0, 2, 1)
        self.attach(level_scale, 1, 1, 1, 3)
        self.attach(btn_rise, 0, 1, 1, 1)
        self.attach(btn_fall, 0, 2, 1, 1)
        self.attach(btn_both, 0, 3, 1, 1)
        self.attach(btn_othr, 0, 4, 1, 1)
        self.attach(level_set, 1, 4, 1, 1)



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
    from Devices.Dummy import Device
    test_util(Settings(Device()))
