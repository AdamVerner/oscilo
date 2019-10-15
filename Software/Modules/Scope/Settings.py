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
from Software.Popups import task_fail
from Software.Devices import Device

LABEL_START = '<big>'
LABEL_END = '</big>'
LABEL_PROPS = {'xpad': 12,
               'use_markup': True
               }


class Settings(Gtk.Grid):
    """
    wrapper for the underlying classes
    """

    def __init__(self, device: Device):
        super(Settings, self).__init__()
        self.device = device
        self.size = (800, 400)

        self.trigger = Trigger(self.device)
        self.vertical = Vertical(self.device)
        self.horizontal = Horizontal(self.device)
        self.filtering = Filters()
        self.control = Control(self.device)

        # TODO add dividers
        self.set_border_width(10)
        self.set_column_spacing(20)

        self.set_row_homogeneous(True)
        self.set_column_homogeneous(True)

        self.attach(self.trigger, 0, 0, 1, 1)
        self.attach(self.vertical, 1, 0, 1, 1)
        self.attach(self.horizontal, 2, 0, 1, 1)
        self.attach(self.filtering, 3, 0, 1, 1)
        self.attach(self.control, 4, 0, 1, 1)


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

    def __init__(self, device: Device):
        super(Trigger, self).__init__()
        self.device = device
        label = Gtk.Label(LABEL_START + 'TRIGGER MENU' + LABEL_END, **LABEL_PROPS)

        level_adjust = Gtk.Adjustment(self.device.get_trig_lvl(), self.device.trig_min,
                                      self.device.trig_max, 1, 1, 1)
        level_scale = Gtk.Scale.new(Gtk.Orientation.VERTICAL, level_adjust)
        level_scale.set_size_request(-1, 100)
        level_scale.set_inverted(True)
        level_scale.set_round_digits(0)

        def set_trigger_level(btn):
            self.device.set_trig_lvl(level_scale.get_value())
            pass

        level_set = Gtk.Button('SET')
        level_set.connect('pressed', set_trigger_level)

        btn_rise = Gtk.ToggleButton('RISE')
        btn_fall = Gtk.ToggleButton('FALL')
        btn_both = Gtk.ToggleButton('BOTH')
        btn_othr = Gtk.ToggleButton('OTHER')  # fucked-up variable name is intentional

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
                # TODO poll trigger modes from device
                if btn_pressed == btn_othr:
                    self.device.set_trigger_mode(self.device.TRIG_MODES.NONE)
                    task_fail()
                elif btn_pressed == btn_rise:
                    self.device.set_trigger_mode(self.device.TRIG_MODES.RISE)
                elif btn_pressed == btn_fall:
                    self.device.set_trigger_mode(self.device.TRIG_MODES.FALL)
                elif btn_pressed == btn_both:
                    self.device.set_trigger_mode(self.device.TRIG_MODES.BOTH)

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

    def __init__(self, device: Device):
        super(Vertical, self).__init__()
        self.device = device
        label = Gtk.Label(LABEL_START + 'VERTICAL MENU' + LABEL_END, **LABEL_PROPS)
        self.attach(label, 0, 0, 3, 1)

        if not self.device.HAS_VERTICAL:
            not_implemented_label = Gtk.Label('Device dosn\'t support this option')
            self.attach(not_implemented_label, 0, 1, 3, 1)
            return


        vga_label = Gtk.Label('GAIN')
        att_label = Gtk.Label('ATT')
        off_label = Gtk.Label('OFFSET')

        def vga_callback(_):
            self.device.vga_level = vga_scale.get_value()

        def att_callback(_):
            """snap to concrete value specified in device.att_steps"""
            # https://stackoverflow.com/questions/12141150/
            # from list of ints, get number closest to given value
            value = min(self.device.att_steps, key=lambda x: abs(x - att_scale.get_value()))
            att_scale.set_value(value)
            self.device.att_level = value

        def off_callback(_):
            self.device.offset = off_scale.get_value()

        vga_set = Gtk.Button('SET')
        att_set = Gtk.Button('SET')
        off_set = Gtk.Button('SET')

        vga_set.connect('pressed', vga_callback)
        att_set.connect('pressed', att_callback)
        off_set.connect('pressed', off_callback)

        vga_adj = Gtk.Adjustment(self.device.vga_level, self.device.vga_min, self.device.vga_max,
                                 1, 1, )
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

        off_adj = Gtk.Adjustment(self.device.offset, 0, 25, 1, 1)

        off_scale = Gtk.Scale.new(Gtk.Orientation.VERTICAL, off_adj)
        off_scale.set_size_request(-1, 100)
        att_scale.set_inverted(True)
        att_scale.set_round_digits(0)

        self.attach(vga_label, 0, 1, 1, 1)
        self.attach(att_label, 1, 1, 1, 1)
        self.attach(off_label, 2, 1, 1, 1)

        self.attach(vga_scale, 0, 2, 1, 1)
        self.attach(att_scale, 1, 2, 1, 1)
        self.attach(off_scale, 2, 2, 1, 1)

        self.attach(vga_set, 0, 3, 1, 1)
        self.attach(att_set, 1, 3, 1, 1)
        self.attach(off_set, 2, 3, 1, 1)


class Horizontal(Gtk.Grid):
    """
    position
    sec/div
    |------------------|
    | |--------------| |
    | |  POS ADJUST  | |
    | |--------------| |
    | |--------------| |
    | |    POS SET   | |
    | |--------------| |
    | |--------------| |
    | | SPEED ADJUST | |
    | |--------------| |
    | |--------------| |
    | |  SPEED SET   | |
    | |--------------| |
    """

    exp = 4.0

    def __init__(self, device: Device):
        super(Horizontal, self).__init__()
        self.device = device
        label = Gtk.Label(LABEL_START + 'HORIZONTAL MENU' + LABEL_END, **LABEL_PROPS)

        pos_lbl = Gtk.Label()
        pos_lbl.set_use_markup(True)
        spd_lbl = Gtk.Label()
        spd_lbl.set_use_markup(True)

        pos_adj = Gtk.Adjustment(self.device.get_trig_place(), 0, 1.1, 0.1, 0.1, 0.1)
        pos_adj.set_value(self.device.get_trig_place())

        maximum = self.device.MAX_SPEED ** (1.02535 / self.exp)
        minimum = self.device.MIN_SPEED ** (1.0 / self.exp)
        current = self.device.get_sampling_speed() ** (1.0 / self.exp)

        spd_adj = Gtk.Adjustment(current, minimum, maximum, 1, 1, 10)
        spd_adj.set_value(current)

        pos_scale = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, pos_adj)
        pos_scale.set_size_request(-1, -1)
        pos_scale.set_draw_value(False)

        spd_scale = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, spd_adj)
        spd_scale.set_size_request(-1, -1)
        spd_scale.set_draw_value(False)

        def pos_changed(adjust):
            val = pos_adj.get_value()
            print(val)
            pos_lbl.set_markup("<span color='green'> %.2f%%</span>" % val)
        pos_adj.connect('value-changed', pos_changed)

        def spd_to_str(speed):
            if speed <= 2000:
                return '%.1f Hz' % speed
            if speed <= 1500000:
                return '%.2f KHz' % (speed / 1000)
            return '%.2f Mhz' % (speed / 1000000)

        def spd_changed(adjust):
            val = spd_adj.get_value() ** self.exp
            spd_lbl.set_markup("<span color='green'>%s</span>" % spd_to_str(val))
        spd_adj.connect('value-changed', spd_changed)

        def pos_set(btn):
            self.device.set_trig_place(pos_scale.get_value())
            pos_lbl.set_markup("<span color='black'>{0:.2f}%</span>".format(
                pos_adj.get_value()))

        pos_btn = Gtk.Button('SET Position')
        pos_btn.connect('pressed', pos_set)
        spd_btn = Gtk.Button('SET Speed')

        # changed(post_adj)  # trigger once, so the default value gets overwritten
        def spd_set(btn):
            val = spd_scale.get_value() ** self.exp
            spd_lbl.set_markup("<span color='black'>%s</span>" %
                               spd_to_str(self.device.set_sampling_speed(val)))
        spd_btn.connect('pressed', spd_set)

        pos_changed(None)
        spd_changed(None)


        self.attach(label,      0, 0, 1, 1)

        self.attach(pos_lbl,   0, 1, 1, 1)
        self.attach(pos_scale, 0, 2, 1, 1)
        self.attach(pos_btn,   0, 3, 1, 1)

        self.attach(spd_lbl,   0, 4, 1, 1)
        self.attach(spd_scale, 0, 5, 1, 1)
        self.attach(spd_btn,   0, 6, 1, 1)


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

    def push_wrap(self, *_):
        if self.push_func:
            print('calling push functiuon', self.push_func)
            self.push_func()

    def __init__(self, device: Device):
        super(Control, self).__init__()
        self.device = device
        label = Gtk.Label(LABEL_START + 'CONTROL' + LABEL_END, **LABEL_PROPS)

        ctrl_btn = Gtk.Button('READY')
        pull_btn = Gtk.Button('PULL')

        self.auto_pull = Gtk.CheckButton()
        auto_pull_lbl = Gtk.Label('Auto pull')

        ctrl_btn.connect('pressed', self.ctrl_begin_callback)
        pull_btn.connect('pressed', self.push_wrap)

        self.attach(label, 0, 0, 2, 1)
        self.attach(ctrl_btn, 0, 1, 2, 1)
        self.attach(auto_pull_lbl, 0, 2, 1, 1)
        self.attach(self.auto_pull, 1, 2, 1, 1)

        self.attach(Gtk.Label(''), 0, 3, 2, 1)
        self.attach(pull_btn, 0, 4, 2, 1)

        # Glib workaround begin
        # https://stackoverflow.com/questions/13518452/
        parent_conn, self.child_conn = Pipe(duplex=False)  # Pipe to pump the label data through

        self.child_conn.send("<span color='green'>READY</span>")

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
            self.push_func()

    def ctrl_begin_callback(self, *_):
        self.child_conn.send("<span color='#999910'>ACTIVE</span>")
        self.device.activate_scope(self.sampling_cb, self.done_cb)


if __name__ == '__main__':
    from Software.TestUtil import test_util
    from Software.Devices import Device

    test_util(Settings(Device()))
