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
from gi.repository import Gtk, Gdk


class Signals(Gtk.Grid):
    """
    selects signal that will be highlighted
    possibility to add more signals
        - reference signals from CSV files
        - Math with other signals


    """

    def __init__(self):
        super(Signals, self).__init__()
        l = Gtk.Label('testLabel')
        self.attach(l, 0, 0, 1, 1)

        self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0.5, 0.5, 0.5, 0.1))


class Signal(Gtk.Grid):
    """
    |--------------------|
    |        NAME        |
    | Color              |
    | Export             |
    |                    |
    |--------------------|

    """

    def __init__(self):
        super(Signal, self).__init__()

        label = Gtk.Label()
        label.set_markup('<big><b>COLOR</b></big>')

        self.attach(label, 0, 0, 2, 1)

        self.color_button = Gtk.ColorButton()

        # with a default color (blue, in this instance)
        color = Gdk.RGBA()
        self.color_button.set_rgba(color)

        # choosing a color in the dialogue window emits a signal
        self.color_button.connect("color-set", self.on_color_chosen)

        color_label = Gtk.Label()
        color_label.set_markup('COLOR')
        self.attach(color_label, 0, 1, 1, 1)
        self.attach(self.color_button, 1, 1, 1, 1)

    def on_color_chosen(self, user_data):
        print("You chose the color: " + self.color_button.get_rgba().to_string())


if __name__ == '__main__':
    from Software.TestUtil import test_util

    s = Signal()
    test_util(s)
