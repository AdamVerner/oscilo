import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def test_util(subject, *functions):
    """
    this function does not exit, unless KeyboardInterrupt is raised
    creates button for every function passed
    """

    w = Gtk.Window()
    g = Gtk.Grid()
    w.add(g)

    g.attach(subject, 0, 0, 3, 1)

    # create button for each function
    btns = [Gtk.Button(label=f.__name__) for f in functions]

    # connect each function to a button
    [btn.connect('clicked', f) for btn, f in zip(btns, functions)]

    # attach every button to grid
    [g.attach(btn, idx, 1, 1, 1) for idx, btn in enumerate(btns)]

    w.show_all()
    Gtk.main()
