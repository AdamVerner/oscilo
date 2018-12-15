# /bin/env python3
# -*- coding: utf-8 -*-
"""

  |----------------------------------------------------------------------------|
  |   TRIGGER_SETTING    #    Horizontal     #    VERTICAL    #    FILTERING   |
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
from gi.repository import Gtk, GObject
from multiprocessing import Pipe
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
        self.vertical   = Vertical(self.device)
        self.horizontal = Horizontal(self.device)
        self.filtering  = Filters()
        self.control    = Control(self.device)

        # TODO add dividers
        self.set_border_width(10)
        self.set_column_spacing(20)

        self.set_row_homogeneous(True)
        self.set_column_homogeneous(True)

        self.attach(self.trigger,    0, 0, 1, 1)
        self.attach(self.vertical,   1, 0, 1, 1)
        self.attach(self.horizontal, 2, 0, 1, 1)
        self.attach(self.filtering,  3, 0, 1, 1)
        self.attach(self.control,    4, 0, 1, 1)


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

        level_adjust = Gtk.Adjustment(self.device.trig_lvl, self.device.trig_min,
                                      self.device.trig_max, 1, 1, 1)
        level_scale = Gtk.Scale.new(Gtk.Orientation.VERTICAL, level_adjust)
        level_scale.set_size_request(-1, 100)
        level_scale.set_inverted(True)
        level_scale.set_round_digits(0)

        def set_trigger_level(btn):
            self.device.trig_lvl = level_scale.get_value()
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

    def __init__(self, device):
        super(Vertical, self).__init__()
        self.device = device
        label = Gtk.Label(LABEL_START + 'VERTICAL MENU' + LABEL_END, **LABEL_PROPS)

        vga_label = Gtk.Label('VGA')
        att_label = Gtk.Label('ATT')

        def vga_callback(_):
            self.device.vga_level = vga_scale.get_value()
            self.device.trig_lvl(122)

        def att_callback(_):
            """snap to concrete value specified in device.att_steps"""
            # https://stackoverflow.com/questions/12141150/
            # from list of ints, get number closest to given value
            value = min(self.device.att_steps, key=lambda x: abs(x - att_scale.get_value()))
            att_scale.set_value(value)
            self.device.att_level = value

            pass

        vga_set = Gtk.Button('SET')
        att_set = Gtk.Button('SET')

        vga_set.connect('pressed', vga_callback)
        att_set.connect('pressed', att_callback)

        vga_adj = Gtk.Adjustment(self.device.vga_level, self.device.vga_min, self.device.vga_max,
                                 1, 1,)
        vga_scale = Gtk.Scale.new(Gtk.Orientation.VERTICAL, vga_adj)
        vga_scale.set_size_request(-1, 100)
        vga_scale.set_inverted(True)
        vga_scale.set_round_digits(0)

        att_adj = Gtk.Adjustment(self.device.att_level,
                                 min(self.device.att_steps),
                                 max(self.device.att_steps),
                                 1, 1)
        att_scale = Gtk.Scale.new(Gtk.Orientation.VERTICAL, att_adj)
        att_scale.set_size_request(-1, 100)
        att_scale.set_inverted(True)
        att_scale.set_round_digits(0)

        for step in self.device.att_steps:
            att_scale.add_mark(step, Gtk.PositionType.RIGHT)

        self.attach(label, 0, 0, 2, 1)
        self.attach(vga_label, 0, 1, 1, 1)
        self.attach(att_label, 1, 1, 1, 1)
        self.attach(vga_scale, 0, 2, 1, 1)
        self.attach(att_scale, 1, 2, 1, 1)

        self.attach(vga_set, 0, 3, 1, 1)
        self.attach(att_set, 1, 3, 1, 1)


class Horizontal(Gtk.Grid):
    """
    position
    sec/div
    |------------------|
    | |--------------| |
    | |  SPIN BUTTON | |
    | |--------------| |
    | |--------------| |
    | |    ROUGH     | |
    | |--------------| |
    | |--------------| |
    | |     SET      | |
    | |--------------| |
    |------------------|
    """

    def __init__(self, device):
        super(Horizontal, self).__init__()
        self.device = device
        label = Gtk.Label(LABEL_START + 'HORIZONTAL MENU' + LABEL_END, **LABEL_PROPS)

        el = Gtk.Label()

        sps_adjust = Gtk.Adjustment(100, 0, 255, 1, 1, 1)
        sps_scale = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, sps_adjust)
        sps_scale.set_size_request(-1, -1)
        sps_scale.set_inverted(True)
        sps_scale.set_round_digits(0)

        sps_spin = Gtk.SpinButton()

        def set_sps(_):
            self.device.trig_lvl = sps_scale.get_value()
            pass

        sps_set = Gtk.Button('SET')
        sps_set.connect('pressed', set_sps)

        self.attach(label, 0, 0, 1, 1)
        self.attach(el, 0, 1, 1, 1)
        self.attach(sps_spin, 0, 2, 1, 1)
        self.attach(sps_scale, 0, 3, 1, 1)
        self.attach(sps_set, 0, 4, 1, 1)


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

        not_implemented_label = Gtk.Label('Not implemented yet...')

        self.attach(label, 0, 0, 1, 1)
        self.attach(not_implemented_label, 0, 1, 1, 1)


class Control(Gtk.Grid):
    """
    only for get_samples button for now
    """

    push_func = None  # function to call when automatic sample collection is wanted

    def __init__(self, device):
        super(Control, self).__init__()
        self.device = device
        label = Gtk.Label(LABEL_START + 'CONTROL' + LABEL_END, **LABEL_PROPS)

        ctrl_btn  = Gtk.Button('READY')
        self.auto_pull = Gtk.CheckButton()
        auto_pull_lbl = Gtk.Label('Auto pull')

        ctrl_btn.connect('pressed', self.ctrl_begin_callback)

        self.attach(label, 0, 0, 2, 1)
        self.attach(ctrl_btn, 0, 1, 2, 1)
        self.attach(auto_pull_lbl, 0, 2, 1, 1)
        self.attach(self.auto_pull, 1, 2, 1, 1)

        # Glib workaround begin
        # https://stackoverflow.com/questions/13518452/
        parent_conn, self.child_conn = Pipe(duplex=False)  # Pipe to pump the label data through

        def read_data(source, condition):
            """
            watches pipe and when data changes, changes the label
            """
            assert parent_conn.poll()
            i = parent_conn.recv()
            for child in ctrl_btn.get_children():
                child.set_label(i)
                child.set_use_markup(True)
            return True  # continue reading

        GObject.io_add_watch(parent_conn.fileno(), GObject.IO_IN, read_data)

        # Glib workaround end

    def sampling_cb(self, *_):
        print('trigger received')
        self.child_conn.send("<span color='#999910'>TRIGR'D</span>")

    def done_cb(self, *_):
        self.child_conn.send("<span color='green'>READY</span>")
        # change button label
        # plot values if the option is enabled
        if self.auto_pull.get_active() and self.push_func:
            print('pushing samples to graph')
            self.push_func(self.device.get_samples())

    def ctrl_begin_callback(self, *_):
        self.child_conn.send("<span color='#999910'>ACTIVE</span>")
        self.device.activate_scope(self.sampling_cb, self.done_cb)


if __name__ == '__main__':
    from TestUtil import test_util
    from Devices.Dummy import Device
    test_util(Settings(Device()))
