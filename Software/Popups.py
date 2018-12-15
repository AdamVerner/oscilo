# /bin/env python3
# -*- coding: utf-8 -*-
"""
popup errors indicating what has gone wrong
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def task_fail(title="Task Failed", msg="Task Failed successfully"):
    """
    shows ERROR popup with some info about task that failed
    :param title: short string that shows as title
    :param msg: can be markup text  
    """
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.CANCEL,
                               title)
    dialog.format_secondary_markup(msg)
    ret = dialog.run()
    dialog.destroy()
    return ret


if __name__ == '__main__':
    task_fail()
