
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Module(Gtk.Box):


    def __init__(self):
        super(Module, self).__init__()
        self.set_border_width(10)

        string = """
<span foreground="blue" size="x-large">USB osciloscope controll application</span>

This is an OpenSource osciloscope controll application written in python with usage of GTK3+
This project was developed as a school work, but it's much more than that.
"""



        lbl = Gtk.Label()
        # lbl.set_justify(Gtk.JUSTIFY_LEFT)
        print(lbl.get_justify())
        lbl.set_xalign(0)
        lbl.set_yalign(0)
        lbl.set_use_markup(True)
        lbl.set_markup(string)
        self.add(lbl)
        self.show_all()

