#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
"""
import os
os.environ['NO_AT_BRIDGE'] = '1'

from .MainWindow import MainWindow

MainWindow()
